import time
import mido
import rtmidi
import keyboard
from collections import deque
from mido import MidiFile
from rtmidi.midiconstants import NOTE_ON, NOTE_OFF

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Import track details
    mid = MidiFile('generated3.mid', clip=True)
    note_track = mid.tracks[1]
    meta_track = mid.tracks[0]

    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()

    midi_in = mido.get_input_names()  # To list the input ports
    print(midi_in)

    if available_ports:
        midiout.open_port(0)
    else:
        print("Opening virtual port: MVGMUSIC")
        midiout.open_virtual_port("MVGMUSIC")

    with midiout:
        while(True):
            for message in note_track:
                if hasattr(message, 'note'):
                    midiout.send_message([NOTE_ON, message.note, message.velocity])
                    time.sleep(message.time / 500)
                    midiout.send_message([NOTE_OFF, message.note, message.velocity])

    del midiout



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
