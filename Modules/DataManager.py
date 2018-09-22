import psycopg2

class DataManager:

    def __init__(self, databaseurl):
        self.db = databaseurl

    def addcode(self, chat, name, key, friendCode):
        try:
            db = psycopg2.connect(databaseurl, sslmode='require')
            instring = """INSERT INTO data(user,chat,key,code) VALUES(%s,%s,%s,%s) RETURNING vendor_id;"""
            cur = db.cursor()
            cur.execute(instring, (name, chat, key, friendCode))
            cur.Commit()
        except:
            print("Errore SQL!")
        finally:
            cur.close()
            db.close()

    def removecode(self, chat, name, key):
        rows_deleted = 0
        try:
            db = psycopg2.connect(self.databaseurl, sslmode='require')
            delstring = """DELETE FROM data WHERE chat=%s AND name=%s AND key=%s"""
            cur = db.cursor()
            cur.execute(delstring, (chat, name, key))
            rows_deleted = cur.rowcount
            cur.Commit()
        except:
            print("Errore SQL!")
        finally:
            cur.close()
            db.close()
            return rows_deleted


    def displayperson(self, chat, name):
        try:
            db = psycopg2.connect(self.databaseurl, sslmode='require')
            qstring = """SELECT * FROM data WHERE chat=%s AND name=%s"""
            cur = db.cursor()
            cur.execute(qstring, (chat, name))
            rows = cur.fetchall()
        except:
            print("Errore SQL!")
        finally:
            cur.close()
            db.close()
            return rows
