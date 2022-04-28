from pathlib import Path

import sqlite3
import datetime



class DataBaseManager:
    def __init__(self, db_name: str):
        db_path = 'src/database.db'
        self.conn = sqlite3.connect(db_path)

    def _execute(self, statement: str, values: list=[]):
        cursor = self.conn.cursor()
        cursor.execute(statement, values)
        return cursor


    def curent_date(self):
        curent_date = datetime.date.today().strftime('%d.%m.%Y')
        return str(curent_date)


    def create_table(self, table_name: str):
        self._execute(f"""CREATE TABLE IF NOT EXISTS {table_name}"""+ 
                      f"""(id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, title TEXT);""")

    
    def drop_table(self, table_name: str):
        self._execute(f"""DROP TABLE {table_name};""")

    
    def add_data(self, table_name: str, data: str):
        date = self.curent_date()
        values = date, data
        placeholders = ','.join('?' * len(values))

        self._execute(f"""INSERT INTO {table_name}"""+
                       """(date, title)"""+
                      f"""VALUES({placeholders});""",
                      values
                      )
        self.conn.commit()


    def retrieve_data(self, table_name: str):
        query = f"""SELECT * FROM {table_name} ORDER BY id"""
        results = self._execute(query).fetchall()

        return results

