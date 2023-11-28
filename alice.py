from common import *
from Crypto.Random import get_random_bytes
import random
import zmq


# Get a list of Alice's files
file_paths = get_file_paths("./alices-code/")
print(file_paths)

# Create the list of file hashes for Alice's file
print("(1) Hashing files...")
hash_list = []
for file_path in file_paths:
    hash_list.append(calculate_ed2k_hash(file_path))

# Generate Alice's private key 
print("(2) Generating private key...")
alice_key = get_random_bytes(32) # 32 byte key for SHA-256 hashes

# Encrypt all of Alice's hashed files
print("(3) Encrypting file hashes...")
alice_message_alice_encryption = []
for hash in hash_list:
    alice_message_alice_encryption.append(exor(hash, alice_key))
random.shuffle(alice_message_alice_encryption) # Shuffle

# Set up connection with Bob
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:8080")

# Send Alice's encryptions to Bob 
print("(4) Sending encryptions to Bob...")
for index, encryption in enumerate(alice_message_alice_encryption, start=1):
    socket.send(encryption)
    assert(int(socket.recv_string()) == 1)
    print(f"Sent encryption #{index}")
socket.send_string("End of Alice encryptions.")

# Recieve Bob's encryptions from Bob 
print("(5) Waiting for Bob's encryptions...")
bob_message_bob_encryption = []
for i in range(5):
    bob_message_bob_encryption.append(socket.recv())
    socket.send_string(str(1)) # Confirm reciept 
assert(socket.recv_string() == "End of Bob encryptions.")
print(("(6) Encryptions recieved!"))

# Encrypt Bob's messages, encrypted with Bob's key with Alice's key
print("(7) Encrypting Bob's messages...")
ba_double_encryptions = [] # Bob's Mmssages encrypted with Bob's key, then Alice's key
for encryption in bob_message_bob_encryption:
    ba_double_encryptions.append(exor(encryption, alice_key))
random.shuffle(ba_double_encryptions) # Shuffle

# Send double encryptions to Bob 
print("(8) Sending Bob-Alice double encryptions to Bob...")
for index, encryption in enumerate(ba_double_encryptions, start=1):
    socket.send(encryption)
    assert(int(socket.recv_string()) == 1)
    print(f"Sent double encryption #{index}")
socket.send_string("End of double encryptions.")

# Recieve double encryptions from Bob
ab_double_encryptions = [] # Alice's messages encrypted with Alice's key, then Bob's key
for i in range(5):
    ab_double_encryptions.append(socket.recv())
    socket.send_string(str(1)) # Confirm reciept 
assert(socket.recv_string() == "End of double encryptions.")
print(("(9) Alice-Bob double encryptions recieved!"))

# Decrypt Alice's messages encrypted by Alice then Bob with Alice's Key
print("(10) Decrypting Alice-Bob double encryptions with Alice's key...")
alice_message_bob_encryption = []
for encryption in ab_double_encryptions:
    alice_message_bob_encryption.append(exor(encryption, alice_key))

# Compute the intersection between Alice's messages encrypted with Bob's key, and Bob's messages encrypted with Bob's key
print("(11) Computing cardinality of the intersection...")
cardinality = len(set(alice_message_bob_encryption).intersection(set(bob_message_bob_encryption)))
print(f"Alice and Bob have {cardinality} code segments in common.")
