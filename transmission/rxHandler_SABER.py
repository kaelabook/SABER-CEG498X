from database.Database_SABER import Database_SABER
import hashlib
rxDB = Database_SABER('server')






def main():

    ciperText, ids_c = rxDB.bulkRetrieval('server', 'encryptedImage')


    for i, cipher in enumerate(ciperText):
        hashGen = hashlib.sha256()
        hashGen.update(cipher)
        rxHash = rxDB.getValue('server',ids_c[i],'id','receivedHash')

        # print(f"Image {i}:")
        # print(f"Origin hash: {rxHash}")
        # print(f"Gen hash: {hashGen.hexdigest()}")

        if rxHash == hashGen.hexdigest():
            continue
        else:
            raise Exception('hash is not equal')




