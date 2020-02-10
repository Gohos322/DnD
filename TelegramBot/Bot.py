# -*- coding: utf-8 -*- 

import os
from flask import Flask, request
import telebot
import random
from bs4 import BeautifulSoup
import urllib.request

#===============================================================================
# Command List

# session - reports the day and hour of the next session
# compendium - provides the roll20.net link pointing to the word or words following the command
# version - provides the changelog of the current version
# arcana - provides the link to the latest Unearthed Arcana
# roll20 - roll a d20
# roll10 - roll a d10
# roll8 - roll a d8
# roll6 - roll a d6
# roll4 - roll a d4
#===============================================================================



TOKEN = '---Insert Your Bot Token Here---'
bot = telebot.TeleBot(token=TOKEN)
server = Flask(__name__)
date = '---Insert the date of the next session here---'
hour = '---Insert the hour of the next session here'
not_planned = 'The day of the next session is not decided yet. Hurry up and pick a date!'
session = "---Insert your party member's name here--- will met on " + date + ' at the ' + hour + " o'clock"
news= "---Insert the changelog here---"


#reports the day and hour of the next session. If not planned, replace "session" with "not_planned"
@bot.message_handler(commands=['session'])
def res_giocata(message):
    bot.reply_to(message, session)

#roll a d20
@bot.message_handler(commands=['roll20'])
def res_d20(message):
    d20 = None
    if d20 == None:
        d20 = 'Hai lanciato un ' + str(random.randint(1,20))
    bot.reply_to(message, d20)
    
#roll a d10
@bot.message_handler(commands=['roll10'])
def res_d10(message):
    d10 = None
    if d10 == None:
        d10 = 'Hai lanciato un ' + str(random.randint(1,10))
    bot.reply_to(message, d10)
    
#roll a d8
@bot.message_handler(commands=['roll8'])
def res_d8(message):
    d8 = None
    if d8 == None:
        d8 = 'Hai lanciato un ' + str(random.randint(1,8))
    bot.reply_to(message, d8)
    
#roll a d6
@bot.message_handler(commands=['roll6'])
def res_d6(message):
    d6 = None
    if d6 == None:
        d6 = 'Hai lanciato un ' + str(random.randint(1,6))
    bot.reply_to(message, d6)
    
#roll a d4    
@bot.message_handler(commands=['roll4'])
def res_d4(message):
    d4 = None
    if d4 == None:
        d4 = 'Hai lanciato un ' + str(random.randint(1,4))
    bot.reply_to(message, d4)


#provides the roll20.net link pointing to the word or words following the command "/compendium"
@bot.message_handler(func=lambda msg: msg.text is not None and '/compendium' in msg.text)
def res_spell(message):
    texts = message.text.split()
    idx = texts.index('/compendium')
    slice = texts[idx+1:]
    string = ' '.join(slice)
    compendium = string.replace(' ', '%20')
    bot.reply_to(message, "I may have found what you're looking for:\n" + 'https://roll20.net/compendium/dnd5e/' + compendium)

#provides the changelog of the current version
@bot.message_handler(commands=['version'])
def res_versione(message):
    bot.reply_to(message, news)

#provides the link to the latest Unearthed Arcana
@bot.message_handler(commands=['arcana'])
def res_arcana(message):
	page = urllib.request.urlopen("https://dnd.wizards.com/articles/unearthed-arcana")
	html = page.read()
	soup = BeautifulSoup(html, 'html.parser')
	anchor = soup.find_all('a', attrs={"class": "image"})
	articles = []
	for i in anchor:
		articles.append(i.get('href'))
	arcana = articles[0]
	url = 'https://dnd.wizards.com' + arcana
	bot.reply_to(message, url)

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://telegram-bot-for-dnd.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
