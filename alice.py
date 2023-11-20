import math
import os
import random
import zmq

from common import read_text_files_from_folder
from cryptography.hazmat.primitives.asymmetric import rsa
from Crypto.Util import number




#  Socket to talk to Bob (the server)
context = zmq.Context()
print("Connecting to Bob...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:8080")

# Get Alice's files 
code_segments = read_text_files_from_folder("./alices-code/")

# Choose 2 large primes 
p = number.getPrime(1024, os.urandom)
q = number.getPrime(1024, os.urandom)

# Send each prime to Bob 
print("Sending primes to Bob...")
socket.send_string(str(p))
assert(int(socket.recv_string()) == 1)
socket.send_string(str(q))
assert(int(socket.recv_string()) == 1)

# Compute SRA components 

# Calculate n (modulus) and phi (Euler's totient function)
n = p * q
phi = (p - 1) * (q - 1)

# Generate a random public exponent (e) such that 1 < e < phi and e is coprime with phi
e = random.randint(2, n)
while math.gcd(e, phi) != 1:
    e = random.randint(2, phi - 1)

# Calculate the private exponent (d) using the modular inverse of e mod phi
d = pow(e, -1, phi)

print(e)
print(d)

# Iterate through each code segment and send the transformed segment to Bob
# for i, code_file in enumerate(code_segments):
    
#     print("Sending code segment %d to Bob" % i)
#     socket.send(code_file)

#     #  Get the reply.
#     message = socket.recv()
#     print("Received reply for #%d [ %s ]" % (i, message))
