
"""
Class: DataConditioner_Saber
Author: Spencer Mullins
Version: 0.0.1
Last Change: 11/28/2025
Description:
A class to encrypt and decrypt serialized data
"""
import base64

from database.Database_SABER import Database_SABER

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os



class Crypto_SABER:
    def __init__(self, mode='origin'):
        self.serializedData = None
        self.mode = mode
        self.cipherText = []
        self.DB = Database_SABER(mode)
        self.cipherText = []
        self.image_ids = []
        self.ivs = None
        self.keyFilePath = self.DB.getValue('pathConfig','AESKey','type','path')
        self.key = None
        self.encryptedData = None
        self.decryptedData = []
    def __del__(self):
        self.DB.cleanup()

    def generateNewKey(self):
        key = os.urandom(32)
        with open(self.keyFilePath,'wb') as f:
            f.write(key)

    def getKey(self):
        with open(self.keyFilePath,'rb') as f:
            self.key = f.read()

    def getSerializedData(self):
        self.serializedData, self.image_ids = self.DB.conditionalBulkRetrieval('origin','serializedImage','hasCircle',1)

    def getEncryptedData(self):
        self.encryptedData, self.image_ids = self.DB.bulkRetrieval('server','encryptedImage')
        self.ivs, self.image_ids = self.DB.bulkRetrieval('server','cryptoIV')

    def encrypt(self,data):
        self.getKey()
        data = base64.b64decode(data)
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key),modes.CTR(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()

        return ciphertext,iv

    def decrypt(self,text,iv):
        self.getKey()
        cipher = Cipher(algorithms.AES(self.key), modes.CTR(iv))
        decryptor = cipher.decryptor()
        data = decryptor.update(text) + decryptor.finalize()
        data = base64.b64encode(data)
        return data

    def encryptAll(self):
        for i, data in enumerate(self.serializedData):
            cipher, iv = self.encrypt(data)
            self.DB.setValue('origin','encryptedImage',cipher,'id',self.image_ids[i])
            self.DB.setValue('origin', 'cryptoIV', iv, 'id', self.image_ids[i])

    def decryptAll(self):
        for i, cipher in enumerate(self.encryptedData):
            data = self.decrypt(cipher,self.ivs[i])
            self.DB.setValue('server','serializedImage',data,'id',self.image_ids[i])

    def main(self):
        if self.mode == 'origin':
            self.getSerializedData()
            self.encryptAll()
            self.__del__()
        elif self.mode == 'server':
            self.getEncryptedData()
            self.decryptAll()
            self.__del__()
        else:
            print('set a mode')
