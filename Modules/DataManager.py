import psycopg2

class DataManager:

    def __init__(self, databaseURL):
        self.db = psycopg2.connect(databaseURL, sslmode='require')

    def __init__(self, server, database, user, password):
        self.db = psycopg2.connect(host=server, database=database, user=user, password=password)

        def addcode(self, chat, name, key, friendCode):
            instring = """INSERT INTO data(user,chat,key,code) VALUES(%s,%s,%s,%s) RETURNING vendor_id;"""

            cur = self.db.cursor()
            cur.execute(instring, (name, chat, key, friendCode))
            cur.Commit()
            cur.close()

        def removecode(self, chat, name, key):
            delstring = """DELETE FROM data WHERE chat=%s AND name=%s AND key=%s"""

            cur = self.db.cursor()
            cur.execute(delstring, (chat, name, key))
            rows_deleted = cur.rowcount
            cur.Commit()
            cur.close()
            return rows_deleted

        def displayperson(self, chat, name):
            qstring = """SELECT * FROM data WHERE chat=%s AND name=%s"""

            cur = self.db.cursor()
            cur.execute(qstring, (chat, name))
            rows = cur.fetchall()
            cur.close()
            return rows
