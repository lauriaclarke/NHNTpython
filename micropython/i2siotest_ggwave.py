import time
from machine import I2S
from machine import Pin
import urequests as requests
import os


record_pin = Pin(38, Pin.IN, Pin.PULL_DOWN)

#=====================================

def wait_for_button():
    while record_pin.value() == 0:
        time.sleep_ms(100)
    time.sleep_ms(100)

#=====================================
    
ssid = "Fios-GBHSL"
pwd = "face0948tom7403sit"

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
    
#=====================================
    
def ggwave(message: str,
           protocolId: int = 1,
           sampleRate: float = 48000,
           volume: int = 50,
           payloadLength: int = -1,
           useDSS: int = 0) -> None:

    url = 'https://ggwave-to-file.ggerganov.com/?m=Hello%20world%21'

    params: Dict[str, Union[str, int, float]] = {
        'm': message,        # message to encode
        'p': protocolId,     # transmission protocol to use
        's': sampleRate,     # output sample rate
        'v': volume,         # output volume
        'l': payloadLength,  # if positive - use fixed-length encoding
        'd': useDSS,         # if positive - use DSS
    }
    
    print(params)
    
    response = requests.get(url)
    
    print(type(response))

    if response == '' or b'Usage: ggwave-to-file' in response.content:
        raise SyntaxError('Request failed')

    return response.content

#=====================================
# INPUT 

mic_sck_pin = Pin(26)
mic_ws_pin = Pin(22)
mic_sd_pin = Pin(21)

audio_in = I2S(
    0,
    sck=mic_sck_pin,
    ws=mic_ws_pin,
    sd=mic_sd_pin,
    mode=I2S.RX,
    bits=16,
    format=I2S.MONO,
    rate=16000,
    ibuf=8192,
)

#=====================================
# OUTPUT

spk_bck_pin = Pin(32)
spk_ws_pin = Pin(25)
spk_sdout_pin = Pin(33)

audio_out = I2S(
    1,
    sck=spk_bck_pin,
    ws=spk_ws_pin,
    sd=spk_sdout_pin,
    mode=I2S.TX,
    bits=16,
    format=I2S.MONO,
    rate=48000,
    ibuf=8192,
)

#=====================================

# print("Press and hold button to record")

# wait_for_button()

# print("Recording")

# samples = bytearray(2048)

# with open("test.raw", "wb") as file:
#     while record_pin.value() == 1:
#         read_bytes = audio_in.readinto(samples)
#         # amplify the signal to make it more audible
#         I2S.shift(buf=samples, bits=16, shift=4)
#         file.write(samples[:read_bytes])


# encode with ggwave and create output file
# waveform = ggwave.encode("hello python", protocolId = 1, volume = 20)

# print(type(waveform))


connect_wifi()

waveform = ggwave("hiya!")

print(type(waveform))

with open("testwave.raw", "wb") as file:
    file.write(waveform)

print("Processing data")

# print("Press the button to playback")

# wait_for_button()

samples = bytearray(2048)

with open("testwave.raw", "rb") as file:
    samples_read = file.readinto(samples)
    while samples_read > 0:
        audio_out.write(samples[:samples_read])
        samples_read = file.readinto(samples)

print("Finished playback")









