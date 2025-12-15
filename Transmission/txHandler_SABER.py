from Database.Database_SABER import Database_SABER

import hashlib
import logging
logger = logging.getLogger("txHandler")
txDB = Database_SABER('origin')
rxDB = Database_SABER('server')


def main():
    ciperText, ids_c = txDB.conditionalBulkRetrieval('origin','encryptedImage','hasCircle',1)


    for i,cipher in enumerate(ciperText):
        hash2 = hashlib.sha256() #hashlib.sha256 needs to be re-instanciated each loop or the hash is just a concatenation from the previous, this is why my tx was breaking in earlier runs.
        hash2.update(cipher)

        nonce = txDB.getValue('origin',ids_c[i],'id','nonce')
        tag = txDB.getValue('origin',ids_c[i],'id','tag')
        rxDB.loadFourValues('server',('encryptedImage','tag','nonce','receivedHash'),(cipher,tag,nonce,hash2.hexdigest()))
        logger.info(f" Function {main.__name__}:  Image loaded to target DB with hash {hash2.hexdigest()} ")
        


    txDB.cleanup()
    rxDB.cleanup()
