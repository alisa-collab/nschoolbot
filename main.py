import pandas as pd
import telebot
bot = telebot.TeleBot(TOKEN)
global passed
раssed = 0
@bot.message_handler(commands=["начало"])
def begin(message):
  if message.text == '/начало' or message.text == '/Начало':
    bot.send_message(message.chat.id, "Здравствуйте! Этот бот поможет вам быстро и легко создать новый чат. Вот список команд: \n \n/начало - это активирует бота \n \n/руководство - в ответ на это бот отправит вам файл с небольшим руководством\n \n/участники - это команда для того, чтобы бот помог вам добавить нужных учеников \n \n/имена - в ответ на эту команду бот отправит сообщение с именами и никнеймами учеников, чтобы было проще обратиться к кому-то из них \n \nТеперь отправьте пароль")
    bot.register_next_step_handler(message, password)
@bot.message_handler(commands=["руководство"])
def begin(message):
  if message.text == '/руководство' or message.text == '/Руководство':
    bot.send_message(message.chat.id, "Вот ссылка на руководство по работе с этим ботом: https://docs.google.com/document/d/1sMwiC7Evf1htI5mkBIy2CkTm4C4OhY7Cch8WcISNSu4/edit?usp=sharing")
@bot.message_handler(commands=["пароль"])
def password(message):
  if message.text == 'НоваяШкола':
    passed = 1
    bot.send_message(message.chat.id, "Хорошо, можем продолжать")
  elif '/пароль' in message.text or '/пароль' in message.text:
    if str(*message.text.split('\n')[1:2:]) == 'НоваяШкола':
      passed = 1
      bot.send_message(message.chat.id, "Хорошо, можем продолжать")
  else:
    bot.send_message(message.chat.id, "Кажется, что-то не так, можете попробовать еще раз")
@bot.message_handler(commands=["участники"])
def new_members(message):
  if message.text == "/участники" or message.text == '/Участники' and passed == 1:
    bot.send_message(message.chat.id, 'Отправьте список участников учебной группы в таком формате: \n/список \nНомер параллели \nФИО ученика 1 \nФИО ученика 2 \nИ так далее')
    bot.register_next_step_handler(message, recieve_members)
  elif passed == 0:
    bot.send_message(message.chat.id, 'Вы еще не прошли идентификацию. Для того, чтобы это сделать, напишите "/пароль" и сам пароль в следующей строке')
    bot.register_next_step_handler(message, password)

def recieve_members(message):
  if '/список' in message.text or '/Список' in message.text:
    global class_num
    class_num = str(*message.text.split('\n')[1:2:])
    if class_num in ['10']:
      t_name = "/content/project" + str(class_num) + ".csv"
      table = pd.read_csv(t_name)
      global members
      members = {}
      for i in range(table.shape[0]):
        members[table['Name'][i]] = table['Telegram username'][i]
      global users
      users = message.text.split('\n')[2::]
      members_to_add = 'Вот список тех, кого надо добавить:'
      for i in members.keys():
        if i in users:
          members_to_add += '\n' + members.get(i)
      bot.send_message(message.chat.id, members_to_add)
    else:
      bot.send_message(message.chat.id, "Я не знаю такого номера параллелли, попробуйте еще раз")
@bot.message_handler(commands=["имена"])
def names(message):
  if message.text == '/имена' or message.text == '/Имена' and passed == 1:
    mes = 'Вот имена и никнеймы учеников в группе: \n'
    for i in users:
      mes += i + ' - ' + members.get(i) + '\n'
    bot.send_message(message.chat.id, mes)
  elif passed == 0:
    bot.send_message(message.chat.id, 'Вы еще не прошли идентификацию. Для того, чтобы это сделать, напишите "/пароль" и сам пароль в следующей строке')
    bot.register_next_step_handler(message, password)
bot.polling(none_stop=True, interval=0)
