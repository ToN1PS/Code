import os
import time

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea
from PyQt5.QtCore import QTimer

from plugins.gpt3 import Gpt3
from plugins.plugin_gpt3_threading import read_history, create_gpt_response, UpdateFileHistory

import threading



class ChatWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Настраиваем основное окно
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Чат с ChatGPT')

        thread1 = threading.Thread(target=self.update_from_plugin)
        thread1.start()

        # Создаем виджеты
        self.username_label = QLabel('Вы', self)
        self.chat_history = QTextEdit(self)
        self.chat_history.setReadOnly(True)
        self.chat_input = QLineEdit(self)
        self.send_button_send = QPushButton('Отправить', self)
        self.send_button_clear_history = QPushButton('Очистить историю', self)

        # Создаем контейнер для истории чата
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.chat_history)

        # Создаем контейнеры для размещения виджетов
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        # Добавляем виджеты в контейнеры
        vbox.addWidget(scroll)
        hbox.addWidget(self.chat_input)
        hbox.addWidget(self.send_button_send)
        hbox.addWidget(self.send_button_clear_history)

        # Добавляем контейнеры в основной контейнер
        vbox.addWidget(self.username_label)
        vbox.addLayout(hbox)

        # Привязываем метод send_message к нажатию на кнопку
        self.send_button_send.clicked.connect(self.send_message)
        self.send_button_clear_history.clicked.connect(self.clear_history)

        # Запускаем таймер для обновления истории чата каждые 2 секунды
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.update_chat_history)
        # self.timer.start(200)

        # Устанавливаем контейнер как основное расположение
        self.setLayout(vbox)

    def clear_history(self):
        os.remove('HistoryChat.txt')


    def update_from_plugin(self):
        try:
            # Обновляем историю чата из файла HistoryChat
            file_path = 'HistoryChat.txt'
            last_modified_time = os.path.getmtime(file_path)
        except:
            with open("HistoryChat.txt", "w") as f:
                f.writelines('История нашего диалога \n')
        while True:
            try:
                current_modified_time = os.path.getmtime(file_path)
                if current_modified_time != last_modified_time:
                    with open('HistoryChat.txt', 'r') as f:
                        last_line = f.readlines()[-1]
                    self.write_in_chat(last_line)
                    
                    print ('Последняя строка',last_line)
                    last_modified_time = current_modified_time
                time.sleep(2)
            except:
                with open("HistoryChat.txt", "w") as f:
                    f.writelines('История нашего диалога \n')

    def write_in_chat(self, last_line):
        #  №;№
        print(type(last_line))
        # last_line
        self.chat_history.append(last_line)


    def send_message(self):

        # Получаем текст из текстового поля
        self.user_input = self.chat_input.text()

        # Очищаем текстовое поле
        self.chat_input.clear()

        thread = threading.Thread(target=self.create_gpt_response, args=(self.user_input,))
        thread.start()



        # history = read_histroy()
        # answer = create_gpt_response(self.user_input, history)
        # UpdateFileHistory(answer, self.user_input)

    def create_gpt_response(self, user_input):
        # Читаем историю чата из файла
        history = read_history()

        # Создаем ответ с помощью GPT
        answer = create_gpt_response(user_input, history)

        # Обновляем файл с историей чата
        UpdateFileHistory(answer, user_input)
        

        

if __name__ == '__main__':
    app = QApplication([])
    widget = ChatWidget()
    widget.show()
    app.exec_()
