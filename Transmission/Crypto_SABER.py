
"""
Class: DataConditioner_Saber
Author: Spencer Mullins
Version: 0.0.1
Last Change: 11/28/2025
Description:
A class to encrypt and decrypt serialized data
"""



from Database.Database_SABER import Database_SABER
import logging
logger = logging.getLogger("Crypto_SABER")
from Utilities.validationUtility_SABER import validationUtility_SABER, handleExceptions
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

    @handleExceptions(reRaise=True)
    def generateNewKey(self):
        key = os.urandom(32)
        with open(self.keyFilePath,'wb+') as f:
            f.write(key)

    @handleExceptions(reRaise=True)
    def getKey(self):
        with open(self.keyFilePath,'rb') as f:
            self.key = f.read()

    @handleExceptions(reRaise=True)
    def getSerializedData(self):
        self.serializedData, self.image_ids = self.DB.conditionalBulkRetrieval('origin','serializedImage','hasCircle',1)

    @handleExceptions(reRaise=True)
    def getEncryptedData(self):
        self.DB.cursor.execute("SELECT id, encryptedImage,nonce,tag FROM server ORDER BY id")
        vals = self.DB.cursor.fetchall()
        self.image_ids = [row[0] for row in vals]
        self.encryptedData = [row[1] for row in vals]
        self.nonces = [row[2] for row in vals]
        self.tags = [row[3] for row in vals]

    @handleExceptions(reRaise=True)
    def encrypt(self,data):
        self.getKey()

        cipher = AES.new(self.key,AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data)

        return ciphertext,nonce,tag
    @handleExceptions(reRaise=True)
    def decrypt(self,ciphertext,nonce, tag):
        self.getKey()
        cipher = AES.new(self.key,AES.MODE_EAX, nonce = nonce)
        plaintext = cipher.decrypt(ciphertext)
      
        try:
            cipher.verify(tag)
            logger.info(f" Function {self.decrypt.__name__}: Decrpytion successful for image containing tag {tag}")
        except ValueError:
            logger.info(f" Function {self.decrypt.__name__}: Decrpytion unsuccessful for image containing tag {tag}")

        return plaintext
    @handleExceptions(reRaise=True)
    def encryptAll(self):
        for i, data in enumerate(self.serializedData):
            cipher, nonce, tag = self.encrypt(data)
            self.DB.setValue('origin','encryptedImage',cipher,'id',self.image_ids[i])
            self.DB.setValue('origin', 'nonce', nonce, 'id', self.image_ids[i])
            self.DB.setValue('origin','tag', tag, 'id',self.image_ids[i])
    @handleExceptions(reRaise=True)
    def decryptAll(self):
        for i, cipher in enumerate(self.encryptedData):
            data = self.decrypt(cipher,self.DB.getValue('server',self.image_ids[i],'id','nonce'),self.DB.getValue('server',self.image_ids[i],'id','tag'))
            self.DB.setValue('server','serializedImage',data,'id',self.image_ids[i])
    @handleExceptions(reRaise=True)
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
