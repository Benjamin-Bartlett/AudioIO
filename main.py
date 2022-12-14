import pyaudio
import numpy as np
import time

p = pyaudio.PyAudio()

CHANNELS = 2
RATE = 44100
CHUNK = 2**4

def callback(in_data, frame_count, time_info, flag):
    # using Numpy to convert to array for processing
    audio_data = np.frombuffer(in_data, dtype=np.float32)
    x = 0
    for a in audio_data:
        a *= 1.1
        #print("asdf")
    print("------------------------ ")
    return audio_data, pyaudio.paContinue

stream = p.open(format=pyaudio.paFloat32,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                input=True,
                frames_per_buffer=CHUNK,
                stream_callback=callback)

stream.start_stream()

while stream.is_active():
    time.sleep(20)
    stream.stop_stream()
    print("Stream is stopped")

stream.close()
p.terminate()
