import requests
import json
import re
import os

# get the api key from your environment variables
apikey = os.getenv('OPENAI_API_KEY')

modelA = "davinci:ft-parsons-school-of-design-2022-11-15-19-36-19"
modelB = "text-davinci-002"

api_url = "https://api.openai.com/v1/completions"
headers = {"Authorization":"Bearer " + apikey, "Content-Type":"application/json"}

prompt = "The following conversation is a conversation between two AIs about the nature of human beings. \nAI1: Who is a human?\nAI2: It really depends who you ask and in which context. Generally, I find the notion of the human is mysterious and sometimes misleading.\nAI1: Who do you think has the best answer to such a complicated question?"

for x in range(3):

    if x % 2 == 0:
        model = modelB
        preprompt = "AI2: "
    else:
        model = modelA
        preprompt = "AI1: "

    post = {
      "model": model,
      "prompt": prompt + "\n" + preprompt,
      "temperature": 0.7,
      "max_tokens": 150,
      "top_p": 1,
      "frequency_penalty": 0,
      "presence_penalty": 0,
      "stop": ["AI1:", "AI2:"]
    }

    print("\n** " + model + ": " + prompt + "\n" + preprompt + " **\n")

    response = requests.post(api_url, data=json.dumps(post), headers=headers)

    if response.status_code != 404:
        json_response = response.json()
        response_string = json_response["choices"][0]["text"].strip()
        print(response_string)
        prompt = prompt + "\n" + preprompt + response_string

def filterResponse():
    if len(re.findall('\.|\?', response_string)) > 1:
        p = re.split('\.|\?', response_string)
        # print(p)
        prompt = p[0]
    else:
        prompt = response_string

