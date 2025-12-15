from Database.Database_SABER import Database_SABER
import hashlib
rxDB = Database_SABER('server')


import logging

logger = logging.getLogger("rxHandler")



def main():

    ciperText, ids_c = rxDB.bulkRetrieval('server', 'encryptedImage')


    for i, cipher in enumerate(ciperText):
        hashGen = hashlib.sha256()
        hashGen.update(cipher)
        rxHash = rxDB.getValue('server',ids_c[i],'id','receivedHash')

        buffer = "-"*43
        if rxHash == hashGen.hexdigest():
            logger.info(f" Function {main.__name__}: Received hash sha256@{rxHash}\n" +
                        " "*44 + f"is equal to generated hash sha256@{hashGen.hexdigest()}")
        else:
            logger.debug(f" Function {main.__name__}: Received hash sha256@{rxHash}\n" +
                         " "*44 + f"is not equal to generated hash sha256@{hashGen.hexdigest()}")
            raise Exception('hash is not equal')




