import telebot

bot = telebot.TeleBot('-')
data_base = {}
user_data = {'FIO':None,'phone':None,'appointment':None}
zayavka_data = {'FIO':None,'phone':None,'appointment':None}
zayavki = []
doctors = {'therapist':'Терапевт','surger':'Хирург','oncologist':'Онколог','uzi':'УЗИ','mri':'МРТ'}
@bot.message_handler(commands=['apts'])
def apts(message):
  for i in zayavki:
    txt='''ФИО пациента:{0}
    Номер телефона: {1}
    К какому врачу записался: {2}
    '''.format(i['FIO'],i['phone'],i['appointment'])
    bot.send_message(message.chat.id, text = txt)

@bot.message_handler(func=lambda message: message.text == "Назад в меню" )
@bot.message_handler(commands=['start'])
def menu(message):
  if message.chat.id not in data_base.keys():
    data_base[message.chat.id] = user_data.copy()
    print(data_base)
  keyboard = telebot.types.InlineKeyboardMarkup()
  callback_button1 = telebot.types.InlineKeyboardButton(text="Запись на приём", callback_data="appointment")
  callback_button2 = telebot.types.InlineKeyboardButton(text="Мои данные",callback_data="mydata")
  callback_button3 = telebot.types.InlineKeyboardButton(text="Контакты", callback_data="contacts")
  keyboard.add(callback_button1)
  keyboard.add(callback_button2)
  keyboard.add(callback_button3)
  bot.send_message(message.chat.id, "Выберите пункт меню:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "appointment" and data_base[call.message.chat.id]['FIO']==None and data_base[call.message.chat.id]['phone']==None)
def Decline(call):
  bot.answer_callback_query(call.id, 'Сначала заполните анкету!')

@bot.callback_query_handler(func=lambda call: call.data == "appointment" and data_base[call.message.chat.id]['FIO']!=None and data_base[call.message.chat.id]['phone']!=None)
def increase(call):
  markup = telebot.types.InlineKeyboardMarkup()
  for i,j in doctors.items():
    markup.add(telebot.types.InlineKeyboardButton(text=j, callback_data=i))
  
  bot.send_message(call.message.chat.id, "Выберите услугу: ",reply_markup = markup)

@bot.callback_query_handler(func=lambda call: call.data in doctors.keys() )
def Zayavka(call):
  data_base[call.message.chat.id]['appointment'] = doctors[call.data] 
  zayavka = zayavka_data.copy()
  zayavka['FIO'] = data_base[call.message.chat.id]['FIO']
  zayavka['phone'] =data_base[call.message.chat.id]['phone']
  zayavka['appointment'] =data_base[call.message.chat.id]['appointment']
  zayavki.append(zayavka)
  print(zayavki)
  bot.send_message(call.message.chat.id, "Заявка одобрена! ")

@bot.callback_query_handler(func=lambda call: call.data == "mydata" )
def SetName(call):
  bot.send_message(call.message.chat.id, "Отправьте боту свои ФИО (например,Илон Иванович Маск) :")
  bot.register_next_step_handler(call.message,SetPhone)

def SetPhone(message):
  data_base[message.chat.id]['FIO'] = message.text
  print(data_base)
  keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
  button_phone = telebot.types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
  keyboard.add(button_phone)
  bot.send_message(message.chat.id, "Отправьте боту номер телефона!", reply_markup=keyboard)
  bot.register_next_step_handler(message,Complete)



def Complete(message):
  data_base[message.chat.id]['phone'] = message.contact.phone_number
  print(data_base)
  keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
  button = telebot.types.KeyboardButton(text="Назад в меню")
  keyboard.add(button)
  bot.send_message(message.chat.id, "Анкета заполнена!",reply_markup = keyboard)


if __name__ == '__main__':
  bot.polling(none_stop=True)
