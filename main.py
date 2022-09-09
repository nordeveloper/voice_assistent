from gtts import gTTS
import random
import time
from playsound import playsound
import speech_recognition as sr
import webbrowser
import requests
import json
import xml.etree.ElementTree as ET
import xmltodict

#commands
commands = dict()
commands['барев'] = 'барев, вонс эс!'
commands['привет'] = 'привет!'
commands['как дела'] = 'дела очень хорошо'
commands['кто ты'] = 'я голосовой помошник верси 0.4, Меня создал Норайр Петросян'
commands['как тебя зовут'] = 'Меня зовут голосовой помошник'
commands['расскажи анекдот'] = 'У тетки сломался телевизор – звонит в контору по ремонту, просит прислать мастера. Тот приходит, долго ковыряется и говорит – H–н–да… тут мастер нужен!'
commands['расскажи сказку'] = 'Пока незнаю никаких сказок'
commands['курс доллара'] = 'usdamd'
commands['курс рубля'] = 'rubamd' 
commands['прогноз погоды'] = 'weather'
commands['открой google chrome'] = 'https://google.com'
commands['открой google'] = 'https://google.com'
commands['открой facebook'] = 'https://facebook.com'
commands['открой yandex'] = 'https://yandex.ru'
commands['открой youtube'] = 'https://youtube.com'
commands['открой армянскую музыку'] = 'https://www.youtube.com/watch?v=z2gWG0Fbptw&list=PLJLbBcB--qZeBvUB9MEvnwqLVBE2rM3c6'


def exchange(currency):

    res = 'курс не найден'

    ex = requests.get('https://cdn.cur.su/api/latest.json').json()
    jd = json.dumps(ex)
    ar = json.loads(jd)
    if(currency=='usdamd'):
       res = str(round(ar['rates']['AMD']))

    if(currency=='usdrub'):
      res = str(round(ar['rates']['RUB']))

    if(currency=='rubamd'):
      res = str(round(ar['rates']['AMD']/ar['rates']['RUB'], 2))    
    return res


def weather():
    response = requests.get("https://export.yandex.ru/bar/reginfo.xml?region=10262")
    xml_content = response.content
    jd = json.dumps(xmltodict.parse(xml_content))
    ar = json.loads(jd)
    wdata = ar['info']['weather']['day']['day_part']

    for w in wdata:
        # print(w)
        if 'temperature' in w:
            wtxt = w['@type'] + 'ом '+ w['temperature']['#text']+', '

        if 'temperature_from' in w:
            wtxt+= w['@type'] + ' от '+ w['temperature_from']['#text']

        if 'temperature_to' in w:
            wtxt+= ' до '+ w['temperature_to']['#text']+', '
        
    return wtxt


def listen_command():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Скажите вашу команду:")
        audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    try:
        our_speech = r.recognize_google(audio, language="ru")
        print("Вы сказали: "+our_speech)
        return our_speech
    except sr.UnknownValueError:
        return "ошибка"
    except sr.RequestError:
        return "ошибка"

def run_command(message):
    message = message.lower()

    first_word = message.split()[0]

    if message == "выход":
        say_message("Пока!")
        exit()   

    if message in commands:
        print('комманда։ '+commands[message])        
        if(first_word=='открой'):
            webbrowser.open(commands[message])

        if(first_word=='курс' and len(message.split()[1]) > 0 ):
            ex_text = exchange(commands[message])
            say_message(ex_text)

        if(commands[message]=='weather'):
            weather_text = weather()
            say_message(weather_text)
        else: 
            print(message)       
            say_message(commands[message])

        

def say_message(message):
    voice = gTTS(message, lang="ru")
    file_voice_name = "_audio_"+str(time.time())+"_"+str(random.randint(0,100000))+".mp3"
    print("Голосовой ассистент: "+message)
    voice.save(file_voice_name)
    playsound(file_voice_name)

if __name__ == '__main__':
    while True:
        command = listen_command()
        run_command(command)