import ggwave
import numpy
import sounddevice as sd

# devices = sd.query_devices()
# print(devices)

stream = sd.InputStream(
    dtype='float32', 
    device=20, 
    channels=1, 
    samplerate=48000, 
    blocksize=1024)
        
stream.start()

print('Listening ... Press Ctrl+C to stop')
instance = ggwave.init()
print(instance)

try:
    while True:
        data, overflow = stream.read(1024)
        databytes = bytes(data[:, 0])
        res = ggwave.decode(instance, databytes)
        if (not res is None):
            try:
                print('Received text: ' + res.decode("utf-8"))
            except:
                pass
except KeyboardInterrupt:
    pass

ggwave.free(instance)

stream.stop()
stream.close()


