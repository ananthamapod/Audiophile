import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt

class Audio(object):
    """ Audio class for interacting with microphone, stores recordings
    from each coordinate, supports writing frames to file """

    def __init__(self, record_seconds=5):
        """ Set up parameters for recording """
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.RECORD_SECONDS = record_seconds
        self.mic = None
        self.frames = {}

    def open_mic(self):
        """ Create a PyAudio instance for recording """
        try:
            self.mic = pyaudio.PyAudio()
            if not self.mic:
                raise Exception("Failed to open mic")
            return True
        except Exception as e:
            print str(e)
            return False

    def record(self, coordinates):
        """ Records for amount of time set when creating,
        saves PCM frames in separate bucket corresponding to coordinates """
        self.frames[coordinates] = []
        stream = self.mic.open(format=self.FORMAT,
                    channels=self.CHANNELS,
                    rate=self.RATE,
                    input=True,
                    frames_per_buffer=self.CHUNK)

        print("* recording")

        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            self.frames[coordinates].append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()

    def close_mic(self):
        """ Terminates the PyAudio instance """
        try:
            self.mic.terminate()
            return True
        except Exception as e:
            print str(e)
            return False

    def write_to_wav(self, output_filename, coords):
        """ Writes coordinates' frames to .wav file """
        frames = self.frames.get(coords)
        if frames:
            wf = wave.open(output_filename, 'wb')
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.mic.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            return True
        else:
            print "No recordings exist for those coordinates"
            return False

    def get_frames(self):
        """ Getter """
        return self.frames

    def analyze_frames(self, coords, calibration_coords=None):
        frames = self.frames.get(coords)
        if not frames:
            print "No recodings exist for those coordinates"
        else:
            # using Blackman window
            window = np.blackman(self.CHUNK)
            swidth = self.mic.get_sample_size(self.FORMAT)
            frames = b''.join(frames)
            indata = np.array(wave.struct.unpack("%dh"%(len(frames)/swidth), frames))
            # taking FFT here
            fftData=abs(np.fft.rfft(indata))

            fig = plt.figure()
            timeSeries = None
            frequencySeries = None
            timeSeries = fig.add_subplot(211)
            frequencySeries = fig.add_subplot(212)
            x = range(len(indata))
            timeSeries.plot(x, indata)

            x = range(len(fftData))
            frequencySeries.plot(x, fftData)

            plt.grid(True)
            fig.canvas.set_window_title('Coords:' + str(coords))
            fig.canvas.show()
            plt.show(block=True)

            if calibration_coords:
                fig = plt.figure()
                corrected_timeSeries = fig.add_subplot(211)
                corrected_frequencySeries = fig.add_subplot(212)
                calib_frames = self.frames.get(calibration_coords)
                calib_frames = b''.join(calib_frames)
                calib_indata = np.array(wave.struct.unpack("%dh"%(len(calib_frames)/swidth), calib_frames))
                corrected_indata = indata - calib_indata
                fftData=abs(np.fft.rfft(corrected_indata))
                x = range(len(indata))
                corrected_timeSeries.plot(x, corrected_indata)

                x = range(len(fftData))
                corrected_frequencySeries.plot(x, fftData)
                plt.grid(True)
                fig.canvas.set_window_title(str(coords)+ ' Calibrated with ' + str(calibration_coords))
                fig.canvas.show()
                plt.show(block=True)
                wf = wave.open("test3.wav", 'wb')
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(self.mic.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                print len(frames)/swidth
                print len(calib_frames)/swidth
                indata = wave.struct.pack("%dh"%(len(frames)/swidth), indata)
                wf.writeframes(indata)
                wf.close()

if __name__ == "__main__":
    """ Testing the Audio class """
    import time
    audio = Audio(4)
    audio.open_mic()
    tmp = raw_input("")
    for i in range(1,11):
        print("3")
        time.sleep(0.5)
        print("2")
        time.sleep(0.5)
        print("1")
        time.sleep(0.5)
        audio.record(i)

    audio.write_to_wav("test1.wav",1)
    audio.write_to_wav("test2.wav",2)
    for i in range(1,11):
        audio.analyze_frames(i)
    audio.close_mic()
