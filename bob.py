import math
import random
import sys
import zmq

from common import read_text_files_from_folder
from common import power_mod_n
from cryptography.hazmat.primitives.asymmetric import rsa



# Set up connection 
context = zmq.Context()
print("Waiting for Alice...")
socket = context.socket(zmq.REP)
socket.bind("tcp://*:8080")

# Get Bob's files 
code_segments = read_text_files_from_folder("./bobs-code/")

# Recieve primes from Alice 
p = int(socket.recv_string())
socket.send_string(str(1)) # Confirm reciept 
q = int(socket.recv_string())
socket.send_string(str(1))  # Confirm reciept 
print("Recieved Alice's primes!")

# Generate SRA components 

# Calculate n (modulus) and phi (Euler's totient function)
n = p * q
phi = (p - 1) * (q - 1)

# Generate a random public exponent (e) such that 1 < e < phi and e is coprime with phi
e = random.randint(2, phi - 1)
while math.gcd(e, phi) != 1:
    e = random.randint(2, phi - 1)

# Calculate the private exponent (d) using the modular inverse of e mod phi
d = pow(e, -1, phi)

# print(e)
# print(d)

sys.setrecursionlimit(5000) # if your computer can't handle this skill issue 
print(power_mod_n(e,d,n))

# while True:
#     #  Wait for next request from client
#     message = socket.recv()
#     print("Received request: %s" % message)

#     #  Do some 'work'
#     time.sleep(1)

#     #  Send reply back to client
#     socket.send(b"World")