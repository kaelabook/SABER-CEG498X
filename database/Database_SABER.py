from os import major

import yaml
import sqlite3
from pathlib import Path
import re
from yaml import FullLoader

"""
Class: Database_SABER
Author: Spencer Mullins
Version: 0.0.1
Last Change: 11/23/25
Description:
SQLite database implemented to hold 2 tables config, and images. config holds configuration information loaded in from a yaml file.
Most of the relevant config information involves paths to other files.

"""


class Database_SABER:
    def __init__(self, dbPath='saber.db'):
        self.dbPath =dbPath

        self.projectPath = Path(__file__).resolve().parent
        self.dbPath = self.projectPath / self.dbPath



        self.configPath = Path('conf/saber_config.yaml')
        self.configPath = self.projectPath / self.configPath
        self.conf = yaml.load(open(self.configPath, 'r+'), Loader=FullLoader)
        self.conn = sqlite3.connect(str(self.dbPath))
        self.cursor = self.conn.cursor()

    def cleanup(self):
        self.conn.close()

    def _init_db(self):
        self.setupPathConfigTable()
        self.setupImageTable()
        self.loadPathConfig()
        self.loadImagePaths()


    def setupPathConfigTable(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS pathConfig ( 
            id INTEGER PRIMARY KEY,
            type TEXT UNIQUE,
            path TEXT UNIQUE
            )
            ''')

    def setupImageTable(self):
        """constructs the table for image data"""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS images ( 
            id INTEGER PRIMARY KEY,
            path TEXT UNIQUE,
            imageName TEXT UNIQUE,
            hasRed INTEGER,
            hasCircle INTEGER
            )
            ''')
    def makePathAbsolute(self,relativePath):
        """helper for making paths absolute"""
        out= str(self.projectPath / Path(relativePath.strip().replace("\n", "")))
        return out

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

    def _extractFileName(self,path: str):
        """Pull file name out of relative path in file"""
        return Path(path.strip().replace("\n", "")).name

    def loadImagePaths(self):
        """loads all image paths from config value"""
        file_path = self.getConfigValue('path')
        cols = ('path','imageName')
        table = 'images'

        with open(self.projectPath/Path(file_path.strip().replace("'","")), 'r') as f:
            for line in f:
                vals = (self.makePathAbsolute(line),self._extractFileName(line))

                self.loadTwoVals(table,cols,vals)
            self.conn.commit()

    def _cleanQuery(self,query):
        """helper to strip query artifacts from queries, queries come back as strings formated as tuples and sometimes store random quotations"""
        queryArtifacts = r"[,()\[\]\"]"
        result = re.sub(queryArtifacts,'',str(query))
        return result.strip().replace("\'","")

    def loadPathConfig(self):
        self.loadFromConfig('pathConfig','path', 'type','image_rec','list','type')


    def loadFromConfig(self,table,column1, column2,majKey,minKeys1 ,minKeys2):
            vals = (self.conf[majKey][minKeys1],self.conf[majKey][minKeys2])
            cols = (column1,column2)
            self.loadTwoVals(table,cols,vals)




    def getConfigValue(self, configType):
        table     = 'pathConfig'
        checkCol = 'type'
        reqCol   = 'path'
        checkVal =  configType


        configPath = self.getValue(table,checkVal,checkCol,reqCol)
        configPath = self._cleanQuery(configPath)

        return configPath

    def retrieve_image_paths(self):
        paths=[]
        self.cursor.execute("SELECT path FROM images")
        path = self.cursor.fetchone()
        while path is not None:
            path = self._cleanQuery(path)
            paths.append(path)
            path = self.cursor.fetchone()
        return paths

    #update and add functions
    def setRedVal(self,imName,hasRed):
        table     = 'images'
        destCol  = 'hasRed'
        dest_val  =  hasRed
        checkCol = 'imageName'
        checkVal =  imName

        self.setValue(table,destCol,dest_val,checkCol,checkVal)

    def setCircleVal(self, imName,hasCircle):
        table     = 'images'
        destCol  = 'hasCircle'
        dest_val  =  hasCircle
        checkCol = 'imageName'
        checkVal =  imName

        self.setValue(table,destCol,dest_val,checkCol,checkVal)

    def setValue(self,table,destCol,destVal,checkCol, checkVal):
        query =  (
                 f"UPDATE {table} "
                 f"SET {destCol} = {destVal} "
                 f"WHERE {checkCol} = '{checkVal}'"
                 )

        self.cursor.execute(query)
        self.conn.commit()

    def getValue(self,table,checkVal,checkCol,reqCol):
        query =  (
                 f"SELECT {reqCol} "
                 f"FROM {table} "
                 f"WHERE {checkCol} = '{checkVal}'"
                 )
        self.cursor.execute(query)
        return self.cursor.fetchall()


