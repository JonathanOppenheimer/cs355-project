from common import *
from Crypto.Random import get_random_bytes
import random
import zmq


# Get a list of Bob's files
file_paths = get_file_paths("./bobs-code/")
print(file_paths)

# Create the list of file hashes for Bob's file
print("(1) Hashing files...")
hash_list = []
for file_path in file_paths:
    hash_list.append(calculate_ed2k_hash(file_path))

# Generate Bob's private key 
print("(2) Generating private key...")
bob_key = get_random_bytes(32) # 32 byte key for SHA-256 hashes

# Encrypt all of Bob's hashed files
print("(3) Encrypting file hashes...")
bob_message_bob_encryption = []
for hash in hash_list:
    bob_message_bob_encryption.append(exor(hash, bob_key))
random.shuffle(bob_message_bob_encryption) # Shuffle

# Set up connection with Alice
context = zmq.Context()
print("(4) Waiting for Alice's encryptions...")
socket = context.socket(zmq.REP)
socket.bind("tcp://*:8080")

# Recieve Alice's encryptions from Alice 
alice_message_alice_encryption = []
for i in range(5):
    alice_message_alice_encryption.append(socket.recv())
    socket.send_string(str(1)) # Confirm reciept 
assert(socket.recv_string() == "End of Alice encryptions.")
print(("(5) Encryptions recieved!"))

# Send Bob's encryptions to Alice 
print("(6) Sending encryptions to Alice...")
for index, encryption in enumerate(bob_message_bob_encryption, start=1):
    socket.send(encryption)
    assert(int(socket.recv_string()) == 1)
    print(f"Sent encryption #{index}")
socket.send_string("End of Bob encryptions.")

# Encrypt Alice's messages, encrypted with Alice's key with Bob's key
print("(7) Encrypting Alices's messages...")
ab_double_encryptions = [] # Alice's messages encrypted with Alice's key, then Bob's key
for encryption in alice_message_alice_encryption:
    ab_double_encryptions.append(exor(encryption, bob_key))
random.shuffle(ab_double_encryptions) # Shuffle

# Recieve double encryptions from Alice
ba_double_encryptions = [] # Bob's Mmssages encrypted with Bob's key, then Alice's key
for i in range(5):
    ba_double_encryptions.append(socket.recv())
    socket.send_string(str(1)) # Confirm reciept 
assert(socket.recv_string() == "End of double encryptions.")
print(("(8) Bob-Alice double encryptions recieved!"))

# Send double encryptions to Alice 
print("(9) Sending Alice-Bob double encryptions to Alice...")
for index, encryption in enumerate(ba_double_encryptions, start=1):
    socket.send(encryption)
    assert(int(socket.recv_string()) == 1)
    print(f"Sent double encryption #{index}")
socket.send_string("End of double encryptions.")
