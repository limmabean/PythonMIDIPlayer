import random
import time
import mido
import zmq
import threading
from mido import MidiFile
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
counter = 0
timer = 0


def unity_server():
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
        send_message = str(random.randint(0, 88)) + ", " + str(random.random()) + ", " + str(timer)
        timer = timer + 1
        socket.send_string(send_message)


def midi_out(port_name):
    # Import track details
    with mido.open_output(port_name, virtual=True) as outport:
        mid = []
        if (port_name=="NOTES"):
            mid = MidiFile('midi/notes/generated.mid', clip=True)
        else:
            mid = MidiFile('midi/drums/2021-12-07_041432_01.mid', clip=True)
        while True:
            for msg in mid.play():
                outport.send(msg)


class myThread(threading.Thread):
    def __init__(self, threadID, name, counter, type):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.type = type

    def run(self):
        print("Starting " + self.name + "\n")
        if self.type == "MIDI":
            midi_out(self.name)
        elif self.type == "SERVER":
            unity_server()
        print("Exiting " + self.name + "\n")


if __name__ == '__main__':
    thread1 = myThread(1, "NOTES", 1, "MIDI")
    thread2 = myThread(2, "DRUMS", 2, "MIDI")
    thread3 = myThread(3, "UNITY_SERVER", 3, "SERVER")

    thread1.start()
    thread2.start()
    thread3.start()

