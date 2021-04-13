#libraries
import telebot
import os
import subprocess
import requests
import json
import datetime
import calendar

#bot main settings
bot=telebot.TeleBot('1779209869:AAFtKr9seF0j08JvpsYJfCtWLkHnmtiTXUA')
chars = 'abcdefghijklnopqrstuvwxyz1234567890'
api_key="411f595c4c1467dec55ad9b125d12217"
input_day=datetime.datetime.today().strftime('%A').lower()
if input_day == "monday":
 ru_day="Понедельник"
elif input_day == "tuesday":
 ru_day="Вторник"
elif input_day == "wednesday":
 ru_day="Среда"
elif input_day == "thursday":
 ru_day="Четверг"
elif input_day == "friday":
 ru_day="Пятница"
elif input_day == "saturday":
 ru_day="Суббота"
elif input_day == "sunday":
 ru_day="Воскресенье, бот отдыхает"
else:
 print("День указан неправильно")
print(input_day, ru_day)
#buttons
keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard.row('Сow', 'Расписание на сегодня')
#bot commands
@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(message.from_user.id, "Добро пожаловать в petroshedulebot, мои создатели Аверин Андрей, Прохоров Евгений и Березко Роман, студенты группы 39-55")
@bot.message_handler(content_types=["text"])
#bot functions
def napisal(message):
#test functions
  if message.text.lower() == "сow":
    output = subprocess.check_output('cowsay There is no cow level in bot', shell=True)
    print("cow")
    bot.send_message(message.chat.id, output, reply_markup=keyboard)
#main function
  elif message.text.lower() =="расписание на сегодня":
    def api_request(api_key, input_day):
      try:
        response = requests.get(f'https://petrocol.ru/schedule/39-55?json=1&key={api_key}')
        if response.status_code == 200:
          print("successful request (code 200)")
          response_json = json.loads(response.text)
          period = ""
          try:
            day_json = response_json["schedule"]["monday"]
          except:
            bot.reply_to(message, "NET PAR EPTA")
          else:
            reply_message = ""
            for i in range(len(day_json)):
              try:
                lesson_json = day_json[str(i+1)][0]
                lesson = lesson_json['lesson']
                teacher = lesson_json['teacher']
                classroom = lesson_json['classroom']
                period += f'Пара {i+1}:\n {lesson}, {teacher}, {classroom}\n'
                # print(period)
                reply_message = f'День недели: {ru_day}\n {period}'
              except:
                pass
            bot.reply_to(message, reply_message)
      except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
      except Exception as err:
        print(f'Other error occurred: {err}')
    api_request(api_key, input_day)
  else:
    bot.send_message(message.chat.id, "Неправильный запрос.")
bot.polling(none_stop=True, interval=0)
