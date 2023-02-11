import ggwave
import numpy as np
import sounddevice as sd
import inspect
from gtts import gTTS
import audio2numpy as a2n
import os
import librosa



devices = sd.query_devices()
print(devices)

os.system("rm *.mp3")

deviceID = 13

# outputText = "this is a very long string of text and I want to see how it's broken up so this is a very long string of text and I want to see how it's broken up so this is a very long string of text and I want to see how it's broken up so this is a very long string of text and I want to see how it's broken up so "
outputText = "hi, my name is lauria. what's your name?"

stream = sd.OutputStream(dtype='float32', device=deviceID, channels=2, samplerate=48000)

stream.start()


ggwaveWaveform = ggwave.encode(outputText, protocolId = 4, volume = 80)
ggwaveOut = np.frombuffer(ggwaveWaveform, 'float32')

ttsWaveform = gTTS(outputText)
ttsWaveform.save('hello.mp3')

os.system("ffmpeg -hide_banner -loglevel error -i hello.mp3 -ar 48000 hello_48k.mp3")
ttsOut, sampleRate = a2n.open_audio('hello_48k.mp3')

# librosa doesn't work on Pis
ttsOut = librosa.effects.pitch_shift(ttsOut, sr=48000, n_steps=40)
# ttsOut = librosa.effects.pitch_shift(ttsOut, sr=48000, n_steps=-30)
# ttsOut = librosa.effects.time_stretch(ttsOut, rate=0.25)


ttsOut32 = np.frombuffer(ttsOut, 'float32')
print(sampleRate)
# print(type(signal32))
# print(signal32.shape)

print(len(ttsOut32), len(ggwaveOut))
if len(ttsOut32) > len(ggwaveOut):
    ttsOut32 = ttsOut32[0:len(ggwaveOut)]
else:
    zeroArray = np.zeros(len(ggwaveOut) - len(ttsOut32), dtype=np.float32)
    ttsOut32 = np.append(ttsOut32, zeroArray)


finalOutput = [ttsOut32, ggwaveOut]

aa = np.array(finalOutput)
a = np.ascontiguousarray(aa.T)
print(a.shape)


stream.write(a)

stream.stop()
stream.close()




# parameters:
#  int payloadLength
#  float sampleRateInp
#  float sampleRateOut
#  float sampleRate
#  int samplesPerFrame
#  float soundMarkerThreshold
#  ggwave_SampleFormat sampleFormatInp
#  ggwave_SampleFormat sampleFormatOut
#  int operatingMode

# paramsFL = {'payloadLength': 64, 'sampleRateInp': 48000.0, 'sampleRateOut': 48000.0, 'sampleRate': 48000.0, 'samplesPerFrame': 1024, 'soundMarkerThreshold': 3.0, 'sampleFormatInp': 5, 'sampleFormatOut': 5, 'operatingMode': 6}
# params = {'payloadLength': -1, 'sampleRateInp': 48000.0, 'sampleRateOut': 48000.0, 'sampleRate': 48000.0, 'samplesPerFrame': 1024, 'soundMarkerThreshold': 3.0, 'sampleFormatInp': 5, 'sampleFormatOut': 5, 'operatingMode': 6}