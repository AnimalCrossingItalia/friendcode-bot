#!/usr/bin/python2.7

import telepot
import time
from telepot.loop import MessageLoop

def handle(msg):
	#set-up variabili
	chat_id = msg['chat']['id']
	command = msg['text']

	#condizione permesso negato
	if false: 
        	bot.sendMessage(chat_id, "Mi dispiace! Questo e un bot privato! Accesso negato!")
        	exit(1)

	#logging comandi
	print 'Comando ricevuto: ' + command

	#comandi
	if command == '/ping':
		bot.sendMessage(chat_id, "pong!")
	
	elif command == '/chatid':
		bot.sendMessage(chat_id, chat_id)
  	
	elif command.startswith('/query'):
		args = command.split(' ')
		#inserire comando per query, usare "args[1]" come parametro
		#gestire eccezione per record non trovato
		output = ' ' #inserire il risultato della query in "output"
		bot.sendMessage(chat_id,output) #stampa output
	
	elif command.startswith('/insert'):
		args = command.split(' ')
		#inserire comando per insert, usare "args[1]" come parametro
		#gestire eccezione per record non trovato
		bot.sendMessage(chat_id,'Record eliminato') #conferma
		
	elif command.startswith('/delete'): 
		args = command.split(' ')
		#inserire comando per delete, usare "args[1]" come parametro
		#gestire eccezione per record già esistente
		bot.sendMessage(chat_id,"Record creato") #conferma
    
#Bot Token
bot = telepot.Bot('TOKEN')
me=bot.getMe()
print "Avvio bot in corso..."
print me

MessageLoop(bot, handle).run_as_thread()
print 'Sono in ascolto...'

while 1:
    time.sleep(10)
