
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
from Crypto.Cipher import AES
import os



class Crypto_SABER:
    def __init__(self, mode='origin'):
        self.serializedData = None
        self.mode = mode
        self.cipherText = []
        self.DB = Database_SABER(mode)
        self.cipherText = []
        self.image_ids = []
        self.tags = None
        self.nonces = None
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
        self.nonces, self.image_ids = self.DB.bulkRetrieval('server','nonce')
        self.tags, self.image_ids = self.DB.bulkRetrieval('server','tag')


    def encrypt(self,data):
        self.getKey()
        data = base64.b64decode(data)
        cipher = AES.new(self.key,AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data)
        print(f"Data last 10: {str(ciphertext[len(ciphertext)-20:len(ciphertext)-10])}")
        print(f"Tag {tag}")
        return ciphertext,nonce,tag

    def decrypt(self,ciphertext,nonce, tag):
        self.getKey()
        cipher = AES.new(self.key,AES.MODE_EAX, nonce = nonce)
        plaintext = cipher.decrypt(ciphertext)
        print(f"Data last 10: {str(ciphertext[len(ciphertext)-20:len(ciphertext)-10])}")
        print(f"Tag: {tag}")
        try:
            cipher.verify(tag)
            print("Authenticated")
        except ValueError:
            print("Decryption Failed")

        return plaintext

    def encryptAll(self):
        for i, data in enumerate(self.serializedData):
            cipher, nonce, tag = self.encrypt(data)
            self.DB.setValue('origin','encryptedImage',cipher,'id',self.image_ids[i])
            self.DB.setValue('origin', 'nonce', nonce, 'id', self.image_ids[i])
            self.DB.setValue('origin','tag', tag, 'id',self.image_ids[i])

    def decryptAll(self):
        for i, cipher in enumerate(self.encryptedData):
            data = self.decrypt(cipher,self.DB.getValue('server',self.image_ids[i],'id','nonce'),self.DB.getValue('server',self.image_ids[i],'id','tag'))
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
