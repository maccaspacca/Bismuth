import base64, os, getpass, hashlib
try:
    from simplecrypt import decrypt
except ImportError:
    decrypt = None
from Crypto.PublicKey import RSA
import sys

def read():
    # import keys
    if not os.path.exists('privkey_encrypted.der'):
        password = ""
        key = RSA.importKey(open('privkey.der').read())
        private_key_readable = key.exportKey().decode("utf-8")
        # public_key = key.publickey()
    else:
        if not decrypt:
            print("Key decryption not available, install simplecrypt")
            sys.exit()
        password = getpass.getpass()
        encrypted_privkey = open('privkey_encrypted.der').read()
        decrypted_privkey = decrypt(password, base64.b64decode(encrypted_privkey))
        key = RSA.importKey(decrypted_privkey)  # be able to sign
        private_key_readable = key.exportKey().decode("utf-8")

    public_key_readable = open('pubkey.der').read()
    public_key_hashed = base64.b64encode(public_key_readable.encode("utf-8")).decode("utf-8")
    address = hashlib.sha224(public_key_readable.encode("utf-8")).hexdigest()
    # import keys

    return key, private_key_readable, public_key_readable, public_key_hashed, address