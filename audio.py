import pyaudio
import wave
import time

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

    def getFrames(self):
        """ Getter """
        return self.frames


if __name__ == "__main__":
    """ Testing the Audio class """
    audio = Audio(10)
    audio.open_mic()
    audio.record(1)
    audio.record(2)
    audio.write_to_wav("test1.wav",1)
    audio.write_to_wav("test2.wav",2)
    audio.close_mic()
