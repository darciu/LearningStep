import sqlite3
from sqlite3 import Error
import datetime


class Database:
    """Class responsible for database connection"""

    def __init__(self):


        self.conn = self.create_connection('database.db')

        sql_create_tasks = """CREATE TABLE IF NOT EXISTS tasks(
                            task_id INTEGER PRIMARY KEY,
                            title TEXT NOT NULL,
                            language TEXT NOT NULL,
                            description TEXT NOT NULL,
                            code TEXT NOT NULL,
                            picture TEXT NOT NULL,
                            creation_date TEXT NOT NULL,
                            last_pass_date TEXT NOT NULL,
                            next_pass_date TEXT NOT NULL,
                            pass_count INTEGER NOT NULL
                            );
                            """
        sql_create_images = """CREATE TABLE IF NOT EXISTS images(
                            image_name TEXT NOT NULL,
                            image_blob BLOB NOT NULL,
                            image_ext TEXT NOT NULL);"""

        self.create_table(self.conn,sql_create_tasks)

        self.create_table(self.conn, sql_create_images)


    def create_connection(self,db_file):

        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return None



    def create_table(self,conn,sql_statement):
        """Create table"""
        try:
            cur = conn.cursor()
            cur.execute(sql_statement)
            conn.commit()

        except Error as e:
            print(e)

    def execute_sql(self,sql,dataset):
        """Executing given sql statement with dataset"""

        cur = self.conn.cursor()
        cur.execute(sql,dataset)
        self.conn.commit()

    def add_task(self,description_dict,code_dict,picture_dict,title, language):
        """Add new task to database"""

        creation_date = datetime.date.today()

        next_pass_date = creation_date + datetime.timedelta(days=1)

        sql = "INSERT INTO tasks(title,language,description,code, picture, creation_date,last_pass_date, next_pass_date,pass_count) VALUES (?,?,?,?,?,?,?,?,?)"

        dataset = (title,language,str(description_dict),str(code_dict),str(picture_dict), creation_date,"None",next_pass_date,0)

        self.execute_sql(sql,dataset)


    def load_available_tasks(self):
        """Returns available tasks"""

        now_time = datetime.date.today()

        sql = "SELECT title, language, creation_date, last_pass_date, pass_count, task_id FROM tasks WHERE next_pass_date <= ?"

        dataset = (str(now_time),)

        cur = self.conn.cursor()

        cur.execute(sql,dataset)

        rows = cur.fetchall()

        return rows


    def get_selected_task(self, task_id):
        """Returns selected (in table) task"""

        sql = "SELECT title, description, code, picture, pass_count FROM tasks WHERE task_id = ?"

        dataset = (int(task_id),)

        cur = self.conn.cursor()

        cur.execute(sql, dataset)

        row = cur.fetchone()

        return row[0], eval(row[1]), eval(row[2]), eval(row[3]), row[4]


    def update_task(self, task_id, pass_count):
        """If task is passed then updates"""
        last_pass_date = datetime.date.today()

        if pass_count == 0:

            next_pass_date = last_pass_date + datetime.timedelta(days=1)

        elif pass_count == 1:

            next_pass_date = last_pass_date + datetime.timedelta(days=3)

        elif pass_count == 2:

            next_pass_date = last_pass_date + datetime.timedelta(days=7)

        elif pass_count == 3:

            next_pass_date = last_pass_date + datetime.timedelta(days=10)

        elif pass_count == 4:

            next_pass_date = last_pass_date + datetime.timedelta(days=14)

        elif pass_count == 5:

            next_pass_date = last_pass_date + datetime.timedelta(days=28)

        elif pass_count == 6:

            next_pass_date = last_pass_date + datetime.timedelta(days= 60)

        elif pass_count == 7:

            next_pass_date = last_pass_date + datetime.timedelta(days= 90)

        else:

            next_pass_date = last_pass_date + datetime.timedelta(days= 180)


        pass_count += 1


        sql = "UPDATE tasks SET last_pass_date = ?, next_pass_date = ?, pass_count = ? WHERE task_id = ?"

        dataset = (last_pass_date, next_pass_date, pass_count, task_id)

        self.execute_sql(sql,dataset)

        return str(next_pass_date)

    def check_if_task_id_exists(self, task_id):
        """Returns True or False if given task id exists in database"""

        sql = "SELECT task_id FROM tasks WHERE task_id = ?"

        dataset = (task_id,)

        cur = self.conn.cursor()

        cur.execute(sql, dataset)

        row = cur.fetchone()

        if row is not None:

            return True

        else:
            return False


    def delete_task(self, task_id):
        """Delete task"""
        sql = "DELETE FROM tasks WHERE task_id = ?"

        dataset = (task_id,)

        try:

            self.execute_sql(sql,dataset)

        except:

            print('Error!')



    ##### IMAGES #########

    def convertToBinaryData(self, filename):

        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

    def insertBLOB(self,image_name, image_path, image_ext):
        """Insert image as BLOB to the database"""
        try:



            sql = """ INSERT INTO images (image_name, image_blob, image_ext) VALUES (?, ?, ?)"""

            image_blob = self.convertToBinaryData(image_path)

            # Convert data into tuple format

            dataset = (image_name, image_blob, image_ext)

            self.execute_sql(sql, dataset)


        except sqlite3.Error as error:

            print("Failed to insert blob data into sqlite table", error)

