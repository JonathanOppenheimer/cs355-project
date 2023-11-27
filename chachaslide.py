import json
from base64 import b64decode, b64encode

from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes

message = b"hi brian"


# Encryption with hey 1 
key1 = get_random_bytes(32)
cipher1 = ChaCha20.new(key=key1)
ciphertext1 = cipher1.encrypt(message)
nonce1 = b64encode(cipher1.nonce).decode('utf-8')
ct1 = b64encode(ciphertext1).decode('utf-8')

# Encryption with key 2 
key2 = get_random_bytes(32)
cipher2 = ChaCha20.new(key=key2)
ciphertext2 = cipher2.encrypt(ciphertext1)
nonce2 = b64encode(cipher2.nonce).decode('utf-8')
ct2 = b64encode(ciphertext2).decode('utf-8')


# Decryption with key 2
try:
    cipher = ChaCha20.new(key=key2, nonce=b64decode(nonce2))
    intermediary = cipher.decrypt(ciphertext2)
except (ValueError, KeyError):
    print("Incorrect decryption")

# Decryption with key 1
try:
    cipher = ChaCha20.new(key=key1, nonce=b64decode(nonce1))
    final = cipher.decrypt(intermediary)
    print(str(final))
except (ValueError, KeyError):
    print("Incorrect decryption")


# Bob gets his piece of code
# Encrypts with his key + nonce



