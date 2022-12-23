import requests
import json
import re
import inspect
import os

# get the api key from your environment variables
apikey = os.getenv('OPENAI_API_KEY')

modelA = "davinci:ft-parsons-school-of-design-2022-11-15-19-36-19"
# modelA = "text-davinci-003"
modelB = "text-davinci-002"

api_url = "https://api.openai.com/v1/completions"
headers = {"Authorization":"Bearer " + apikey, "Content-Type":"application/json"}

prompt_array = ["The following conversation is a conversation between two AIs about the nature of human beings.\n", "A: Who is a human?\n", "B: It really depends who you ask and in which context. Generally, I find the notion of the human is mysterious and sometimes misleading.\n", "A: Who do you think has the best answer to such a complicated question?\n"]


def array_to_string(input):
    output = ""
    for x in input:
        output = output + x
    return output 

def converse(n_exchange, starter_prompt):
    
    responses = []

    responses = responses + starter_prompt

    prompt = array_to_string(responses)

    print(prompt)

    # loop will iterate for duration of conversation
    for x in range(n_exchange):
        # print("\n---------------------------------------------------------\n")
        # switch between model and prompts
        # if x % 2 == 0:
        #     model = modelB
        #     preprompt = "B: "
        #     stop = ["A: "]
        # else:
        model = modelA
        preprompt = "A: "
        stop = [""]
            # stop = ["B: "]
        
        # add the empty preprompt with newline to the response list
        responses.append(preprompt + "\n")

        # turn the array of responses into a long string
        prompt = array_to_string(responses)
        
        # if x % 2 == 0:
        #   prompt = array_to_string(responses)
        # else:
        #   prompt = array_to_string(responses[-2] + responses[-1])

        post = {
          "model": model,
          "prompt": prompt,
          "temperature": 0.7,
          "max_tokens": 150,
          "top_p": 1,
          "frequency_penalty": 0,
          "presence_penalty": 0,
           "stop": stop
        #    "stop": ["A: ", "B: "] #stop
        }
    
        # print("\n** " + model + ": " + prompt + " **\n")

        response = requests.post(api_url, data=json.dumps(post), headers=headers)

        if response.status_code != 404:
            # get the json response
            json_response = response.json()
            print("\n\n")
            print(post)
            print("\n\n")
            print(json_response)
            print("\n\n")
            json_response_string = json_response["choices"][0]["text"].strip()

            # add the preprompt to the response and make sure it has a new line 
            full_response = preprompt + json_response_string + "\n"

            # remove the empty preprompt from the list
            responses.pop()
            
            # add the formatted string to the list
            responses.append(full_response)
            
            print(full_response)


        elif response.status_code == 404:
            print("*** 404 ERROR ON REQUEST ***")
            return

    return responses


def main():
    conversation = converse(1, prompt_array)
    print(array_to_string(conversation))


if __name__ == "__main__":
    main()