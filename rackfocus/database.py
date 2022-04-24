import os
import sqlite3

from .models import DatasetModel

class DatabaseController:
    _OUTPUT_FILE_NAME = 'rackfocus_out.db'

    def __init__(self, output_loc):
        self.output_loc = output_loc
        self.conn = sqlite3.connect(self._db_location)
        self.cursor = self.conn.cursor()

    @property
    def _db_location(self):
        return os.path.join(self.output_loc, self._OUTPUT_FILE_NAME)

    def _create_table(self, table_name, schema):
        self.cursor.execute('create table {} ({})'.format(table_name, schema))
        self.commit_db()

    def _drop_table(self, table_name):
        self.cursor.execute('drop table if exists {}'.format(table_name))
        self.commit_db()

    def write_to_table(self, table_name, data):
        """`data` expected to be a tuple or a list thereof."""
        for item in data:
            self.cursor.execute('insert into {} values ({})'.format(table_name, ','.join('?' * len(item))), item)

    def prepare_db(self):
        """Wipes all tables and re-creates new tables. Relies on DatasetModel
        for both these operations."""
        for model_class in DatasetModel.__subclasses__():
            model = model_class()
            table_name = model.get_database_table_name()
            self._drop_table(table_name)
            self._create_table(table_name, model.get_database_table_schema())

    def commit_db(self):
        self.conn.commit()

    def close_db(self):
        self.conn.close()

    def delete_db(self):
        """Deletes the entire database file, used for cleanup on unexpected
        interruptions."""
        os.remove(self._db_location)
