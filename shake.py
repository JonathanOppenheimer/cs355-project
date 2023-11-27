import hashlib
import numpy as np

bob_passphrase = b"no_ops_allowed"
alice_passphrase = b"albert_fan_club_heart"
message = b"hi brian"

def exor(v1, v2):
    a = np.frombuffer(v1, dtype = np.uint8)
    b = np.frombuffer(v2, dtype = np.uint8)
    re=(a^b).tobytes()
    return(re)

# Encrypt with hey 1 
key_bob = hashlib.shake_128(bob_passphrase)
ciphertext1 = exor(message, key_bob.digest(len(message)))

# Encrypt with key 2
key_alice = hashlib.shake_128(alice_passphrase)
ciphertext2 = exor(ciphertext1, key_alice.digest(len(message)))

# Decrypt with key 1 
intermediary = exor(ciphertext2, key_alice.digest(len(message)))

# Decrypt with key 2
final = exor(intermediary, key_bob.digest(len(message)))

print(final)
