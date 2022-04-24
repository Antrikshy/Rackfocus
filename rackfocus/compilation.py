import os, shutil, gzip, urllib.request

from .models import DatasetModel
from .database import DatabaseController

class Compiler:
    def __init__(self, working_dir, output_loc):
        self.working_dir = working_dir
        self.output_loc = output_loc
        os.makedirs(self.working_dir, exist_ok=True)
        os.makedirs(self.output_loc, exist_ok=True)
        self.db = DatabaseController(output_loc)

    def fetch_datasets(self):
        for model_class in DatasetModel.__subclasses__():
            model = model_class()
            output_file = os.path.join(self.working_dir, model.get_file_name())
            download_url = model.get_download_url()
            print("Downloading dataset: {}".format(output_file))
            with urllib.request.urlopen(download_url) as response, open(output_file, 'wb') as out:
                shutil.copyfileobj(response, out)

    def cleanup_datasets(self, delete_db=False):
        shutil.rmtree(self.working_dir)
        """In case of unexpected interruptions that require cleanup"""
        if delete_db:
            self.close_database()
            self.db.delete_db()

    def setup_database(self):
        """Primes database connections, drops and re-creates all tables."""
        print("Resetting database.")
        self.db.prepare_db()

    def write_database(self):
        for model_class in DatasetModel.__subclasses__():
            model = model_class()
            print("Writing {} to database...".format(model.name))
            downloaded_file_path = os.path.join(self.working_dir, model.get_file_name())
            with gzip.open(downloaded_file_path, 'rb') as file:
                file.readline()
                for line in file:
                    line_str = line.decode('utf-8')
                    data = model.convert_line_to_tuples(line_str)
                    self.db.write_to_table(model.get_database_table_name(), data)
            self.db.commit_db()

    def close_database(self):
        self.db.commit_db()
        self.db.close_db()
