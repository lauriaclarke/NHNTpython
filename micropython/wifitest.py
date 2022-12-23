
import urequests as requests
import ujson
import os

ssid = "Fios-GBHSL"
pwd = "face0948tom7403sit"
# get the api key from your environment variables
apikey = os.getenv('OPENAI_API_KEY')
model = "davinci:ft-parsons-school-of-design-2022-11-15-19-36-19"


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

def get_user_request_header():
    post_data = ujson.dumps({ 'account': 'user_account', 'password': 'password'})
    request_url = 'http://passport2.makeblock.com/v1/user/login'
    res = requests.post(request_url, headers = {'content-type': 'application/json'}, data = post_data).json()
    header_data = ''
    if res['code'] == 0:
        header_data = { "content-type": 'application/json; charset=utf-8', "devicetype": '1'}
        header_data["uid"] = str(res['data']['user']['uid'])
        header_data["deviceid"] = '30AEA427EC60'
    return header_data

def get_air_quality_info():
    if not codey.wifi.is_connected():
        return ''
    post_data = ujson.dumps({ "cid": cid, "arg": arg})
    request_url = 'http://msapi.passport3.makeblock.com/' + 'air/getone'
    res = requests.post(request_url, headers = get_user_request_header(), data = post_data)
    text = res.text
    return float(text)



connect_wifi()





# def main():
# if __name__ == "__main__":
    # main()
