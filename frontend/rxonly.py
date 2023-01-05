import ggwave
import pyaudio
import requests
import json
import re
import inspect
import os
import openai
from ctypes import *

from pyscript import Element

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
    
def receiveGGWave():
    alsaErrorHandling()

    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=48000, input=True, frames_per_buffer=1024)

    print('listening ... Press Ctrl+C to stop')
    instance = ggwave.init()

    try:
        while True:
            data = stream.read(1024, exception_on_overflow=False)
            res = ggwave.decode(instance, data)
            if (not res is None):
                try:
                    outputText = res.decode("utf-8")
                    print('received text: ' + res.decode("utf-8"))

                    # successful decode
                    ggwave.free(instance)
                    stream.stop_stream()
                    stream.close()
                    p.terminate()

                    return outputText

                except:
                    pass
    except KeyboardInterrupt:
        pass

def arrayToString(input):
    output = ""
    for x in input:
        output = output + x
    return output 

# state machine:
#   listen
#   receive data over sound
#   print output 


startStop = False
responses = []

def startButton():
    response = receiveGGWave()
    print(response)
    startStop = True

def stopButton():
    startStop = False

# while startStop == True:
#     while len(responses) < 3:
#     responses.append(receiveGGWave())
#     if len(responses) > 0:
#         print(responses[-1])
#     else:
#         print("no response has been recorded")





