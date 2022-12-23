import requests
import json
import os

# get the api key from your environment variables
apikey = os.getenv('OPENAI_API_KEY')
model = "davinci:ft-parsons-school-of-design-2022-11-15-19-36-19"

api_url = "https://api.openai.com/v1/completions"
headers = {"Authorization":"Bearer " + apikey, "Content-Type":"application/json"}
post = {
  "model": model,
  "prompt": "Who is a human?",
  "temperature": 0.7,
  "max_tokens": 256,
  "top_p": 1,
  "frequency_penalty": 0,
  "presence_penalty": 0
}

response = requests.post(api_url, data=json.dumps(post), headers=headers)

if response.status_code != 404:
    json_response = response.json()
    print(json_response)
    print(json_response["choices"][0]["text"])
    for key, value in json_response.items():
        print(key, ":", value)


# print(response.text)
# print(response.json())
# print(response.status_code)
# print(response.headers)