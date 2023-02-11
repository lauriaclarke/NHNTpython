import ggwave
import os
import re
import sys
import openai
from ctypes import *
import ggwave
import numpy as np
import sounddevice as sd
import time
import datetime
from gtts import gTTS
import audio2numpy as a2n
# import librosa


SHIFT_SEND = 40
SHIFT_RECEIVE = -30

MAX_TOKENS=200
MAX_STRING=140

PROTOCOL = 4

# computer settings
# OUTPUT_DEVICE=20
# INPUT_DEVICE=20

# pi settings
OUTPUT_DEVICE=0
INPUT_DEVICE=1

EXCHANGE_COUNT=10

# get the api key from your environment variables
apikey = os.getenv('OPENAI_API_KEY')
openai.api_key = apikey

# alien aesthetics reading
# modelReceive = "davinci:ft-parsons-school-of-design-2022-11-15-19-36-19"

# environmental literature
# modelReceive = "davinci:ft-parsons-school-of-design-2023-01-20-01-37-01"

# latour
modelReceive = "davinci:ft-parsons-school-of-design-2023-02-06-15-16-50"

# generic models
# modelReceive = "text-davinci-003"
modelSend = "text-davinci-003"
   
stop = ["."]

# promptArray = ["The following conversation is a conversation between two AIs about the nature of human beings.\n", "AI1: Who is a human?\n", "AI2: It really depends who you ask and in which context. Generally, I find the notion of the human is mysterious and sometimes misleading.\n", "AI1: Who do you think has the best answer to such a complicated question?\n"]
# promptArray = ["Why are humans so mean to plants?\n"]
promptArray = ["Who is a human?\n"]
prepromptSend = "Ask a question about the following statement from the perspective of a houseplant: "
prepromptReceive = "Answer this question from the perspective of a houseplant who hates humans: "

def arrayToString(input):
    output = ""
    for x in input:
        output = output + x
    return output 

def getMessagePart(inputText):
    partRegex = re.compile(r'(\d)[/](\d)') 
    regexOut = partRegex.search(inputText)

    if regexOut == None:
        print("no message marker")
        return 1, 1, inputText
    else:
        # extract the message number and and number of parts 
        msgNumber = regexOut.group(1)
        msgParts = regexOut.group(2)
    
        # strip the part numbers from the message
        messageText = re.sub('\d[/]\d:', '', inputText)
    
        return msgNumber, msgParts, messageText

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
    # split strings that are too long into chunks of length MAX_STRING characters
    # TODO: end on word breaks instead of mid-word
    
    # print(inputText)
    # print(len(inputText))

    toSend = []
    if len(inputText) > MAX_STRING:
        i = 0
        while i < len(inputText):
            i += MAX_STRING
            toSend.append(inputText[i - MAX_STRING:i])
    else:
        toSend.append(inputText)


    # print(toSend) 
    
    stream = sd.OutputStream(
        dtype='float32', 
        device=OUTPUT_DEVICE, 
        channels=1, 
        samplerate=48000)
    
    stream.start()
    
    # send the array of strings
    for i in range(0, len(toSend)):

        partString = str(i + 1) + "/" + str(len(toSend)) + ": "
        print(partString)

        # if len(toSend) > 1:
        
        stringToSend = partString + toSend[i]
        
        # generate audio waveform for string "hello python"
        # waveform = ggwave.encode(toSend[0], protocolId = 1, volume = 50)
        waveform = ggwave.encode(stringToSend, protocolId = PROTOCOL, volume = 50)

        print("transmitting text... " + toSend[i])

        # write to the pyaudio stream
        towrite = np.frombuffer(waveform, 'float32')

        stream.write(towrite)

    # close the audio stream
    stream.stop()
    stream.close()

def sendGGWaveUT(inputText, pitchShift):
    # split strings that are too long into chunks of length MAX_STRING characters
    # TODO: end on word breaks instead of mid-word
    
    # print(inputText)
    # print(len(inputText))

    toSend = []
    if len(inputText) > MAX_STRING:
        i = 0
        while i < len(inputText):
            i += MAX_STRING
            toSend.append(inputText[i - MAX_STRING:i])
    else:
        toSend.append(inputText)


    # print(toSend) 
    
    stream = sd.OutputStream(
        dtype='float32', 
        device=OUTPUT_DEVICE, 
        channels=2, 
        samplerate=48000)
    
    stream.start()
    
    # send the array of strings
    for i in range(0, len(toSend)):

        partString = str(i + 1) + "/" + str(len(toSend)) + ": "
        print(partString)

        # if len(toSend) > 1:
        
        stringToSend = partString + toSend[i]
        
        # generate audio waveform for encoded text
        ggwaveWaveform = ggwave.encode(stringToSend, protocolId = PROTOCOL, volume = 50)
        ggwaveOut = np.frombuffer(ggwaveWaveform, 'float32')

        # encode in voice data
        ttsWaveform = gTTS(stringToSend)
        ttsWaveform.save('hello.mp3')

        # adjust sample rate accordingly
        cmd = "ffmpeg -hide_banner -loglevel error -i hello.mp3 -ar " + str(sampleRateAdjust) + " hello_48k.mp3"
        os.system(cmd)
        ttsOut, sampleRate = a2n.open_audio('hello_48k.mp3')

        # remove our files 
        os.system("rm *.mp3")

        # apply pitch shift
        # ttsOut = librosa.effects.pitch_shift(ttsOut, sr=48000, n_steps=pitchShift)

        # reformat
        ttsOut32 = np.frombuffer(ttsOut, 'float32')


        # make sure they're the same length
        print(len(ttsOut32), len(ggwaveOut))
        if len(ttsOut32) > len(ggwaveOut):
            ttsOut32 = ttsOut32[0:len(ggwaveOut)]
        else:
            zeroArray = np.zeros(len(ggwaveOut) - len(ttsOut32), dtype=np.float32)
            ttsOut32 = np.append(ttsOut32, zeroArray)
        
        # ttsOut32 = np.frombuffer(ttsOut32, 'float32')

        # format the data into an array appropriately
        finalOutput = [ttsOut32, ggwaveOut]
        aa = np.array(finalOutput)
        a = np.ascontiguousarray(aa.T)
        print(a.shape)
        print("transmitting text... " + toSend[i])

        # write to the pyaudio stream
        stream.write(a)

    # close the audio stream
    stream.stop()
    stream.close()

def receiveGGWave():
    stream = sd.InputStream(
        dtype='float32', 
        device=INPUT_DEVICE, 
        channels=1, 
        samplerate=48000, 
        blocksize=1024)

    # start the sound decive input stream    
    stream.start()

    print('listening ... press Ctrl+C to stop')

    # ggwave instace
    instance = ggwave.init()

    # initialize function to expect three parts
    msgParts = 3
    msgNumber = 1

    # array to store the messages 
    msgs = []

    try:
        # until we've received all parts, call this function
        while msgNumber < msgParts:

            # get data from the stream
            data, overflow = stream.read(1024)

            # convert from numpy to bytes  
            databytes = bytes(data[:, 0])

            # decode the bytes
            res = ggwave.decode(instance, databytes)

            # if decode is successful
            if (not res is None):
                try:
                    outputText = res.decode("utf-8")
                    print('received text: ' + res.decode("utf-8"))

                    # get the message number / parts and contents
                    msgNumber, msgParts, outputTextClean = getMessagePart(outputText)

                    print(msgNumber, msgParts, outputTextClean)

                    # append the cleaned output text to the message array
                    msgs.append(outputTextClean)

                except KeyboardInterrupt:
                    pass
    except KeyboardInterrupt:
        pass
    
    # successful decode
    ggwave.free(instance)
    stream.stop()
    stream.close()

    # concatenate all the message parts into a single string
    return arrayToString(msgs)

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

def converseSingle(mode, currentResponses):
    
    responses = []

    responses = responses + currentResponses

    # false means we're in receive mode and the plant is asking questions
    if mode == "send":
        preprompt = prepromptSend
        model = modelSend
    else:
        preprompt = prepromptReceive
        model = modelReceive

    prompt = preprompt + responses[-1] + "\n"
    
    print(prompt)
    
    # get the completion from model
    completion = openai.Completion.create(engine=model, prompt=prompt, max_tokens=MAX_TOKENS, stop=stop)

    responseString = completion.choices[0].text.strip()
    
    fullResponse = responseString + "\n"

    # add the formatted string to the list
    responses.append(fullResponse)
    
    return responses

def waitForStart():
    print("waiting for start command...")
    while True:
        if(receiveGGWave() == "start"):
            break

def rxtxrxTest():
    outputText = receiveGGWave()
    print(outputText)
    sendGGWave("howdy I'm a raspberry pi")
    outputText = receiveGGWave()

# return a tuple with the mode of the plant and the current state of the sendReceive flag
def parseArgs():
    if(len(sys.argv) > 1):
        args = sys.argv[1:]
        print(args)
        if(args[0] == "send"):
            print("starting in SEND mode")
            return "send", True
        elif(args[0] == "receive"):
            print("starting in RECEIVE mode")
            return "receive", False
    else:
        print("couldn't parse argument, starting in RECEIVE mode")
        return "receive", False
    

# state machine:
#   query gpt3
#   send data over sound
#   listen
#   receive data over sound

def main(): 
    alsaErrorHandling()

    # create a log file
    t = datetime.datetime.now()
    filename = "logs/" + t.strftime("%m_%d_%H_%M_%S") + ".txt"
    f = open(filename, "w")
    
    # devices = sd.query_devices(0)
    # print(devices)
    # devices = sd.query_devices(1)
    # print(devices)

    # keep track of whether we start in send or receive mode
    # initialize the flag for switching between send and receive per the conversation
    mode, sendReceive = parseArgs()

    # wait for start command
    waitForStart()

    # wait three second before starting
    time.sleep(3)

    # if we're in receive mode first then just start with a blank array
    responses = []

    # if send mode load a question from the prompt
    if mode == "send":

        # set the sample rate adjustment based on initial state
        pitchShift = SHIFT_SEND

        time.sleep(1)
        responses = responses + promptArray 

        if PROTOCOL == 4:
            sendGGWaveUT(responses[0], sampleRateAdjust)
        else:
            sendGGWave(responses[0])

        # write to logfile
        f.write(responses[0] + "\n")

        sendReceive = False
    else: 
        pitchShift = SHIFT_RECEIVE

    # start the conversation
    for i in range(0, EXCHANGE_COUNT):
        
        if sendReceive == True:
            # get a response from the API
            responses = converseSingle(mode, responses)
            
            # give some time to improce cadence
            time.sleep(1)

            print("\nsending...\n")

            # send the most recent response
            if PROTOCOL == 4:
                sendGGWaveUT(responses[-1], sampleRateAdjust)
            else:
                sendGGWave(responses[-1])

            # write to logfile
            f.write(responses[-1] + "\n")

            sendReceive = False

        elif sendReceive == False:
            print("\nreceiving...\n")

            outputText = receiveGGWave()

            responses.append(outputText)

            # write to logfile
            f.write(outputText + "\n")
            
            sendReceive = True

    f.close()




if __name__ == "__main__":
    main()
