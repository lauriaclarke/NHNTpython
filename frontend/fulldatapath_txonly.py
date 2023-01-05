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

MAX_TOKENS=150

# get the api key from your environment variables
apikey = os.getenv('OPENAI_API_KEY')
openai.api_key = apikey

# modelA = "davinci:ft-parsons-school-of-design-2022-11-15-19-36-19"
modelA = "text-davinci-003"
modelB = "text-davinci-002"

api_url = "https://api.openai.com/v1/completions"
headers = {"Authorization":"Bearer " + apikey, "Content-Type":"application/json"}

promptArray = ["The following conversation is a conversation between two AIs about the nature of human beings.\n", "AI1: Who is a human?\n", "AI2: It really depends who you ask and in which context. Generally, I find the notion of the human is mysterious and sometimes misleading.\n", "AI1: Who do you think has the best answer to such a complicated question?\n"]



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

def sendGGWave(inputText):
    # suppress alsa errors
    alsaErrorHandling()
    
    p = pyaudio.PyAudio()

    # generate audio waveform for string "hello python"
    waveform = ggwave.encode(inputText, protocolId = 1, volume = 20)

    print("transmitting text " + inputText + "...")
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=48000, output=True, frames_per_buffer=4096)
    stream.write(waveform, len(waveform)//4)
    stream.stop_stream()
    stream.close()

    p.terminate()
    
def receiveGGWave():
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

def converseLoop(n_exchange, starterPrompt):
    
    responses = []

    responses = responses + starterPrompt

    prompt = arrayToString(responses)

    print(prompt)

    # loop will iterate for duration of conversation
    for x in range(n_exchange):
        # print("\n---------------------------------------------------------\n")
        # switch between model and prompts
        if x % 2 == 0:
            model = modelB
            preprompt = "AI2: "
            stop = ["AI1: "]
        else:
            model = modelA
            preprompt = "AI1: "
            stop = ["AI2: ", "."]
        
        # add the empty preprompt with newline to the response list
        responses.append(preprompt + "\n")

        # turn the array of responses into a long string
        prompt = arrayToString(responses)

        # for modelB use the entire prompt, for modelA only the last two responses 
        if x % 2 == 0:
          prompt = arrayToString(responses)
        else:
          prompt = arrayToString(responses[-2] + responses[-1])

        # print("\n** " + model + ": " + prompt + " **\n")
        
        # get the completion from model
        completion = openai.Completion.create(engine=model, prompt=prompt, max_tokens=100, stop=stop)

        responseString = completion.choices[0].text.strip()
        
        # add the preprompt to the response and make sure it has a new line 
        fullResponse = preprompt + responseString + "\n"

        # remove the empty preprompt from the list
        responses.pop()
        
        # add the formatted string to the list
        responses.append(fullResponse)
        
        print(fullResponse)

    return responses

def converseSingle(n, currentResponses):
    
    responses = []

    responses = responses + currentResponses

    prompt = arrayToString(responses)

    print(prompt)

    # switch between model and prompts
    if n % 2 == 0:
        model = modelB
        preprompt = "AI2: "
        stop = ["AI1: "]
    else:
        model = modelA
        preprompt = "AI1: "
        stop = ["AI2: ", "."]
    
    # add the empty preprompt with newline to the response list
    responses.append(preprompt + "\n")

    # turn the array of responses into a long string
    prompt = arrayToString(responses)

    # for modelB use the entire prompt, for modelA only the last two responses 
    if n % 2 == 0:
      prompt = arrayToString(responses)
    else:
      prompt = arrayToString(responses[-2] + responses[-1])
    
    # print("\n** " + model + ": " + prompt + " **\n")
    
    # get the completion from model
    completion = openai.Completion.create(engine=model, prompt=prompt, max_tokens=MAX_TOKENS, stop=stop)

    responseString = completion.choices[0].text.strip()
    
    # add the preprompt to the response and make sure it has a new line 
    fullResponse = preprompt + responseString + "\n"

    # remove the empty preprompt from the list
    responses.pop()
    
    # add the formatted string to the list
    responses.append(fullResponse)
    
    # print(fullResponse)

    return responses



# state machine:
#   query gpt3
#   send data over sound
#   listen
#   receive data over sound

def main():

    responses = []

    responses = responses + promptArray 

    for i in range(0, 3):
        responses = converseSingle(i, responses)
        print("sending...")
        sendGGWave(responses[-1])

    # conversation = converse(3, prompt_array)
    # print(arrayToString(conversation))

    # while True:
    #     print("sending...")
    #     sendGGWave()
    #     sendReceive = False




if __name__ == "__main__":
    main()