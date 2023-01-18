
import ggwave
import numpy as np
import sounddevice as sd

# devices = sd.query_devices()
# print(devices)

stream = sd.OutputStream(
    dtype='float32', 
    device=20, 
    channels=1, 
    samplerate=48000)

stream.start()

waveform = ggwave.encode("hello python", protocolId = 1, volume = 20)

towrite = np.frombuffer(waveform, 'float32')

stream.write(towrite)

stream.stop()
stream.close()

# import ggwave
# print(ggwave.__file__)

# # import pyaudio
# # import pprint

# # p = pyaudio.PyAudio()

# instance = ggwave.init()

# # generate audio waveform for string "hello python"
# waveform = ggwave.encode("hello python", protocolId = 1, volume = 20)

# print(type(waveform))

# with open("testwave.raw", "wb") as file:
#     file.write(waveform)

# # print("Transmitting text 'hello python' ...")


# res = ggwave.decode(instance, waveform)
# if (not res is None):
#     try:
#         print('Received text: ' + res.decode("utf-8"))
#     except:
#         pass
# # stream = p.open(format=pyaudio.paFloat32, channels=1, rate=48000, output=True, frames_per_buffer=4096)
# # stream.write(waveform, len(waveform)//4)
# # stream.stop_stream()
# # stream.close()

# # p.terminate()



def sendGGWave(inputText):
    
    # p = pyaudio.PyAudio()

    # split strings that are too long into chunks of length MAX_STRING characters
    # TODO: end on word breaks instead of mid-word
    toSend = []
    if len(inputText) > MAX_STRING:
        i = 0
        while i < len(inputText):
            i += MAX_STRING
            toSend.append(inputText[i - MAX_STRING:i])
    else:
        toSend.append(inputText)

    print(toSend) 
    
    stream = sd.OutputStream(
        dtype='float32', 
        device=OUTPUT_DEVICE, 
        channels=1, 
        samplerate=48000)
    
    stream.start()

    # send the array of strings
    for i in range(0, len(toSend)):
        # generate audio waveform for string "hello python"
        waveform = ggwave.encode(toSend[i], protocolId = 1, volume = 50)

        print("transmitting text " + toSend[i] + "...")

        # write to the pyaudio stream
        towrite = np.frombuffer(waveform, 'float32')

        stream.write(towrite)

    # close the audio stream
    stream.stop()
    stream.close()