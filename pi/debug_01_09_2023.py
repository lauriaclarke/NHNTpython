
import pyaudio
import wave

chunk = 1024      # Each chunk will consist of 1024 samples
sample_format = pyaudio.paInt16      # 16 bits per sample
channels = 1      # Number of audio channels
fs = 44100        # Record at 44100 samples per second
time_in_seconds = 3
filename = "soundsample.wav"

p = pyaudio.PyAudio()  # Create an interface to PortAudio

print('-----NowRecording-----')

#Opena Stream with the values we just defined
stream = p.open(format=sample_format, input_device_index=0, channels=channels, rate= fs, frames_per_buffer= chunk, input= True)

frames = []  # Initialize array to store frames

#Store data in chunks for 3 seconds
for i in range(0, int(fs / chunk * time_in_seconds)):
    data = stream.read(chunk)
    frames.append(data)

#Stop and close the Stream and PyAudio
stream.stop_stream()
stream.close()
p.terminate()

print('-----FinishedRecording-----')


#Open and Set the data of the WAV file
file = wave.open(filename, 'wb')
file.setnchannels(channels)
file.setsampwidth(p.get_sample_size(sample_format))
file.setframerate(fs)

#Writeand Close the File
file.writeframes(b''.join(frames))
file.close()


print('-----PlayBack-----')

# Set chunk size of 1024 samples per data frame
chunk = 1024  

# Open the sound file 
wf = wave.open(filename, 'rb')

# Create an interface to PortAudio
p = pyaudio.PyAudio()

# Open a .Stream object to write the WAV file to
# 'output = True' indicates that the sound will be played rather than recorded
stream = p.open(format = p.get_format_from_width(wf.getsampwidth()), channels = wf.getnchannels(), rate = wf.getframerate(), output = True)

# Read data in chunks
data = wf.readframes(chunk)

# Play the sound by writing the audio data to the stream
while data != '':
    stream.write(data)
    data = wf.readframes(chunk)

# Close and terminate the stream
stream.close()
p.terminate()