import telebot as tb
import pandas as pd
# import matplotlib.pyplot as plt
import dataframe_image as dfi
from auxiliar import bot_token

#### config
## columns format, float as currency
pd.options.display.float_format = '${:,.2f}'.format

#### read csv
transactions = pd.read_csv('~/Documents/Bot-Finanzas/db/movimientos.csv', encoding='utf-8')
accounts = pd.read_csv('~/Documents/Bot-Finanzas/db/cuentas.csv', encoding='utf-8')

#### column formating
transactions['Cantidad'] = transactions['Cantidad'].replace('[^-.0-9]', '', regex=True).astype(float)

#### read availables commands from the txt file
with open('/home/pi/Documents/Bot-Finanzas/commands.txt', encoding='utf-8') as f:
    lines = f.read()

#### auxiliar variables
cols_trans = ['Tipo', 'Cuenta', 'Cantidad', 'Fecha', 'Descripción']

#### auxiliar functions

## functions for the handlers
def lastn_request(message):
	line = message.text.lower().split()
	if len(line) >= 2 and line[0] == 'last':
		return True
	else:
		return False

## others functions
def saves_png(df, img_name, path):
	dfi.export(df, f'{path}{img_name}.png', table_conversion='matplotlib')

def groupby_sum(df, cols_names, cols_sum):
	return df.groupby(cols_names, as_index=False)[[cols_sum]].sum()

#### Bot
bot = tb.TeleBot(bot_token)

print('Iniciado')

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Bot de Finanzas Personales iniciado")

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.send_message(message.chat.id, lines, parse_mode="markdown")

#@bot.message_handler(commands=['stop'])
#def stop_bot(message):
#	bot.stop_polling()

@bot.message_handler(func=lastn_request)
def lastn_trans(message):
	line = message.text.lower().split()

	try:
		n_rows = min(int(line[1]), len(transactions))

	except ValueError:
		bot.send_message(message.chat.id, 'Please especify the number of rows')
		return

	saves_png(transactions[cols_trans].tail(n_rows), 'lastn', '/home/pi/Documents/Bot-Finanzas/images/')

	bot.send_photo(message.chat.id, open('/home/pi/Documents/Bot-Finanzas/images/lastn.png', 'rb'))

@bot.message_handler(regexp='^[Ss]umm *.*')
def summary(message):
	line = message.text.lower().split()

	if len(line) == 1:
		# summary with all the accounts
		df = groupby_sum(transactions, ['Cuenta'], 'Cantidad')

	elif line[1] == 'debit':
		# summary filtering out credit
		df = transactions[transactions['Tipo'] != 'Crédito']
		df = groupby_sum(df, ['Cuenta'], 'Cantidad')
	
	elif line[1] == 'credit':
		# summary filtering out debit
		df = transactions[transactions['Tipo'] == 'Crédito']
		df = groupby_sum(df, ['Cuenta'], 'Cantidad')

	try:
		saves_png(df, 'summary', '/home/pi/Documents/Bot-Finanzas/images/')
		bot.send_photo(message.chat.id, open('/home/pi/Documents/Bot-Finanzas/images/summary.png', 'rb'))
	
	except:
		bot.reply_to(message, 'Please send the correct filter for the instruction')
	
	bot.send_message(message.chat.id, str(len(line)))


@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.send_message(message.chat.id, 'How can I help you?')

print('Before infinity polling')

bot.infinity_polling()

print('After infinity polling')

print('Listo')