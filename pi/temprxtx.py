

def receiveGGWave(p):
    stream = p.open(format=pyaudio.paFloat32, input_device_index=1, channels=1, rate=48000, input=True, frames_per_buffer=1024)

    # print('listening ... Press Ctrl+C to stop')
    instance = ggwave.init()

    try:
        while True:
            data = stream.read(1024, exception_on_overflow=False)
            #print(len(data))
            #print(data[1])
            res = ggwave.decode(instance, data)
            if (not res is None):
                try:
                    outputText = res.decode("utf-8")
                    # print('received text: ' + res.decode("utf-8"))

                    # successful decode
                    ggwave.free(instance)
                    stream.stop_stream()
                    stream.close()
                    # p.terminate()

                    return outputText

                except:
                    pass
    except KeyboardInterrupt:
        pass
        
def sendGGWave(inputText, p):

    # split strings that are too long into chunks of length MAX_STRING characters
    # TODO: end on word breaks instead of mid-word
    toSend = []
    if len(inputText) > MAX_STRING:
        i = 0
        while i < len(inputText):
            i += MAX_STRING
            toSend.append(inputText[i - MAX_STRING:i])
    else:
        toSend.append(inputText)

    print(toSend)


    # send the array of strings
    for i in range(0, len(toSend)):
        #p = pyaudio.PyAudio()

        #print(p)

        instance = ggwave.init()
        
        # generate audio waveform for string "hello python"
        waveform = ggwave.encode(toSend[i], protocolId = 1, volume = 20)
        # print("transmitting text " + toSend[i] + "...")
        # write to the pyaudio stream
        stream = p.open(format=pyaudio.paFloat32, channels=2, rate=48000, output=True, frames_per_buffer=4096)
        stream.write(waveform, len(waveform)//4)

        # close the audio stream
        ggwave.free(instance)
        stream.stop_stream()
        stream.close()
        #p.terminate()

    # print("done sending")