import pyaudio
import wave
import time
import serial

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

frames = []

mic = None
ser = None

def open_mic():
    return pyaudio.PyAudio()

def record(p):
    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

    print("* recording")

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()

def close_mic(p):
    p.terminate()
    return True

def write_to_wav(p):
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def setup():
    global mic
    global ser
    mic = open_mic()
    #ser = serial.Serial('/dev/tty.usbserial', 9600)
    #ser.readline()
    #ser.write(b'Hello')

setup()
record(mic)
time.sleep(5)
record(mic)
close_mic(mic)
write_to_wav(mic)
