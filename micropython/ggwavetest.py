
import ggwave
import pyaudio
# import pprint

# p = pyaudio.PyAudio()

# generate audio waveform for string "hello python"
waveform = ggwave.encode("hello python", protocolId = 1, volume = 20)

print(type(waveform))

with open("testwave.raw", "wb") as file:
    file.write(waveform)

print("Transmitting text 'hello python' ...")
# stream = p.open(format=pyaudio.paFloat32, channels=1, rate=48000, output=True, frames_per_buffer=4096)
# stream.write(waveform, len(waveform)//4)
# stream.stop_stream()
# stream.close()

# p.terminate()