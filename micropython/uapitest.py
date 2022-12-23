import urequests as requests
import ujson
import os

ssid = "Fios-GBHSL"
pwd = "face0948tom7403sit"

# get the api key from your environment variables
apikey = os.getenv('OPENAI_API_KEY')

api_url = "https://api.openai.com/v1/completions"
headers = {"Authorization":"Bearer " + apikey, "Content-Type":"application/json"}
post = {"model": "text-davinci-002", "prompt": "Who is a human?", "temperature": 0.7, "max_tokens": 256, "top_p": 1, "frequency_penalty": 0, "presence_penalty": 0}


def get_gpt3_completion():
  response = requests.post(api_url, data=ujson.dumps(post), headers=headers)

  if response.status_code != 404:
      json_response = response.json()
      # print(json_response["choices"][0]["text"])
  
  return json_response["choices"][0]["text"]



def connect_wifi():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, pwd)
        while not wlan.isconnected():
            pass
    print('connected to: ' + ssid)        
    # print('network config:', wlan.ifconfig())


connect_wifi()
print(get_gpt3_completion())