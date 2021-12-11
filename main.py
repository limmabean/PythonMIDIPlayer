import random
import time
import mido
import zmq
import threading
from mido import MidiFile
import glob

midi_index_lock = threading.Lock()
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
counter = 0
timer = 0
drum_files = []
note_files = []
drum_mid = []
note_mid = []
midi_index = 0


def unity_server():
    while True:
        #  Wait for next request from client
        message = socket.recv()
        print("Received request: %s" % message)
        #  Do some 'work'.
        # Eventually this will be controlled by something not random. Instead based on input from the Unity Server
        midi_index_lock.acquire()
        global midi_index
        midi_index = random.randint(0, 50)
        midi_index_lock.release()
        #  Send reply back to client
        #  In the real world usage, after you finish your work, send your output here
        send_message = str(random.randint(0, 88)) + ", " + str(random.random()) + ", " + str(timer)
        timer = timer + 1
        socket.send_string(send_message)


def midi_out(port_name):
    global midi_index
    # Import track details
    with mido.open_output(port_name, virtual=True) as outport:
        while True:
            if port_name == "NOTES":
                print("Playing file: " + note_files[midi_index % len(note_files)])
                for msg in note_mid[midi_index % len(note_mid)].play():
                    outport.send(msg)
                midi_index_lock.acquire()
                # Eventually this will be controlled by something not random
                midi_index = random.randint(0, 50)
                midi_index_lock.release()
            elif port_name == "DRUMS":
                print("Playing file: " + drum_files[midi_index % len(drum_files)])
                for msg in drum_mid[midi_index % len(drum_mid)].play():
                    outport.send(msg)
                midi_index_lock.acquire()
                # Eventually this will be controlled by something not random
                midi_index = random.randint(0, 50)
                midi_index_lock.release()


class MyThread(threading.Thread):
    def __init__(self, thread_id, name, thread_type):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.thread_type = thread_type

    def run(self):
        print("Starting " + self.name + " thread" + "\n")
        if self.thread_type == "MIDI":
            midi_out(self.name)
        elif self.thread_type == "SERVER":
            unity_server()
        print("Exiting " + self.name + "\n")


if __name__ == '__main__':
    print("Creating threads and lock...")
    notes_thread = MyThread(1, "NOTES", "MIDI")
    drums_thread = MyThread(2, "DRUMS", "MIDI")
    unity_server_thread = MyThread(3, "UNITY_SERVER", "SERVER")

    print("Setting random seed...")
    random.seed()

    print("Loading midi files...")
    for file in glob.glob("./midi/drums/*.mid"):
        drum_files.append(file)
    for file in glob.glob("./midi/notes/*.mid"):
        note_files.append(file)

    for file in drum_files:
        drum_mid.append(MidiFile(file, clip=True))
    for file in note_files:
        note_mid.append(MidiFile(file, clip=True))
    print("Midi files loaded.")

    notes_thread.start()
    drums_thread.start()
    unity_server_thread.start()
