#!/usr/bin/python2.7

import os
import time

import telepot
from telepot.loop import MessageLoop

from Modules.DataManager import DataManager


# Check if message sender is admin to lock or unlock admin only commands
def isadmin(msg):
    retval = False  # Default return value
    admins = bot.getChatAdministrators(
        msg['chat']['id'] )  # Get a list of groups admins
    for admin in admins:  # For each admin...
        if admin['user'] == msg['from']:  # ...if he's the message sender...
            retval = True  # ...return true and break the cycle.
            break
    return retval


def handle(msg):
    # variables set-up
    chat_id = msg['chat']['id']
    command = msg['text']
    is_admin = isadmin( msg )

    # check if the chat is a group or not
    if msg['chat']['type'] != 'group' and msg['chat']['type'] != 'supergroup':
        bot.sendMessage(chat_id, "Questo bot va eseguito da un gruppo!")
        exit(1)

    # command logging
    print('Comando ricevuto: ' + command)

    # commands
    if command.startswith('/ping'):
        bot.sendMessage(chat_id, "pong!")

    # display information about the programs
    elif command.startswith( '/about' ):
        bot.sendMessage( chat_id, """Friend Code Bot
versione 1.0.1 (build 23/09/2018)
        
creato e mantenuto da:
Emiliano Sandri (www.emilianosandri.it)
Stefano Di Pasquale (http://www.stefaniscion.altervista.org/)
        
il codice sorgente del bot è disponibile su:
https://github.com/Stefaniscion/friendcode-bot""" )

    # display the bot commands explanations
    elif command.startswith( '/help' ) or command.startswith( '/man' ):
        bot.sendMessage( chat_id, """Friend Code Bot
Questo bot permette di memorizzare i codici amico del gruppo.
        
COMANDI:
Inserire nuovi codici (solo amministratori):
/ins  [nome]  [etichetta]  [codice amico]
        
Eliminare un codice (solo amministratori):
/del  [nome]  [etichetta]
        
Richiamare i codici associati ad una persona:
/find  [nome]
        
Vedere tutti i codici del gruppo:
/list
        
Nota: tutti i parametri dei comandi vanno separati con due spazi
        
SIGNIFICATO PARAMETRI:
nome -> il nome della persona a cui è associato il codice (es. "Mario", "Paolo R")
etichetta -> la descrizione del codice (es. "Switch", "3DS", "Wii U", "3DS EU", "3DS JAP")
codice -> il codice amico da memorizzare (es. "1234-5678-9012")
        """ )

    # given a name get all his friend codes
    elif command.startswith( '/find' ) or command.startswith( '/query' ):
        args = command.split(
            '  ' )  # split the message text in an array made by command + args
        if len(
                args
        ) == 2:  # if the array contains 2 elements (command + 1 argument)...
            output = data.queryperson(
                chat_id, args[1] )  # search codes for the requested person
            if output == False:  # if the method returns false an error happened
                bot.sendMessage( chat_id,
                                 "Errore di sistema, riprova più tardi." )
            else:
                if len(
                        output
                ) == 0:  # if the query didn't returned results write it to the user.
                    bot.sendMessage(
                        chat_id,
                        "Non è stato trovato nessun codice per il nome richiesto"
                    )
                else:  # else write the searched person names and all the codes in a string then send it.
                    msg = args[1] + "\n"
                    for row in output:
                        msg += row[0] + " " + row[1] + "\n"
                    bot.sendMessage( chat_id, msg )  # print output
        else:  # if the user gives the command in a bad format display explanation
            bot.sendMessage( chat_id, "Utilizzo comando: /query  [nome]" )

    # list all codes of the group
    elif command.startswith( '/list' ) or command.startswith( '/listall' ):
        user_codes = data.listall(
            chat_id )  # ask all codes of the current group
        output = "Lista dei codici amico del gruppo\n\n"
        for (user, codes) in user_codes.items():
            output += user + "\n"
            for code in codes:
                output += code[0] + " " + code[1] + "\n"
            output += "\n"
        bot.sendMessage( chat_id, output )

    # delete a code
    elif command.startswith( '/del' ) or command.startswith( '/delete' ):
        if is_admin:  # check if user is admin
            args = command.split( '  ' )
            if len( args ) == 3:
                retval = data.removecode(
                    chat_id, args[1], args[2] )  # remove the code from database
                if retval == 2:
                    bot.sendMessage(
                        chat_id,
                        'Record eliminato' )  # elimination confirmation
                elif retval == 1:
                    bot.sendMessage( chat_id,
                                     'Record non trovato' )  # record not found
                else:
                    bot.sendMessage( chat_id,
                                     "Errore di sistema, riprova più tardi."
                                     )  # system error
            else:
                bot.sendMessage(
                    chat_id, "Utilizzo comando: /delete  [nome]  [etichetta]" )
        else:
            bot.sendMessage(
                chat_id,
                "Questo comando può essere usato solo dagli amministratori del gruppo"
            )

    elif command.startswith( '/add' ) or command.startswith( '/insert' ):  # insert new code
        if is_admin:  # check if admin
            args = command.split( '  ' )
            if len( args ) == 4:
                retval = data.addcode( chat_id, args[1], args[2],
                                       args[3] )  # insert the code
                if retval == 2:
                    bot.sendMessage( chat_id, "Record creato" )  # confirmation
                elif retval == 1:
                    bot.sendMessage( chat_id,
                                     "Record già esistente" )  # duplicate error
                else:
                    bot.sendMessage( chat_id,
                                     "Errore di sistema, riprova più tardi."
                                     )  # system error
            else:
                bot.sendMessage(
                    chat_id,
                    "Utilizzo comando: /insert  [nome]  [etichetta]  [codice amico]"
                )
        else:
            bot.sendMessage(
                chat_id,
                "Questo comando può essere usato solo dagli amministratori del gruppo"
            )


data = DataManager(os.environ['DATABASE_URL'])
bot = telepot.Bot(os.environ['API-TOKEN'])

me = bot.getMe()
print("Avvio bot in corso...")
print(me)

MessageLoop(bot, handle).run_as_thread()
print('Sono in ascolto...')

while 1:
    time.sleep(10)
