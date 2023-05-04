from plugins.gpt3 import Gpt3
import os
from vacore import VACore
import subprocess

from PyQt5.QtWidgets import QApplication

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea
from PyQt5.QtCore import QTimer



def start(core:VACore):
    manifest = {
        "name": "GPT",
        "version": "1",
        "require_online": True,

        "commands": {
            "открой пятницу|пятница|запусти пятницу|включи пятниц": main,
        }
    }
    return manifest

def UpdateFileHistory(answer, phrase) -> list:
    try:
        split_answer = answer.split('\n')
        if split_answer[1] == '':
            answer = split_answer[2]
        else: 
            answer = split_answer[1]
        answer = answer.replace('\n', '')
    except:
        pass

    if "GPT :" in answer:
        answer = answer.replace("GPT :", '')
    elif "GPT:" in answer:
        answer = answer.replace("GPT:", '')

    try:
        phrase = phrase.replace('\n', '')
    except:
        pass
    constructor = [f'GPT : {answer} USER : {phrase} \n']
    with open("HistoryChat.txt", "a") as f:
        f.writelines(constructor)

def read_history():
    try:
        with open("HistoryChat.txt", "r") as f:
            content = f.readlines()
    except:
        with open("HistoryChat.txt", "w") as f:
            f.writelines('История нашего диалога \n')
            content = ''
    return content

def phrase_replace(phrase):
    if 'пятница' in phrase:
        phrase = phrase.replace('пятница','')
    elif 'пятницу' in phrase:
        phrase = phrase.replace('пятницу','')
    return phrase

def main(core:VACore, phrase:str):
    print('Пятница запущена')
    phrase += ""



    process =  getattr(core, "previous_answer", None)
    if process == None:
        process = subprocess.Popen(['venv/Scripts/python', 'chat.py'])

    core.previous_answer = process

    

    if phrase != '':
        if 'выйти из контекста' in phrase:
            
            clear_file_history()
            process.terminate()
            core.context_set(main, duration=0)
        else:
            if ('пятница' in phrase) or ('пятницу' in phrase):
                phrase = phrase_replace(phrase)
                history = read_history()
                answer = create_gpt_response(phrase, history)
                UpdateFileHistory(answer, phrase)
                

    core.context_set(main, duration=100)

def create_gpt_response(phrase, history):
    my_list = f' текущий запрос: {phrase}'
    my_string = ''
    for item in history:
        my_string += item
    my_string += my_list
    gpt = Gpt3()
    answer = gpt.response(my_string)
    print(answer)
    return answer

def clear_file_history():
    os.remove('HistoryChat.txt')

if __name__ == "__main__":
    core = VACore()
    core.plugin_load(start)
    core.run()
