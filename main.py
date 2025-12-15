from CircleRecognition.CircleRec_SABER import CircleRec_SABER
from Transmission.DataConditioner_SABER import DataConditioner_SABER
from Transmission.Crypto_SABER import Crypto_SABER
import Transmission.txHandler_SABER
import Transmission.rxHandler_SABER
import subprocess
import logging
from Utilities.logDefs import *
logger = logging.getLogger("mainFunction")
# result = subprocess.run(["bash", "cleanMain.sh"], capture_output=True, text=True)
#
# print("Standard Output:")
# print(result.stdout)
# print("\nStandard Error:")
# print(result.stderr)
# print(f"\nExit Code: {result.returncode}")
logging.basicConfig(filename='SABER_log.log',format='%(asctime)s %(levelname)s:%(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

logger.info(WRAPPINGLINE)
logger.info(SABERSPLASH_ASCII)


logger.info(SECTIONBREAK)
logger.info(" SABER demonstration has begun.")

detect = CircleRec_SABER()
og_conditioner = DataConditioner_SABER(mode = 'origin')
og_crypto = Crypto_SABER(mode = 'origin')
debug_conditioner = DataConditioner_SABER(mode = 'debug')

if __name__ == "__main__":
    logger.info(SECTIONBREAK+"\n")
    logger.info(" Begin circle detection")
    detect.warmupHough()
    detect.main()
    logger.info(" Circle detection has completed successfully")
    logger.info(SECTIONBREAK*120+"\n")
    logger.info(" Serialization has begun")
    og_conditioner.main()
    logger.info(" Serialization has completed successfully\n")
    logger.info(SECTIONBREAK+"\n")
    logger.info(" Encryption has begun")
    og_crypto.generateNewKey()
    og_crypto.main()

    logger.info(" Encryption has completed successfully\n")
    logger.info(SECTIONBREAK+"\n")
    logger.info(" Dummy transmission has begun")
    Transmission.txHandler_SABER.main()
    Transmission.rxHandler_SABER.main()
    logger.info(" Dummy transmission has completed successfully\n")
    logger.info(SECTIONBREAK+"\n")
    
    srv_crypto = Crypto_SABER(mode='server')
    
    srv_conditioner = DataConditioner_SABER(mode='server')
    
    logger.info(" Decrypytion has begun")
    srv_crypto.main()
    logger.info(" Decryption has completed successfully")
    logger.info(SECTIONBREAK+"\n")
    logger.info(" Deserialization has begun")
    srv_conditioner.main()
    logger.info(" Deserialization has completed successfully\n")
    logger.info(SECTIONBREAK+"\n")
    logger.info(" Progam has completed without error, plans can now be served to the galaxy\n")
    logger.info(WRAPPINGLINE + "\n\n\n\n\n\n")


