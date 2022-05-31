from gtts import gTTS
import random
import time
import playsound
import speech_recognition as sr
import webbrowser

#commands
commands = dict()
commands['привет'] = 'Привет!'
commands['как дела'] = 'дела очень хорошо'
commands['кто ты'] = 'я голосовой помошник верси 0.2, Меня создал Норайр Петросян'
commands['как тебя зовут'] = 'Меня зовут голосовой помошник'
commands['раскажи анекдот'] = 'пока не научился'
commands['открой google'] = 'https://google.com'
commands['открой facebook'] = 'https://facebook.com'
commands['открой yandex'] = 'https://yandex.ru'
commands['открой youtube'] = 'https://youtube.com'
commands['открой армянсую музыку'] = 'https://www.youtube.com/watch?v=z2gWG0Fbptw&list=PLJLbBcB--qZeBvUB9MEvnwqLVBE2rM3c6'

def listen_command():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Скажите вашу команду: ")
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

    if message in commands:
        print(commands[message])
        
        if(first_word=='open'):
            webbrowser.open(commands[message])
        else:
            say_message(commands[message])

        if commands[message] == "Выход":
            say_message("Пока!")
            exit()    
        

def say_message(message):
    voice = gTTS(message, lang="ru")
    file_voice_name = "_audio_"+str(time.time())+"_"+str(random.randint(0,100000))+".mp3"
    voice.save(file_voice_name)
    playsound.playsound(file_voice_name)
    print("Голосовой ассистент: "+message)

if __name__ == '__main__':
    while True:
        command = listen_command()
        run_command(command)