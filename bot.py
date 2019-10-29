import telebot

TOKEN = '911229343:AAH3m3tdbeKlnzp5OV-JOZwM0ZPVZs_BHTo'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
	bot.send_message(
		message.chat.id,
		'Hue-moe, kakie vesti?')

bot.polling(none_stop=True)
