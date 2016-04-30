import pyaudio
import wave
import numpy as np
import base64

def FFT(frames):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    swidth = 2

    frames = base64.b64decode(frames)

    # using Blackman window
    window = np.blackman(CHUNK)
    print swidth
    print FORMAT
    print len(frames)
    print "--------"
    indata = np.array(wave.struct.unpack("%dh"%(len(frames)/swidth), frames))
    # taking FFT here
    fftData=abs(np.fft.rfft(indata))
    fftData = np.log10(fftData)*10
    fftData = list(fftData)[:10000]
    indata = list(indata)[:10000]

    return indata, fftData
