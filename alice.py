import os
import zmq

from common import read_text_files_from_folder
from Crypto.Util import number


#  Socket to talk to Bob (the server)
context = zmq.Context()
print("Connecting to Bob...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:8080")

# Get Alice's files 
code_segments = read_text_files_from_folder("./alices-code/")

# Choose 2 large primes 
prime_one = number.getPrime(1024, os.urandom)
prime_two = number.getPrime(1024, os.urandom)

# Send each prime to Bob 
print("Sending primes to Bob...")
socket.send_string(str(prime_one))
assert(int(socket.recv_string()) == 1)
socket.send_string(str(prime_two))
assert(int(socket.recv_string()) == 1)


# Iterate through each code segment and send the transformed segment to Bob
# for i, code_file in enumerate(code_segments):
    
#     print("Sending code segment %d to Bob" % i)
#     socket.send(code_file)

#     #  Get the reply.
#     message = socket.recv()
#     print("Received reply for #%d [ %s ]" % (i, message))
