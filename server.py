#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#
import random
import time
import zmq


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

counter = 0
timer = 0
while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message)

    #  Do some 'work'.
    #  Try reducing sleep time to 0.01 to see how blazingly fast it communicates
    #  In the real world usage, you just need to replace time.sleep() with
    #  whatever work you want python to do, maybe a machine learning task?
    time.sleep(1)
    #  Send reply back to client
    #  In the real world usage, after you finish your work, send your output here
    sendMessage = str(random.randint(0, 88)) + ", " + str(random.random()) + ", " + str(timer)
    timer = timer + 1
    socket.send_string(sendMessage)
