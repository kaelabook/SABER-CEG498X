

import yaml
import sqlite3
from pathlib import Path
from yaml import FullLoader
import os
"""
Class: Database_SABER
Author: Spencer Mullins
Version: 0.0.3
Last Change: 11/29/25
Description:
SQLite database implemented to hold 2 tables config, and images. config holds configuration information loaded in from a yaml file.
Most of the relevant config information involves paths to other files.
"""

#static helpers
def _extractFileName(path: str):
    """Pull file name out of relative path in file"""
    return Path(str(path).strip().replace("\n", "")).name


def getFileNames(directory_path):

    file_names = []
    try:
        # Get a list of all entries in the directory
        all_entries = os.listdir(directory_path)

        # Iterate through each entry and check if it's a file
        for entry in all_entries:
            full_path = os.path.join(directory_path, entry)
            if os.path.isfile(full_path):
                file_names.append(entry)
    except FileNotFoundError:
        print(f"Error: Directory not found at '{directory_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")
    return file_names

class Database_SABER:
    def __init__(self, mode='origin', *, read_only: bool = False, init_db: bool = True, load_data: bool = True):
        self.mode = mode
        self.dbPath = self.chooseDB()

        self.projectPath = Path(__file__).resolve().parent
        self.dbPath = self.projectPath / self.dbPath
        self.configPath = Path('conf/saber_config.yaml')
        self.configPath = self.projectPath / self.configPath
        self.conf = yaml.load(open(self.configPath, 'r+'), Loader=FullLoader)

        if read_only:
            uri = f"file:{self.dbPath}?mode=ro"
            self.conn = sqlite3.connect(uri, uri=True)
        else:
            self.conn = sqlite3.connect(str(self.dbPath))

        self.cursor = self.conn.cursor()

        if init_db:
            self._init_db(load_data=load_data)

    # Dynamic Helpers
    def chooseDB(self):
        if self.mode == 'origin':
            return 'saber.db'
        elif self.mode == 'server':
            return 'saber-server.db'
        else:
            return 'dbTest'
    def makePathAbsolute(self, relativePath):
        """helper for making paths absolute"""
        out = self.projectPath / Path(str(relativePath).strip().replace("\n", ""))
        return out
    # Deconstructor
    def cleanup(self):
        self.conn.close()

    # Initializers
    def _init_db(self, load_data: bool = True):
        self.setupPathConfigTable()
        if load_data:
            self.loadPathConfig()

            if self.mode == 'origin':
                self.setupOriginImageTable()
                if load_data:
                    self.loadImagePaths()
            elif self.mode == 'server':
                self.setupServerImageTable()
            else:
                raise Exception("invalid mode entered, please use 'origin' or 'server'")

    def setupPathConfigTable(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS pathConfig ( 
            id INTEGER PRIMARY KEY,
            type TEXT UNIQUE,
            path TEXT UNIQUE
            )
            ''')

    def setupServerImageTable(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS server (
        id INTEGER PRIMARY KEY,
        path TEXT UNIQUE,
        imageName TEXT UNIQUE,
        serializedImage TEXT UNIQUE, 
        encryptedImage TEXT UNIQUE,
        nonce TEXT UNIQUE,
        tag TEXT UNIQUE,
        receivedHash TEXT UNIQUE
        )
        ''')

    def setupOriginImageTable(self):
        """constructs the table for origin data"""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS origin( 
            id INTEGER PRIMARY KEY,
            path TEXT UNIQUE,
            imageName TEXT UNIQUE,
            hasRed INTEGER,
            hasCircle INTEGER,
            serializedImage TEXT UNIQUE,
            encryptedImage TEXT UNIQUE,
            nonce TEXT UNIQUE,
            tag TEXT UNIQUE,
            generatedHash TEXT UNIQUE
            )
            ''')


    # General loaders
    def loadVal(self,table,col, val):
        """loads a single row value at associated column"""
        query = f"INSERT OR IGNORE INTO {table} ({col}) VALUES (?)"
        self.cursor.execute(query,(val,))
        self.conn.commit()

    def loadTwoVals(self,table, cols: tuple, vals:tuple):
        """load two columns of two rows with associated values"""
        query = f"INSERT OR IGNORE INTO {table} {cols} VALUES (?,?)"
        self.cursor.execute(query,vals)
        self.conn.commit()

    def loadThreeValues(self,table, cols: tuple, vals:tuple):
        """load two columns of two rows with associated values"""
        query = f"INSERT OR IGNORE INTO {table} {cols} VALUES (?,?,?)"
        self.cursor.execute(query,vals)
        self.conn.commit()
    def loadFourValues(self,table, cols: tuple, vals:tuple):
        """load two columns of two rows with associated values"""
        query = f"INSERT OR IGNORE INTO {table} {cols} VALUES (?,?,?,?)"
        self.cursor.execute(query,vals)
        self.conn.commit()

    def loadFromConfig(self, table, column1, column2, majKey, minKeys1, minKeys2):
        """parses loaded in yaml, key depth is only 2, major + minor keys"""
        vals = (str(self.makePathAbsolute(self.conf[majKey][minKeys1])), self.conf[majKey][minKeys2])
        cols = (column1, column2)

        self.loadTwoVals(table, cols, vals)


    # Specific Loaders
    def loadPathConfig(self):
        self.loadFromConfig('pathConfig','path', 'type','images_origin','path','type')
        self.loadFromConfig('pathConfig', 'path', 'type', 'aes_key', 'path', 'type')
        self.loadFromConfig('pathConfig', 'path', 'type', 'images_server', 'path', 'type')


    def loadImagePaths(self):
        path = self.getValue('pathConfig','images-origin','type','path')
        path = self.makePathAbsolute(path)
        images = getFileNames(path)
        for image in images:
            pathIm = str(path / Path(image))
            self.loadTwoVals('origin',('imageName','path'),(image,pathIm))

    # General Mutators
    def setValue(self,table,destCol,destVal,checkCol, checkVal):
        query =  (
                 f"UPDATE {table} "
                 f"SET {destCol} = ? "
                 f"WHERE {checkCol} = ?"
                 )

        self.cursor.execute(query, (destVal,checkVal))
        self.conn.commit()


    # General accessors

    def getValue(self,table,checkVal,checkCol,reqCol):
        query =  (
                 f"SELECT {reqCol} "
                 f"FROM {table} "
                 f"WHERE {checkCol} = ?"
                 f"ORDER BY id"
                 )
        self.cursor.execute(query,(checkVal,))
        rtn = self.cursor.fetchone()
        return rtn[0]

    def bulkRetrieval(self,table,col):
        ids = []
        vals = []
        query = f"SELECT id, {col} FROM {table} ORDER BY id"
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        while row is not None:
            ids.append(row[0])
            vals.append(row[1])
            row = self.cursor.fetchone()
        return vals,ids

    def conditionalBulkRetrieval(self,table,col,checkCol,checkVal):
        ids = []
        vals = []
        query = f"SELECT id, {col} FROM {table} WHERE {checkCol} = ? ORDER BY id"
        self.cursor.execute(query,(checkVal,))
        row = self.cursor.fetchone()
        while row is not None:
            ids.append(row[0])
            vals.append(row[1])
            row = self.cursor.fetchone()
        return vals,ids

# Hello This a test comment.