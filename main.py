import mido
import time
import pyautogui
import keyboard

inputs = mido.get_input_names()

if not inputs:
    print("No MIDI input devices found")
    exit()

print("Using:", inputs[0])

# Avoid overwriting built-in name "letters"
key_layout = "Z1X2CV3B4N5MA6S7DF8G9H0JQIWOERPT[Y]U"

NOTE_TO_KEY = {}
start_note = 48  # C2

for i, key in enumerate(key_layout):
    NOTE_TO_KEY[start_note + i] = key.lower()  # keyboard prefers lowercase for letters

held_notes = set()

with mido.open_input(inputs[0]) as port:
    print("Listening... press keys (Ctrl+C to stop)")

    try:
        while True:
            for msg in port.iter_pending():

                # NOTE ON (key press)
                if msg.type == "note_on" and msg.velocity > 0:
                    note = msg.note

                    if note in NOTE_TO_KEY and note not in held_notes:
                        key = NOTE_TO_KEY[note]
                        held_notes.add(note)

                        print(f"DOWN: {key}")
                        # pyautogui.keyDown(key)
                        keyboard.press(key)

                # NOTE OFF (key release)
                elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
                    note = msg.note

                    if note in NOTE_TO_KEY and note in held_notes:
                        key = NOTE_TO_KEY[note]
                        held_notes.remove(note)

                        print(f"UP: {key}")
                        # pyautogui.keyUp(key)
                        keyboard.release(key)

            time.sleep(0.005)

    except KeyboardInterrupt:
        print("\nStopping... releasing all keys")

        # safety: release anything still held
        for note in list(held_notes):
            key = NOTE_TO_KEY.get(note)
            if key:
                # pyautogui.keyUp(key)
                keyboard.release(key)

        print("Stopped cleanly.")