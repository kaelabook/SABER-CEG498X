import yaml
import sqlite3
from pathlib import Path
"""
Class: Database_SABER
Author: Spencer Mullins
Version: 0.0.1
Last Change: 11/23/25
Description:
SQLite database implemented to hold 2 tables config, and images. config holds configuration information loaded in from a yaml file.
Most of the relevant config information involves paths to other files.

TODO: 
Update to include other tables, configs, etc as time goes on. 
Need to update to store absolute paths programmatically for the config table, like in the image table.
Add docstrings for all methods and general comments.
Clean up unescesarry repetion.

"""
INSERT_IMAGE_PATH = "INSERT OR IGNORE INTO images (path) VALUES (?)"
INSERT_CONFIG = "INSERT OR IGNORE INTO config (type, path) VALUES (?, ?)"

class Database_SABER:
    def __init__(self):
        self.db_path = 'saber.db'

        self.config_path = Path('conf/saber_config.yaml')

        self.project_path = Path(__file__).resolve().parent
        self.db_path = self.project_path / self.db_path

        self.config_path = self.project_path / self.config_path


        self.db_conn = sqlite3.connect(str(self.db_path))
        self.db_cursor = self.db_conn.cursor()
        self._init_db()
#Setup and helpers
    def cleanup(self):
        self.db_conn.close()

    def _init_db(self):
        self._setup_config()
        self._setup_images()
        self._load_image_paths()
        self._load_in_config()

    def _setup_config(self):
        self.db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS config ( 
            id INTEGER PRIMARY KEY,
            type TEXT UNIQUE,
            path TEXT NOT NULL
            )
            ''')

    def _setup_images(self):
        self.db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS images ( 
            id INTEGER PRIMARY KEY,
            path TEXT UNIQUE,
            red INTEGER,
            circle INTEGER
            )
            ''')

    def _insert_to_db(self,insert_command, values_tuple, im_path=''):
        self.db_cursor.execute(insert_command, values_tuple )

    def _load_image_paths(self):
        with open(self.retrieve_config_path('config', 'image_list'), 'r') as f:
            for line in f:
                path_tuple = (str(self.project_path / Path(line.strip().replace("\n", ""))),)
                self._insert_to_db(INSERT_IMAGE_PATH, path_tuple)
            self.db_conn.commit()
    def reset_db(self):
        val = input('Are you sure you want to reset the database? (y/n) \n '
                    'This will drop all tables, only use for testing, do not use in production')
        if val == 'y' or val == 'Y':
            drop = "DROP TABLE IF EXISTS "
            self.db_cursor.execute(drop + 'config')
            self.db_cursor.execute(drop + 'images')
            self.db_conn.commit()
        elif val == 'n' or val == 'N':
            exit()
        else:
            exit()
    def _clean_query(self,result):
        result = str(result)
        result = result[2:len(result)-3]
        return result




    def _load_in_config(self):
        f = open(self.config_path, 'r+')
        conf = yaml.safe_load(f)
        image_rec_tuple = ('image_list',conf['image_rec']['list'])
        detection_list_tuple = ('detection_list',conf['image_rec']['output'])

        self._insert_to_db(INSERT_CONFIG, image_rec_tuple)
        self._insert_to_db(INSERT_CONFIG, detection_list_tuple)

        self.db_conn.commit()

    #retreival functions
    def retrieve_config_path(self,table, config_type):

        self.db_cursor.execute("SELECT path FROM " + table + " WHERE type = '" + config_type + "'")
        _path = self.db_cursor.fetchall()
        full_path = self.project_path / Path(self._clean_query(_path))
        return full_path

    def retrieve_image_paths(self):
        paths=[]
        self.db_cursor.execute("SELECT path FROM images")
        path = self.db_cursor.fetchone()
        while path is not None:
            path = self._clean_query(path)
            paths.append(path)
            path = self.db_cursor.fetchone()
        return paths

    #update and add functions
    def update_red(self,im_path,hasred):
        insert_image_red = f"UPDATE images SET red = {hasred} WHERE path = '{im_path}'"
        self.db_cursor.execute(insert_image_red)
        self.db_conn.commit()
    def update_circle(self, im_path,hascircle):
        insert_image_circle = f"UPDATE images SET circle = {hascircle} WHERE path = '{im_path}'"
        self.db_cursor.execute(insert_image_circle)
        self.db_conn.commit()




