# -*- coding: utf-8 -*- 

import os
from flask import Flask, request
import telebot
import random


#===============================================================================
# start - attiva il bot
# giocata - riferisce la data e l'ora della prossima giocata
# info - mostra il link drive in cui sono raccolte le informazioni sugli avvenimenti importanti
# help - dichiara la funzione del bot
# compendio - fornisce il link di roll20 dell'informazione richiesta
# verme - chiede scusa
# versione - riferisce le note dell'ultima versione
# lodami - elargisce delle lodi
# roll20 - lancia un d20
# roll10 - lancia un d10
# roll8 - lancia un d8
# roll6 - lancia un d6
# roll4 - lancia un d4
#===============================================================================



TOKEN = '1014485534:AAHfgoHTQ9xG_PAq3DlCfKmvujieWnpnmAc'
bot = telebot.TeleBot(token=TOKEN)
server = Flask(__name__)
data = '30/01/2020'
orario = '16:30'
giocata = 'Azhag, Mazekeen, Daylen, Sariel e Sif si incontreranno il ' + data + ' alle ore ' + orario
drive = 'Per avere tutte le informazioni clicca qui\nhttps://drive.google.com/open?id=17wt-Uu2c4kbbd94qS-qptFhfOYODTRvK'
news= "Versione 1.1\nAggiunto il comando /versione, per avere informazioni sulle ultime modifiche a Carletto.\nIl comando /spell è diventato /compendio.  Ora può trovare qualunque entry in roll20.\nAggiunto il comando /lodami, perchè sentirsi gratificati è sempre importante"




@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Pronto a servire il padrone')

@bot.message_handler(commands=['giocata'])
def res_giocata(message):
    bot.reply_to(message, giocata)

@bot.message_handler(commands=['info'])
def res_info(message):
    bot.reply_to(message, drive)

@bot.message_handler(commands=['help'])
def res_help(message):
    bot.reply_to(message, 'Il mio padrone mi ha creato per organizzare al meglio le giocate')

@bot.message_handler(commands=['roll20'])
def res_d20(message):
    d20 = None
    if d20 == None:
        d20 = 'Hai lanciato un ' + str(random.randint(1,20))
    bot.reply_to(message, d20)
    

@bot.message_handler(commands=['roll10'])
def res_d10(message):
    d10 = None
    if d10 == None:
        d10 = 'Hai lanciato un ' + str(random.randint(1,10))
    bot.reply_to(message, d10)
    

@bot.message_handler(commands=['roll8'])
def res_d8(message):
    d8 = None
    if d8 == None:
        d8 = 'Hai lanciato un ' + str(random.randint(1,8))
    bot.reply_to(message, d8)
    

@bot.message_handler(commands=['roll6'])
def res_d6(message):
    d6 = None
    if d6 == None:
        d6 = 'Hai lanciato un ' + str(random.randint(1,6))
    bot.reply_to(message, d6)
    
    
@bot.message_handler(commands=['roll4'])
def res_d4(message):
    d4 = None
    if d4 == None:
        d4 = 'Hai lanciato un ' + str(random.randint(1,4))
    bot.reply_to(message, d4)


@bot.message_handler(func=lambda msg: msg.text is not None and '/compendio' in msg.text)
def res_spell(message):
    texts = message.text.split()
    idx = texts.index('/compendio')
    slice = texts[idx+1:]
    string = ' '.join(slice)
    compendio = string.replace(' ', '%20')
    bot.reply_to(message, 'Forse ho trovato quello che cercavi nella grande biblioteca:\n' + 'https://roll20.net/compendium/dnd5e/' + compendio)


@bot.message_handler(commands=['verme'])
def res_verme(message):
    bot.reply_to(message, 'Sono un verme verminoso e ho sbagliato a contraddire il padrone')
    
@bot.message_handler(commands=['lodami'])
def res_lodami(message):
    bot.reply_to(message, "Bene, signore.\nLei non solo è bello, ma potentissimo.\nIo sono pronto a fare qualunque cosa per servirla.\nLa dolce misericordia che mi concedete è il vero segno della vostra altissima nobiltà... Basta? Ok, sto zitto.")

@bot.message_handler(commands=['versione'])
def res_versione(message):
    bot.reply_to(message, news)

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://powerful-bayou-10660.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
