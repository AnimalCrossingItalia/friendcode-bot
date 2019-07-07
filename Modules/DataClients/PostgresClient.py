import psycopg2


# helper class that eases the communication with application's DB
class DataManager:

    # Constructur sets the database's url
    def __init__(self, databaseurl):
        self.databaseurl = databaseurl

    # Add a new friend code in the DB
    def addcode(self, chat, name, key, friendcode):
        retval = 0  # default return value, returned in case of error
        try:
            db = psycopg2.connect( self.databaseurl, sslmode='require' )
            cur = db.cursor()
            # check if the same code already exists
            qstring = """SELECT * FROM data WHERE "chat"=%s AND "user"=%s and "key"=%s"""
            cur.execute( qstring, [chat, name, key] )
            if len( cur.fetchall()
                    ) == 0:  # if not insert it and return 2 (success)
                instring = """INSERT INTO data("user", "chat", "key", "code") VALUES (%s, %s, %s, %s);"""
                cur.execute( instring, [name, chat, key, friendcode] )
                db.commit()
                retval = 2
            else:  # if yes returs 1 (duplicate error)
                retval = 1
        except psycopg2.DatabaseError as error:
            print( error )
        finally:
            cur.close()
            db.close()
            return retval

    # remove a friend code from the DB
    def removecode(self, chat, name, key):
        retval = 0  # default return value, returned in case of error
        try:
            db = psycopg2.connect(self.databaseurl, sslmode='require')
            delstring = """DELETE FROM data WHERE "chat"=%s AND "user"=%s AND "key"=%s"""
            cur = db.cursor()
            cur.execute( delstring, [chat, name, key] )
            if cur.rowcount == 0:  # If any row wasn't deleted return 1 (code not found)
                retval = 1
            else:  # Else return 2 (success)
                retval = 2
            db.commit()  # update the DB
        except psycopg2.DatabaseError as error:
            print( error )
        finally:
            cur.close()
            db.close()
            return retval

    # search a person and get all of this codes
    def queryperson(self, chat, name):
        rows = False  # var rows is initialized with False (default value returned in case of error)
        try:
            db = psycopg2.connect(self.databaseurl, sslmode='require')
            # query: search in the DB persons from the current chat with a given name
            qstring = """SELECT "key","code" FROM data WHERE "chat"=%s AND "user"=%s"""
            cur = db.cursor()
            cur.execute( qstring, [chat, name] )
            rows = cur.fetchall(
            )  # if the query worked get a list of the results ( key,code ) tuples
        except psycopg2.DatabaseError as error:
            print( error )
        finally:
            cur.close()
            db.close()
            return rows  # return results ( or false in case of error )

    def listall(self, chat):
        users_codes = False  # var users_codes is initialized with False (default value returned in case of error)
        try:
            db = psycopg2.connect( self.databaseurl, sslmode='require' )
            # query: get every registered person of a chat without repeating them
            q1string = """SELECT DISTINCT("user") FROM data WHERE "chat"=%s ORDER BY "user";"""
            cur = db.cursor()
            cur.execute( q1string, [str( chat )] )
            users = cur.fetchall(
            )  # get a list of users (not chat users, persons registered in the bot!)
            users_codes = {}  # transform users_codes in a dictionary
            for user in users:  # for every user...
                codes = self.queryperson( chat,
                                          user[0] )  # ...get his friend codes...
                # ...put the list of his friend codes as a value on the returned dictionary (name is the key)
                users_codes[user[0]] = codes
        except psycopg2.DatabaseError as error:
            print( error )
        finally:
            cur.close()
            db.close()
            return users_codes
