import pyaudio
import numpy as np
import wave
import sounddevice as sd
import soundfile as sf
from tkinter import *
import matplotlib.pyplot as plt
from pydub import AudioSegment
from pydub.playback import play
import time


#Helpful variables
CHANNELS = 1
RATE = 44100
CHUNK = 800


#***********
# Records audio for a given number of seconds from output stream
# Writes data onto a wav file called recoding.wav
#***********
def record():
    seconds = int(input("How many seconds would you like to record for"))
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt32,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    input=True,
                    frames_per_buffer=CHUNK,)
                    #stream_callback=callback)

    seconds = seconds
    frames = []
    soundscale = 1
    print("Recording")
    for i in range(0, int(RATE/CHUNK*seconds)):#keeps reading data for specified amount of seconds
        data = stream.read(CHUNK)
        for d in data: #adds data collected to an array for future use
            d *= 0
            soundscale+=5
        frames.append(data)


    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Recording Stopped")


    #writes data to file
    sFile = wave.open('recoding.wav','wb')
    sFile.setnchannels(CHANNELS)
    sFile.setsampwidth(p.get_sample_size(pyaudio.paInt32))

    sFile.setframerate(RATE)
    sFile.writeframes(b''.join(frames))
    sFile.close()

#***********
# Plays recoding.wav
# Plays edited sound based on original recording as all edits can recast to recoding
#***********
def play():
    data, fs = sf.read('recoding.wav', dtype='float32')
    sd.play(data, fs)
    status = sd.wait()

#***********
# Takes a segment of recording
# Casts that segment onto original recording file
#***********
def cut():
   cutting = "y"
   while(cutting == "y"): #allows users to not affect original file in order to retrim
    start = (int)(input("Start millisecond"))
    end = (int)(input("Ending millisecond"))

    sound = AudioSegment.from_wav("recoding.wav")
    extract = sound[start:end]
    extract.export("cutsound.wav", format="wav")

    data, fs = sf.read('cutsound.wav', dtype = 'float32')
    sd.play(data, fs)
    status = sd.wait()
    cutting=input("Type y to cut again anything else to stop trimming")
   extract.export("recoding.wav", format="wav")

#***********
# Produces a wave graph of the sound
#***********
def waveGraph():
    file = wave.open('recoding.wav', 'rb')
    sample_freq = file.getframerate()
    frames = file.getnframes()
    signal_wave = file.readframes(-1)
    file.close()

    time = frames / sample_freq

    audio_array = np.frombuffer(signal_wave, dtype=np.int32)
    times = np.linspace(0, time, num=frames)

    plt.figure(figsize=(15, 5))
    plt.plot(times, audio_array)
    plt.ylabel('Signal Wave')
    plt.xlabel('Time(s)')
    plt.xlim(0, time)
    plt.title('Sound')
    plt.show()

#***********
# Produces a frequency graph of the sound
#***********
def frequencyGraph():
    file = wave.open('recoding.wav', 'rb')
    sample_freq = file.getframerate()
    frames = file.getnframes()
    signal_wave = file.readframes(-1)
    file.close()

    time = frames / sample_freq

    audio_array = np.frombuffer(signal_wave, dtype=np.int32)
    times = np.linspace(0, time, num=frames)

    plt.figure(figsize=(15, 5))
    plt.specgram(audio_array, Fs=sample_freq)
    plt.title('Left Channel')
    plt.ylabel('Frequency (Hz)')
    plt.xlabel('Time (s)')
    plt.xlim(0, time)
    plt.colorbar()
    plt.show()
#***********
# Changes the pitch by a user entered amount of octaves
# Does not retain same time scale
#***********
def pitchChanger():
    changingSound="y"
    while(changingSound == "y"):#allows user to not affect original recording so they can repitch shift
        sound = AudioSegment.from_wav("recoding.wav")
        octaves = float(input("How many ocatave would you like to change(+ or -)"))
        new_sample_rate = int (sound.frame_rate * (2.0 ** octaves))
        changedSound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
        changedSound = changedSound.set_frame_rate(44100)
        changedSound.export("changedsound.wav", format = "wav")
        data, fs = sf.read('changedsound.wav', dtype='float32')
        sd.play(data, fs)
        status = sd.wait()
        changingSound=input("Type y to change pitch again anything else to stop")
    changedSound.export("recoding.wav", format = "wav")
#***********
# Changes the volume by a user entered amount of octaves
#***********
def changeVolume():
    changingSound = "y"
    while (changingSound == "y"):#allows user to not affect original recording so they can revolume shift
        volumeChange = int(input("How much would you like to change volume by + or -"))
        sound = AudioSegment.from_wav("recoding.wav")
        changedSound = sound + volumeChange
        changedSound.export("changedsound.wav", format="wav")
        data, fs = sf.read('changedsound.wav', dtype='float32')
        sd.play(data, fs)
        status = sd.wait()
        changingSound = input("Type y to change volume again anything else to stop")
    changedSound.export("recoding.wav", format="wav")
#***********
# Plays recording a user entered amount of times
#***********
def playLoop():
    loops = int(input("How many times would you like to loop"))
    for i in range(0,loops):
        play()
#***********
# An effect that quiets the begining and end of recording
# User inputs how long they want quiet
#***********
def glideSound():
    glide=int(input("How many milliseconds would you like quiet? Effect may not work properly if you select more than half of recording time"))
    start = 0
    end = glide

    sound = AudioSegment.from_wav("recoding.wav")
    firsthalf = sound[start:end]
    firsthalf = firsthalf - 10

    file = wave.open('recoding.wav', 'rb')
    sample_freq = file.getframerate()
    rate = file.getnframes()
    seconds = sample_freq/float(rate)

    start = glide+3
    end = seconds-glide

    middlehalf = sound[start:end]

    start = seconds-glide+3
    end = seconds-5

    secondhalf = sound[start:end]
    secondhalf = secondhalf - 10

    newSound = firsthalf + middlehalf + secondhalf
    newSound.export("changedsound.wav", format="wav")
    data, fs = sf.read('changedsound.wav', dtype='float32')
    sd.play(data, fs)
    status = sd.wait()
    safe = input("type y to save effect anything else to not")
    if safe == "y": #allows user to save the effect
        newSound.export("recoding.wav", format="wav")
#***********
# An effect that provides an echo
#***********
def echo():
    file = wave.open('recoding.wav', 'rb')
    sample_freq = file.getframerate()
    rate = file.getnframes()
    seconds = sample_freq / float(rate)

    sound = AudioSegment.from_wav("recoding.wav")
    sound2 = AudioSegment.from_wav("recoding.wav")
    sound3 = sound[seconds-999:seconds-1]
    sound - 20
    overlay = sound.overlay(sound2, position = 1000) + sound3
    overlay.export("changedsound.wav", format="wav")
    data, fs = sf.read('changedsound.wav', dtype='float32')
    sd.play(data, fs)
    status = sd.wait()
    safe=input("type y to save effect anything else to not")
    if safe == "y": #allows user to save effect
        overlay.export("recoding.wav", format="wav")

#***********
# Exporrts the file to an Mp3
#***********
def export():
    name = input("What would you like to call you're file")
    sound = AudioSegment.from_wav("recoding.wav")
    sound.export(name+".mp3", format="mp3")

#***********
# Menu allowing for better user experience
#***********
window = Tk()
window.title("Music Editor")
window.configure(background="white")
Label(window, text="What would you like to do?", bg="white", fg= "black",font ="none 12 bold").grid(row=1,column = 0,sticky=W)
Label(window, text="Please record something before using other functions", bg="white", fg= "black",font ="none 12 bold").grid(row=2,column = 0,sticky=W)
Button(window,text="Record",width=6,command = record).grid(row=3,column=0,sticky=W)
Button(window,text="Play",width=6,command = play).grid(row=4,column=0,sticky=W)
Button(window,text="Play looped",width=14,command = playLoop).grid(row=5,column=0,sticky=W)

Label(window, text="Edit", bg="white", fg= "black",font ="none 12 bold").grid(row=6,column = 0,sticky=W)
Button(window,text="Change Volume",width=14,command = changeVolume).grid(row=7,column=0,sticky=W)
Button(window,text="Cut",width=6,command = cut).grid(row=8,column=0,sticky=W)
Button(window,text="Change Pitch",width=14,command = pitchChanger).grid(row=9,column=0,sticky=W)

Label(window, text="Effects", bg="white", fg= "black",font ="none 12 bold").grid(row=10,column = 0,sticky=W)
Button(window,text="Glide Effect",width=14,command = glideSound).grid(row=11,column=0,sticky=W)
Button(window,text="Echo Effect",width=14,command = echo).grid(row=12,column=0,sticky=W)

Label(window, text="Miscellaneous", bg="white", fg= "black",font ="none 12 bold").grid(row=13,column = 0,sticky=W)
Button(window,text="Wave Graph",width=10,command = waveGraph).grid(row=14,column=0,sticky=W)
Button(window,text="Frequency Graph",width=14,command = frequencyGraph).grid(row=15,column=0,sticky=W)
Button(window,text="Export to Mp3",width=14,command = export).grid(row=16,column=0,sticky=W)
window.mainloop()
