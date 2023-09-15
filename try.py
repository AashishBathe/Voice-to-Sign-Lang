import tkinter as tk
import pyaudio
import threading
import speech_recognition as sr

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

audio = pyaudio.PyAudio()
frames = []

def start_recording():
    global frames
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Recording started...")
    while True:
        data = stream.read(CHUNK)
        frames.append(data)

        if start_button['state'] == 'normal':
            break

    print("Recording stopped...")
    stream.stop_stream()
    stream.close()

    # Convert the list of frames to a bytes object
    audio_bytes = b''.join(frames)

    # Create an instance of AudioData from the byte data
    audio_data = sr.AudioData(audio_bytes, RATE, CHANNELS)

    # Create a recognizer object
    recognizer = sr.Recognizer()

    # Recognize the speech in the audio data using Google Speech Recognition
    try:
        text = recognizer.recognize_google(audio_data)
        print("Google Speech Recognition thinks you said: " + text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def stop_recording():
    start_button['state'] = 'normal'
    stop_button['state'] = 'disabled'

def start_thread():
    global t
    t = threading.Thread(target=start_recording)
    t.start()

root = tk.Tk()

start_button = tk.Button(root, text="Start Recording", command=lambda: [start_thread(), start_button.config(state='disabled'), stop_button.config(state='normal')])
stop_button = tk.Button(root, text="Stop Recording", command=stop_recording, state='disabled')

start_button.pack()
stop_button.pack()

root.mainloop()

audio.terminate()
