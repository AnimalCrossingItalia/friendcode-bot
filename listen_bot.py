#!/usr/bin/python2.7

import os
import time

import telepot
from telepot.loop import MessageLoop

from Modules.DataManager import DataManager


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
        output = data.displayperson(chat_id, args[1])
        if len(output) == 0:
            bot.sendMessage(chat_id, "")
        else:
            msg = args[1] + "\n\n"
            for row in output:
                msg += row[0] + " " + row[1]
            bot.sendMessage(chat_id, msg)  # stampa output

    elif command.startswith('/delete'):
        args = command.split(' ')
        removed = data.removecode(chat_id, args[1], args[2])
        if removed == 0:
            bot.sendMessage(chat_id, 'Record non trovato')  # conferma
        else:
            bot.sendMessage(chat_id, 'Record eliminato')  # conferma

    elif command.startswith('/insert'):
        args = command.split(' ')
        data.addcode(chat_id, args[1], args[2], args[3])
        # TODO: gestire eccezione per record gia esistente
        bot.sendMessage(chat_id, "Record creato")  # conferma


data = DataManager(os.environ['API-TOKEN'])
bot = telepot.Bot(os.environ['DATABASE_URL'])
me = bot.getMe()
print("Avvio bot in corso...")
print(me)

MessageLoop(bot, handle).run_as_thread()
print('Sono in ascolto...')

while 1:
    time.sleep(10)
