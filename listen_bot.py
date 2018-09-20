#!/usr/bin/python2.7

#telepot
import telepot
#loop
import time
from telepot.loop import MessageLoop

def handle(msg):
	#set-up variabili
	chat_id = msg['chat']['id']
	command = msg['text']

	#permessi di utilizzo
  #if msg['from']['id'] != USER_ID:
	if false: 
        	bot.sendMessage(chat_id, "Mi dispiace! Questo e un bot privato! Accesso negato!")
        	exit(1)

	#log comandi
	print 'Comando ricevuto: ' + command

	#comandi
	if command == '/ping':
		bot.sendMessage(chat_id, "pong!")
  elif command == '/list':
    bot.sendMessage(chat_id, "lista")
    
#Bot Token
bot = telepot.Bot('TOKEN')
me=bot.getMe()
print "Avvio bot in corso..."
print me

MessageLoop(bot, handle).run_as_thread()
print 'Sono in ascolto...'

while 1:
    time.sleep(10)
