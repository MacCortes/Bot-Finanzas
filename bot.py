import telebot

# 1678222267:AAFWYbb5BmVO0HRwlc6XeX5YsxvrhMesqbs

token = '1678222267:AAFWYbb5BmVO0HRwlc6XeX5YsxvrhMesqbs'

bot = telebot.TeleBot(token)

print('Iniciado')

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Bot de Finanzas Personales iniciado")

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "Comandos disponibles")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, 'Probando')

bot.infinity_polling()

print('Listo')