import mido
import zmq
import threading
from mido import MidiFile
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
counter = 0
timer = 0


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
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name + "\n")
        midi_out(self.name)
        print("Exiting " + self.name + "\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    thread1 = myThread(1, "NOTES", 1)
    thread2 = myThread(2, "DRUMS", 2)

    thread1.start()
    thread2.start()




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
