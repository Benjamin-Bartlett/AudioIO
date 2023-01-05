import pyaudio
import numpy as np
import wave
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
import time










p = pyaudio.PyAudio()
CHANNELS = 1
RATE = 44100
CHUNK = 800

#def callback(in_data, frame_count, time_info, flag):
    # using Numpy to convert to array for processing
    #audio_data = np.frombuffer(in_data, dtype=np.float32)
    #x = 0
    #for a in audio_data:
       # a *= 1.1
        #print("asdf")
    #print("------------------------ ")
    #return audio_data, pyaudio.paContinue

stream = p.open(format=pyaudio.paInt32,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                input=True,
                frames_per_buffer=CHUNK,)
                #stream_callback=callback)
#testing
seconds = 5
#stream.start_stream()
frames = []
secondTack = 0
secondCount = 0
for i in range(0, int(RATE/CHUNK*seconds)):
    data = stream.read(CHUNK)
    for d in data:
        d *= 5
    frames.append(data)

#while stream.is_active():
    #time.sleep(20)
    #stream.stop_stream()
    #print("Stream is stopped")
stream.stop_stream()
stream.close()
p.terminate()

sFile = wave.open('recoding.wav','wb')
sFile.setnchannels(CHANNELS)
sFile.setsampwidth(p.get_sample_size(pyaudio.paInt32))

sFile.setframerate(RATE)
sFile.writeframes(b''.join(frames))
sFile.close()

data, fs = sf.read('recoding.wav', dtype = 'float32')
sd.play(data, fs)
status = sd.wait()

file = wave.open('recoding.wav','rb')
sample_freq = file.getframerate()
frames = file.getnframes()
signal_wave = file.readframes(-1)
file.close()

time = frames / sample_freq

audio_array = np.frombuffer(signal_wave, dtype = np.int32)
times = np.linspace(0, time, num=frames)

showinggraph = True
while showinggraph:
    graph = str(input("Which graph do you want to see, w or s? 'Close' to terminate"))
    if graph.lower() == "close":
        break;
    if graph.lower() == "w":
        plt.figure(figsize=(15,5))
        plt.plot(times,audio_array)
        plt.ylabel('Signal Wave')
        plt.xlabel('Time(s)')
        plt.xlim(0,time)
        plt.title('Sound')
        plt.show()

    if graph.lower() == "s":
        plt.figure(figsize=(15, 5))
        plt.specgram(audio_array, Fs=sample_freq)
        plt.title('Left Channel')
        plt.ylabel('Frequency (Hz)')
        plt.xlabel('Time (s)')
        plt.xlim(0, time)
        plt.colorbar()
        plt.show()
