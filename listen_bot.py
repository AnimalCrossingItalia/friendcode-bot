#!/usr/bin/python2.7

import telepot
import time
import sys

from telepot.loop import MessageLoop

from Modules.DataManager import DataManager

def

def handle(msg):
    # set-up variabili
    chat_id = msg['chat']['id']
    command = msg['text']

    # condizione permesso negato
    if msg['chat']['type'] != 'group' and msg['chat']['type'] != 'supergroup':
        bot.sendMessage(chat_id, "Questo bot va eseguito da un gruppo!")
        exit(1)

    # logging comandi
    print('Comando ricevuto: ' + command)

    # comandi
    if command.startswith('/ping'):
        bot.sendMessage(chat_id, "pong!")

    elif command.startswith('/msg'):
        bot.sendMessage(chat_id, msg)

    elif command.startswith('/query'):
        args = command.split(' ')
        # inserire comando per query, usare "args[1]" come parametro
        # gestire eccezione per record non trovato
        output = ' '  # inserire il risultato della query in "output"
        bot.sendMessage(chat_id, output)  # stampa output

    elif command.startswith('/delete'):
        args = command.split(' ')
        # inserire comando per insert, usare "args[1]" come parametro
        # gestire eccezione per record non trovato
        bot.sendMessage(chat_id, 'Record eliminato')  # conferma

    elif command.startswith('/insert'):
        args = command.split(' ')
        # inserire comando per delete, usare "args[1]" come parametro
        # gestire eccezione per record gia esistente
        bot.sendMessage(chat_id, "Record creato")  # conferma


data = DataManager(sys.argv[2], sys.argv[3], sys.argv[4]. sys.argv[5])
bot = telepot.Bot(sys.argv[1])
me = bot.getMe()
print("Avvio bot in corso...")
print(me)

MessageLoop(bot, handle).run_as_thread()
print('Sono in ascolto...')

while 1:
    time.sleep(10)
