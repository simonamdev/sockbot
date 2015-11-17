import sqlite3
import os


class PysqliteError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Pysqlite:
    def __init__(self, database_name='', database_file=''):
        self.dbname = database_name
        if os.path.isfile(database_file) and os.access(database_file, os.R_OK):
            self.dbcon = sqlite3.connect(database_file)
            self.dbcur = self.dbcon.cursor()
        else:
            raise PysqliteError('{} could not be found or cannot be accessed!'.format(self.dbname))

    def get_db_data(self, table):
        try:
            db_data = self.dbcur.execute('SELECT * FROM {}'.format(table))
        except Exception as e:
            raise PysqliteError('Pysqlite experienced the following exception: {}'.format(e))
        data_list = []
        for row in db_data:
            data_list.append(row)
        if len(data_list) == 0:
            raise PysqliteError('Pysqlite found no data in the table: {} in the DB: {}'.format(table, self.dbname))
        return data_list

    def insert_db_data(self, table, row_string, db_data):
        try:
            self.dbcur.execute('INSERT INTO {} VALUES {}'.format(table, row_string), db_data)
            self.dbcon.commit()
        except Exception as e:
            raise PysqliteError('Pysqlite experienced the following exception: {}'.format(e))

if __name__ == '__main__':
    ggforcharity_db = Pysqlite('GGforCharity', 'ggforcharity.db')
    data = ggforcharity_db.get_db_data('testing')
    for row in data:
        print(row)
    ggforcharity_db.insert_db_data('testing', '(NULL, ?, ?, ?, ?, ?)', ('Day String', 100, 20, 'Event', 'purrcat259'))
    for row in data:
        print(row)
