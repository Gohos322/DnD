import telebot
import time
import random


#===============================================================================
# start - attiva il bot
# giocata - riferisce la data e l'ora della prossima giocata
# info - mostra il link drive in cui sono raccolte le informazioni sugli avvenimenti importanti
# help - dichiara la funzione del bot
# spell - fornisce il link di dndbeyond della spell richiesta
# verme - chiede scusa
# roll20 - lancia un d20
# roll10 - lancia un d10
# roll8 - lancia un d8
# roll6 - lancia un d6
# roll4 - lancia un d4
#===============================================================================



bot_token = '1014485534:AAHfgoHTQ9xG_PAq3DlCfKmvujieWnpnmAc'
bot = telebot.TeleBot(token=bot_token)
data = ''
orario = ''
giocata = 'add your charachter name here, they will meet this day ->' + data + 'at this hour ->' + orario
drive = 'Per avere tutte le informazioni clicca qui    https://drive.google.com/open?id=17wt-Uu2c4kbbd94qS-qptFhfOYODTRvK'




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


@bot.message_handler(func=lambda msg: msg.text is not None and '/spell' in msg.text)
def res_spell(message):
    texts = message.text.split()
    idx = texts.index('/spell')
    slice = texts[idx+1:]
    string = ' '.join(slice)
    spell = string.replace(' ', '%20')
    bot.reply_to(message, 'https://roll20.net/compendium/dnd5e/' + spell)


@bot.message_handler(commands=['verme'])
def res_verme(message):
    bot.reply_to(message, 'Sono un verme verminoso e ho sbagliato a contraddire il padrone')


while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(3)
