import telebot as tb
import pandas as pd
from auxiliar import bot_token

# leer los csv
movimientos = pd.read_csv('bases/movimientos.csv', encoding='utf-8')
cuentas = pd.read_csv('bases/cuentas.csv', encoding='utf-8')

# leer los comandos disponibles del txt
with open('comandos.txt', encoding='utf8') as f:
    lines = f.read()

print(bot_token)

bot = tb.TeleBot(bot_token)

print('Iniciado')

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Bot de Finanzas Personales iniciado")

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.send_message(message.chat.id, lines)

@bot.message_handler(commands=["movimiento"])
def add_trans(message):
	pass

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.send_message(message.chat.id, 'Probando')

bot.infinity_polling()

print(lines)
print('Listo')