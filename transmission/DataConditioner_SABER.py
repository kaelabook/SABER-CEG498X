"""
Class: DataConditioner_Saber
Author: Spencer Mullins
Version: 0.0.1
Last Change: 11/29/2025
Description
A class to condition and decondition data for and from transmission, serialize/deserialize.
"""
import base64
from pathlib import Path
from database.Database_SABER import Database_SABER

class DataConditioner_SABER:
    def __init__(self,mode):
        if mode == 'debug':
            self.DB= Database_SABER(mode = 'origin')
        else:
            self.DB = Database_SABER(mode=mode)
        self.files = []
        self.serializedData = []
        self.mode = mode
        self.rxImagePath = self.DB.getValue('pathConfig','images-server','type','path')
        self.ids = []
        self.decryptedData = []

    def __del__(self):
        self.DB.cleanup()



    def loadFilePaths(self):
        """loads in filepaths and ids"""
        self.files,self.ids = self.DB.conditionalBulkRetrieval('origin','path','hasCircle',1)

    def loadDecrypted(self,table='server'):
        if table != 'server':
            self.decryptedData,self.ids = self.DB.conditionalBulkRetrieval(table, 'serializedImage','hasCircle',1)
        else:
            self.decryptedData,self.ids = self.DB.bulkRetrieval(table,'serializedImage')


    def serialize(self):
        for i,filePath in enumerate(self.files):
            with open(filePath,'rb') as f:
                self.DB.setValue('origin','serializedImage',base64.b64encode(f.read()),'id',self.ids[i])



    def deserialize(self):
        """deserializes data and writes it to a folder"""
        for i,data in enumerate(self.decryptedData):
            nameStr = f"image{i}.png"
            outputPath = self.rxImagePath / Path(nameStr)
            decoded = base64.b64decode(data)
            with open(outputPath, "wb") as outputFile:
                outputFile.write(decoded)
                outputFile.close()
            if self.mode == 'server':
                self.DB.setValue('server','path',str(outputPath),'id',self.ids[i])
    def main(self):
        if self.mode == 'origin':
            self.loadFilePaths()
            self.serialize()
            self.__del__()
        elif self.mode == 'server':
            self.loadDecrypted()
            self.deserialize()
            self.__del__()
        elif self.mode == 'debug':
            self.loadFilePaths()
            self.serialize()
            self.loadDecrypted('origin')
            self.deserialize()