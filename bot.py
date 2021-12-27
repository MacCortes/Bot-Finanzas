import telebot as tb
import pandas as pd
from auxiliar import bot_token

movimientos = pd.read_csv('bases/movimientos.csv', encoding='utf-8')
cuentas = pd.read_csv('bases/cuentas.csv', encoding='utf-8')

print(bot_token)

bot = tb.TeleBot(bot_token)

print('Iniciado')

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Bot de Finanzas Personales iniciado")

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "Comandos disponibles")

@bot.message_handler(commands=["movimiento"])
def add_trans(message):
	pass


@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.send_message(message.chat.id, 'Probando')

#bot.infinity_polling()

print('Listo')