import sqlite3
from sqlite3 import Error



class Database:

    def __init__(self):


        self.conn = self.create_connection('database.db')

        sql_create_tasks = """CREATE TABLE IF NOT EXISTS tasks(
                            task_id integer PRIMARY KEY,
                            title text NOT NULL,
                            language text NOT NULL,
                            description text NOT NULL,
                            code text NOT NULL,
                            creation_date text NOT NULL,
                            last_pass_date text NOT NULL,
                            next_pass_date text NOT NULL,
                            pass_count integer NOT NULL
                            );
                            """
        self.create_table(self.conn,sql_create_tasks)


    def create_connection(self,db_file):

        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return None



    def create_table(self,conn,sql_statement):
        try:
            cur = conn.cursor()
            cur.execute(sql_statement)
            conn.commit()

        except Error as e:
            print(e)