import json
import logging
from base64 import b64decode, urlsafe_b64decode, b64encode, urlsafe_b64encode
from urllib.parse import unquote_plus

from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from Crypto.Signature import PKCS1_v1_5 as PKCSSign
from lxml import etree

from federation.exceptions import EncryptedMessageError, NoSenderKeyFoundError
from federation.protocols.base import BaseProtocol
from federation.protocols.diaspora.encrypted import EncryptedPayload
from federation.protocols.diaspora.magic_envelope import MagicEnvelope
from federation.utils.diaspora import fetch_public_key
from federation.utils.text import decode_if_bytes, encode_if_text

logger = logging.getLogger("federation")

PROTOCOL_NAME = "diaspora"
PROTOCOL_NS = "https://joindiaspora.com/protocol"
MAGIC_ENV_TAG = "{http://salmon-protocol.org/ns/magic-env}env"


def identify_payload(payload):
    """Try to identify whether this is a Diaspora payload.

    Try first public message. Then private message. The check if this is a legacy payload.
    """
    # Private encrypted JSON payload
    try:
        data = json.loads(decode_if_bytes(payload))
        if "encrypted_magic_envelope" in data:
            return True
    except Exception:
        pass
    # Public XML payload
    try:
        xml = etree.fromstring(encode_if_text(payload))
        if xml.tag == MAGIC_ENV_TAG:
            return True
    except Exception:
        pass
    # Legacy XML payload
    try:
        xml = unquote_plus(payload)
        return xml.find('xmlns="%s"' % PROTOCOL_NS) > -1
    except Exception:
        pass
    return False


class Protocol(BaseProtocol):
    """Diaspora protocol parts

    Mostly taken from Pyaspora (https://github.com/lukeross/pyaspora).
    """
    def __init__(self):
        super().__init__()
        self.encrypted = self.legacy = False

    def get_json_payload_magic_envelope(self, payload):
        """Encrypted JSON payload"""
        private_key = self._get_user_key(self.user)
        return EncryptedPayload.decrypt(payload=payload, private_key=private_key)

    def store_magic_envelope_doc(self, payload):
        """Get the Magic Envelope, trying JSON first."""
        try:
            json_payload = json.loads(decode_if_bytes(payload))
        except ValueError:
            # XML payload
            xml = unquote_plus(decode_if_bytes(payload))
            xml = xml.lstrip().encode("utf-8")
            logger.debug("diaspora.protocol.store_magic_envelope_doc: xml payload: %s", xml)
            self.doc = etree.fromstring(xml)
        else:
            logger.debug("diaspora.protocol.store_magic_envelope_doc: json payload: %s", json_payload)
            self.doc = self.get_json_payload_magic_envelope(json_payload)

    def receive(self, payload, user=None, sender_key_fetcher=None, skip_author_verification=False):
        """Receive a payload.

        For testing purposes, `skip_author_verification` can be passed. Authorship will not be verified."""
        self.user = user
        self.get_contact_key = sender_key_fetcher
        self.store_magic_envelope_doc(payload)
        # Check for a legacy header
        self.find_header()
        # Open payload and get actual message
        self.content = self.get_message_content()
        # Get sender handle
        self.sender_handle = self.get_sender()
        # Verify the message is from who it claims to be
        if not skip_author_verification:
            self.verify_signature()
        return self.sender_handle, self.content

    def _get_user_key(self, user):
        if not getattr(self.user, "private_key", None):
            raise EncryptedMessageError("Cannot decrypt private message without user key")
        return self.user.private_key

    def find_header(self):
        self.header = self.doc.find(".//{"+PROTOCOL_NS+"}header")
        if self.header != None:
            # Legacy public header found
            self.legacy = True
            return
        if self.doc.find(".//{" + PROTOCOL_NS + "}encrypted_header") == None:
            # No legacy encrypted header found
            return
        self.legacy = True
        if not self.user:
            raise EncryptedMessageError("Cannot decrypt private message without user object")
        user_private_key = self._get_user_key(self.user)
        self.encrypted = True
        self.header = self.parse_header(
            self.doc.find(".//{"+PROTOCOL_NS+"}encrypted_header").text,
            user_private_key
        )

    def get_sender(self):
        if self.legacy:
            return self.get_sender_legacy()
        return MagicEnvelope.get_sender(self.doc)

    def get_sender_legacy(self):
        try:
            return self.header.find(".//{"+PROTOCOL_NS+"}author_id").text
        except AttributeError:
            # Look at the message, try various elements
            message = etree.fromstring(self.content)
            element = message.find(".//author")
            if element is None:
                element = message.find(".//sender_handle")
            if element is None:
                element = message.find(".//diaspora_handle")
            if element is None:
                return None
            return element.text

    def get_message_content(self):
        """
        Given the Slap XML, extract out the payload.
        """
        body = self.doc.find(
            ".//{http://salmon-protocol.org/ns/magic-env}data").text

        if self.encrypted:
            body = self._get_encrypted_body(body)
        else:
            body = urlsafe_b64decode(body.encode("ascii"))

        logger.debug("diaspora.protocol.get_message_content: %s", body)
        return body

    def _get_encrypted_body(self, body):
        """
        Decrypt the body of the payload.
        """
        inner_iv = b64decode(self.header.find(".//iv").text.encode("ascii"))
        inner_key = b64decode(
            self.header.find(".//aes_key").text.encode("ascii"))
        decrypter = AES.new(inner_key, AES.MODE_CBC, inner_iv)
        body = b64decode(urlsafe_b64decode(body.encode("ascii")))
        body = decrypter.decrypt(body)
        body = self.pkcs7_unpad(body)
        return body

    def verify_signature(self):
        """
        Verify the signed XML elements to have confidence that the claimed
        author did actually generate this message.
        """
        if self.get_contact_key:
            sender_key = self.get_contact_key(self.sender_handle)
        else:
            sender_key = fetch_public_key(self.sender_handle)
        if not sender_key:
            raise NoSenderKeyFoundError("Could not find a sender contact to retrieve key")
        MagicEnvelope(doc=self.doc, public_key=sender_key, verify=True)

    def parse_header(self, b64data, key):
        """
        Extract the header and decrypt it. This requires the User's private
        key and hence the passphrase for the key.
        """
        decoded_json = b64decode(b64data.encode("ascii"))
        rep = json.loads(decoded_json.decode("ascii"))
        outer_key_details = self.decrypt_outer_aes_key_bundle(
            rep["aes_key"], key)
        header = self.get_decrypted_header(
            b64decode(rep["ciphertext"].encode("ascii")),
            key=b64decode(outer_key_details["key"].encode("ascii")),
            iv=b64decode(outer_key_details["iv"].encode("ascii"))
        )
        return header

    def decrypt_outer_aes_key_bundle(self, data, key):
        """
        Decrypt the AES "outer key" credentials using the private key and
        passphrase.
        """
        if not key:
            raise EncryptedMessageError("No key to decrypt with")
        cipher = PKCS1_v1_5.new(key)
        decoded_json = cipher.decrypt(
            b64decode(data.encode("ascii")),
            sentinel=None
        )
        return json.loads(decoded_json.decode("ascii"))

    def get_decrypted_header(self, ciphertext, key, iv):
        """
        Having extracted the AES "outer key" (envelope) information, actually
        decrypt the header.
        """
        encrypter = AES.new(key, AES.MODE_CBC, iv)
        padded = encrypter.decrypt(ciphertext)
        xml = self.pkcs7_unpad(padded)
        doc = etree.fromstring(xml)
        return doc

    def pkcs7_unpad(self, data):
        """
        Remove the padding bytes that were added at point of encryption.
        """
        if isinstance(data, str):
            return data[0:-ord(data[-1])]
        else:
            return data[0:-data[-1]]

    def build_send(self, entity, from_user, to_user=None, *args, **kwargs):
        """Build POST data for sending out to remotes."""
        if entity.outbound_doc:
            # Use pregenerated outbound document
            xml = entity.outbound_doc
        else:
            xml = entity.to_xml()
        self.init_message(xml, from_user.handle, from_user.private_key)
        xml = self.create_salmon_envelope(to_user)
        return {'xml': xml}

    def init_message(self, message, author_username, private_key):
        """
        Build a Diaspora message and prepare to send the payload <message>,
        authored by Contact <author>. The receipient is specified later, so
        that the same message can be sent to several people without needing to
        keep re-encrypting the inner.
        """

        # We need an AES key for the envelope
        self.inner_iv = get_random_bytes(AES.block_size)
        self.inner_key = get_random_bytes(32)
        self.inner_encrypter = AES.new(
            self.inner_key, AES.MODE_CBC, self.inner_iv)

        # ...and one for the payload message
        self.outer_iv = get_random_bytes(AES.block_size)
        self.outer_key = get_random_bytes(32)
        self.outer_encrypter = AES.new(
            self.outer_key, AES.MODE_CBC, self.outer_iv)
        self.message = message
        self.author_username = author_username
        self.private_key = private_key

    def xml_to_string(self, doc, xml_declaration=False):
        """
        Utility function to turn an XML document to a string. This is
        abstracted out so that pretty-printing can be turned on and off in one
        place.
        """
        return etree.tostring(
            doc,
            xml_declaration=xml_declaration,
            pretty_print=True,
            encoding="UTF-8"
        )

    def create_decrypted_header(self):
        """
        Build the XML document for the header. The header contains the key
        used to encrypt the message body.
        """
        decrypted_header = etree.Element('decrypted_header')
        etree.SubElement(decrypted_header, "iv").text = \
            b64encode(self.inner_iv)
        etree.SubElement(decrypted_header, "aes_key").text = \
            b64encode(self.inner_key)
        etree.SubElement(decrypted_header, "author_id").text = \
            self.author_username
        return self.xml_to_string(decrypted_header)

    def create_public_header(self):
        decrypted_header = etree.Element('header')
        etree.SubElement(decrypted_header, "author_id").text = \
            self.author_username
        return decrypted_header

    def create_ciphertext(self):
        """
        Encrypt the header.
        """
        to_encrypt = self.pkcs7_pad(
            self.create_decrypted_header(),
            AES.block_size
        )
        out = self.outer_encrypter.encrypt(to_encrypt)
        return out

    def create_outer_aes_key_bundle(self):
        """
        Record the information on the key used to encrypt the header.
        """
        d = json.dumps({
            "iv": b64encode(self.outer_iv).decode("ascii"),
            "key": b64encode(self.outer_key).decode("ascii")
        })
        return d

    def create_encrypted_outer_aes_key_bundle(self, recipient_rsa):
        """
        The Outer AES Key Bundle is encrypted with the receipient's public
        key, so only the receipient can decrypt the header.
        """
        cipher = PKCS1_v1_5.new(recipient_rsa)
        return cipher.encrypt(
            self.create_outer_aes_key_bundle().encode("utf-8"))

    def create_encrypted_header_json_object(self, public_key):
        """
        The actual header and the encrypted outer (header) key are put into a
        document together.
        """
        aes_key = b64encode(self.create_encrypted_outer_aes_key_bundle(
            public_key)).decode("ascii")
        ciphertext = b64encode(self.create_ciphertext()).decode("ascii")

        d = json.dumps({
            "aes_key": aes_key,
            "ciphertext": ciphertext
        })
        return d

    def create_encrypted_header(self, public_key):
        """
        The "encrypted header JSON object" is dropped into some XML. I am not
        sure what this is for, but is required to interact.
        """
        doc = etree.Element("encrypted_header")
        doc.text = b64encode(self.create_encrypted_header_json_object(
            public_key).encode("ascii"))
        return doc

    def create_payload(self):
        """
        Wrap the actual payload message in the standard XML wrapping.
        """
        doc = etree.Element("XML")
        inner = etree.SubElement(doc, "post")
        if isinstance(self.message, str):
            inner.text = self.message
        else:
            inner.append(self.message)
        return self.xml_to_string(doc)

    def create_encrypted_payload(self):
        """
        Encrypt the payload XML with the inner (body) key.
        """
        to_encrypt = self.pkcs7_pad(self.create_payload(), AES.block_size)
        return self.inner_encrypter.encrypt(to_encrypt)

    def create_salmon_envelope(self, recipient):
        """
        Build the whole message, pulling together the encrypted payload and the
        encrypted header. Selected elements are signed by the author so that
        tampering can be detected.

        Note, this corresponds to the old Diaspora protocol which will slowly be replaced by the
        new version. See PR https://github.com/diaspora/diaspora_federation/issues/30

        Args:
            recipient - Recipient object which must have public key as `key` (private messages only)

        Returns:
            XML document as string
        """
        nsmap = {
            None: PROTOCOL_NS,
            'me': 'http://salmon-protocol.org/ns/magic-env'
        }
        doc = etree.Element("{%s}diaspora" % nsmap[None], nsmap=nsmap)
        if recipient:
            doc.append(self.create_encrypted_header(recipient.key))
        else:
            doc.append(self.create_public_header())
        env = etree.SubElement(doc, "{%s}env" % nsmap["me"])
        etree.SubElement(env, "{%s}encoding" % nsmap["me"]).text = 'base64url'
        etree.SubElement(env, "{%s}alg" % nsmap["me"]).text = 'RSA-SHA256'
        if recipient:
            payload = urlsafe_b64encode(b64encode(
                self.create_encrypted_payload())).decode("ascii")
        else:
            payload = urlsafe_b64encode(self.create_payload()).decode("ascii")
        etree.SubElement(env, "{%s}data" % nsmap["me"],
                         {"type": "application/xml"}).text = payload
        sig_contents = payload + "." + \
            b64encode(b"application/xml").decode("ascii") + "." + \
            b64encode(b"base64url").decode("ascii") + "." + \
            b64encode(b"RSA-SHA256").decode("ascii")
        sig_hash = SHA256.new(sig_contents.encode("ascii"))
        cipher = PKCSSign.new(self.private_key)
        sig = urlsafe_b64encode(cipher.sign(sig_hash))
        etree.SubElement(env, "{%s}sig" % nsmap["me"]).text = sig
        return self.xml_to_string(doc)

    def pkcs7_pad(self, inp, block_size):
        """
        Using the PKCS#7 padding scheme, pad <inp> to be a multiple of
        <block_size> bytes. Ruby's AES encryption pads with this scheme, but
        pycrypto doesn't support it.
        """
        val = block_size - len(inp) % block_size
        if val == 0:
            return inp + (self.array_to_bytes([block_size]) * block_size)
        else:
            return inp + (self.array_to_bytes([val]) * val)

    def array_to_bytes(self, vals):
        return bytes(vals)
