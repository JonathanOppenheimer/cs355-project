import zmq

from common import read_text_files_from_folder



#  Socket to talk to Bob (the server)
context = zmq.Context()
print("Connecting to Bob...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# Get Alice's files 
code_segments = read_text_files_from_folder("./alices-code/")

# Iterate through each code segment and send the transformed segment to Bob
for i, code_file in enumerate(code_segments):
    
    print("Sending code segment %d to Bob" % i)
    socket.send(code_file)

    #  Get the reply.
    message = socket.recv()
    print("Received reply for #%d [ %s ]" % (i, message))
