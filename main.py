import random
import pyaudio
import numpy as np
import time
import matplotlib.pyplot as plt

RATE =48000
CHUNK=2**12
width = 2


# creating a list that stores the x values
xList = []
i = 0
for i in range(CHUNK):
    xList.append(i)

# create the figure
fig, ax = plt.subplots()
ln, = ax.plot([], [])

plt.xlim(0, CHUNK)
plt.ylim(-1, 1)

def displayGraph(samples):
    x = xList
    y = samples
    ln.set_data(x, y)
    print("Asdf")
    plt.pause(0.1)


p = pyaudio.PyAudio()

# callback function to stream audio, another thread.
def callback(in_data,frame_count, time_info, status):
    audio = np.frombuffer(in_data)
    return (audio, pyaudio.paContinue)

#create a pyaudio object
inStream = p.open(format = p.get_format_from_width(width, unsigned=False),
                       channels=1,
                       rate=RATE,
                       input=True,
                       frames_per_buffer=CHUNK,
                       stream_callback = callback)

"""
Setting up the array that will handle the timeseries of audio data from our input
"""
audio = np.empty((CHUNK),dtype="float")
inStream.start_stream()

while True:
    x = 0

#while True:
#  try:
#      time.sleep(.1)
#      #displayGraph(gSample)

#  except KeyboardInterrupt:

#    inStream.stop_stream()
#    inStream.close()
#    p.terminate()
#    print("* Killed Process")
#    quit()


