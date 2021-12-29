import telebot as tb
import pandas as pd
import dataframe_image as dfi
from auxiliar import bot_token

# read csv
transactions = pd.read_csv('~/Documents/Bot-Finanzas/db/movimientos.csv', encoding='utf-8')
accounts = pd.read_csv('~/Documents/Bot-Finanzas/db/cuentas.csv', encoding='utf-8')

# read availables commands from the txt file
with open('~/Documents/Bot-Finanzas/db/commands.txt', encoding='utf8') as f:
    lines = f.read()

# auxiliar variables
cols_trans = ['Tipo', 'Cuenta', 'Cantidad', 'Fecha', 'Descripción']

# auxiliar functions
def lastn_request(message):
	line = message.text.lower().split()
	if len(line) >= 2 and line[0] == 'last':
		return True
	else:
		return False		 

# Bot
bot = tb.TeleBot(bot_token)

print('Iniciado')

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Bot de Finanzas Personales iniciado")

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.send_message(message.chat.id, lines, parse_mode="markdown")

@bot.message_handler(func=lastn_request)
def lastn_trans(message):
	line = message.text.lower().split()

	try:
		n_rows = min(int(line[1]), len(transactions))
	
	except ValueError:
		bot.send_message(message.chat.id, 'Please especify the number of rows')

	dfi.export(transactions[cols_trans].tail(n_rows), '~/Documents/Bot-Finanzas/images/lastn.png')

	bot.send_photo(message.chat.id, open('~/Documents/Bot-Finanzas/images/lastn.png', 'rb'))
	

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.send_message(message.chat.id, 'How can I help you?')

bot.infinity_polling()

print('Listo')