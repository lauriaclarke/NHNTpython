import pyaudio
import wave
from ctypes import *

chunk = 256  # Record in chunks of 1024 samples
sample_format = pyaudio.paFloat32  # 16 bits per sample
channels = 1
fs = 48000  # Record at 44100 samples per second
seconds = 3
# filename = "output.wav"
filename = "/usr/share/sounds/alsa/Front_Center.wav"


def recordSound(p):
    # p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    # p.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    print('Finished recording')

def playSound(p):
    print('Play Back')
    
    # Open the sound file 
    wf = wave.open(filename, 'rb')

    print(p.get_format_from_width(wf.getsampwidth()))
    print(wf.getframerate())

    # Open a .Stream object to write the WAV file to
    # 'output = True' indicates that the sound will be played rather than recorded
    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()), channels = channels, rate = wf.getframerate(), output = True, frames_per_buffer=chunk)

    print(stream)
    # # Read data in chunks
    data = wf.readframes(chunk)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(chunk)

    # Close and terminate the stream
    stream.stop_stream()
    stream.close()
    # p.terminate()

    print("Finished Play Back")

def py_error_handler(filename, line, function, err, fmt):
    pass

def alsaErrorHandling():
    # From alsa-lib Git 3fd4ab9be0db7c7430ebd258f2717a976381715d
    # $ grep -rn snd_lib_error_handler_t
    # include/error.h:59:typedef void (*snd_lib_error_handler_t)(const char *file, int line, const char *function, int err, const char *fmt, ...) /* __attribute__ ((format (printf, 5, 6))) */;
    # Define our error handler type
    ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p) 
    c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)

def main():
    alsaErrorHandling()
    p = pyaudio.PyAudio()
    playSound(p)
    p.terminate()


if __name__ == "__main__":
    main()
