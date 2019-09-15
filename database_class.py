import sqlite3
from sqlite3 import Error
import datetime


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

    def execute_sql(self,sql,dataset):

        cur = self.conn.cursor()
        cur.execute(sql,dataset)
        self.conn.commit()

    def add_task(self,description_dict,code_dict,title, language):

        creation_date = datetime.date.today()

        next_pass_date = creation_date + datetime.timedelta(days=1)

        sql = "INSERT INTO tasks(title,language,description,code,creation_date,last_pass_date, next_pass_date,pass_count) VALUES (?,?,?,?,?,?,?,?)"

        dataset = (title,language,str(description_dict),str(code_dict),creation_date,"None",next_pass_date,0)

        self.execute_sql(sql,dataset)


    def load_available_tasks(self):

        now_time = datetime.date.today()

        sql = "SELECT title, language, creation_date, last_pass_date, pass_count, task_id FROM tasks WHERE next_pass_date <= ?"

        dataset = (str(now_time),)

        cur = self.conn.cursor()

        cur.execute(sql,dataset)

        rows = cur.fetchall()

        return rows
