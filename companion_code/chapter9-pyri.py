import urllib.request
import json
import pyaudio
import wave
from xml.etree import ElementTree
import subprocess
import time

def record_sound(seconds, chunk_size, sample_rate, filename, channels, format_type):
    p = pyaudio.PyAudio()

    stream = p.open(format=format_type,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk_size)

    print("Speak now")

    frames = []

    for i in range(0, int(sample_rate / chunk_size * seconds)):
        data = stream.read(chunk_size)
        frames.append(data)

    print("Finished")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format_type))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

def google_speech_recognition(filename):
    global url
    #upload the file to google
    audio = open(filename,'rb').read()
    headers={'Content-Type': 'audio/x-flac; rate=16000', 'User-Agent':'Mozilla/5.0'}
    request = urllib.request.Request(url, data=audio, headers=headers)

    response = urllib.request.urlopen(request)
    out = response.read()
    json_data = json.loads(out.decode("utf-8"))

    return json_data

def wolfram_alpha(speech):
    url_section = urllib.parse.urlencode(dict(
        input=speech,
        appid=wolfram_alpha_app_id,
        ))

    url = 'http://api.wolframalpha.com/v2/query?' + url_section
    
    response = urllib.request.urlopen(url)
    
#    print(resp.read())

    tree = ElementTree.parse(response)
    root = tree.getroot()
#    print(root.tag, root.attrib)

    for node in root.findall('.//pod'):
        print(node.attrib['title'])
        for text_node in node.findall('.//plaintext'):
            if text_node.text:
                print(text_node.text)
        print("****")
        

chunk_size = 512
sample_rate = 44100
seconds = 5
filename = "output.wav"
channels = 1
format_type = pyaudio.paInt16

url = "https://www.google.com/speech-api/v1/recognize?client=chromium&lang=en-US"

wolfram_alpha_app_id = "YRY9AV-XP94AHWV9L"

record_sound(seconds, chunk_size, sample_rate, filename, channels, format_type)

#Conver the file to flac
subprocess.call(["sox", "output.wav", "-r16k", "-t", "wav", "output-16k.wav"])
subprocess.call(["flac", "-5", "-f", "output-16k.wav"],stdout=subprocess.PIPE )

time.sleep(2)

try:
    google_data = google_speech_recognition("output-16k.flac")
except urllib.error.HTTPError:
    print("voice recognition failure")
else:
    print(google_data)

    if google_data['status'] == 0:
        wolfram_alpha(google_data['hypotheses'][0]['utterance'])
    else:
        print("Voice recognition failed. Try again")



