import time
import zmq

from common import read_text_files_from_folder


# Set up connection 
context = zmq.Context()
print("Waiting for Alice...")
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

# Get Bob's files 
code_segments = read_text_files_from_folder("./bobs-code/")

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message)

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    socket.send(b"World")