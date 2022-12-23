import ggwave
import pyaudio
import requests
import json
import re
import inspect
import os
import openai

# get the api key from your environment variables
apikey = os.getenv('OPENAI_API_KEY')
openai.api_key = apikey

modelA = "davinci:ft-parsons-school-of-design-2022-11-15-19-36-19"
# modelA = "text-davinci-003"
modelB = "text-davinci-002"

api_url = "https://api.openai.com/v1/completions"
headers = {"Authorization":"Bearer " + apikey, "Content-Type":"application/json"}

prompt_array = ["The following conversation is a conversation between two AIs about the nature of human beings.\n", "AI1: Who is a human?\n", "AI2: It really depends who you ask and in which context. Generally, I find the notion of the human is mysterious and sometimes misleading.\n", "AI1: Who do you think has the best answer to such a complicated question?\n"]



def sendGGWave(inputText):

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

def converse(n_exchange, starter_prompt):
    
    responses = []

    responses = responses + starter_prompt

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

        post = {
          "model": model,
          "prompt": prompt,
          "temperature": 0.7,
          "max_tokens": 250,
          "top_p": 1,
          "frequency_penalty": 0,
          "presence_penalty": 0,
           "stop": stop
        }
    
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



# state machine:
#   query gpt3
#   send data over sound
#   listen
#   receive data over sound

def main():
    conversation = converse(3, prompt_array)
    print(arrayToString(conversation))

    # sendReceive = True

    # while True:
    #   if sendReceive == True:

    #     print("sending...")
    #     sendGGWave()
    #     sendReceive = False

    #   elif sendReceive == False:
    #     print("receiving...")
    #     outputText = receiveGGWave()
    #     print(outputText)
    #     sendReceive = True


if __name__ == "__main__":
    main()