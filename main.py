from circle_detection.CircleRec_SABER import CircleRec_SABER
from transmission.DataConditioner_SABER import DataConditioner_SABER
from transmission.Crypto_SABER import Crypto_SABER
import transmission.txHandler_SABER
import transmission.rxHandler_SABER
import subprocess

# result = subprocess.run(["bash", "cleanMain.sh"], capture_output=True, text=True)
#
# print("Standard Output:")
# print(result.stdout)
# print("\nStandard Error:")
# print(result.stderr)
# print(f"\nExit Code: {result.returncode}")



detect = CircleRec_SABER()
og_conditioner = DataConditioner_SABER(mode = 'origin')
og_crypto = Crypto_SABER(mode = 'origin')
debug_conditioner = DataConditioner_SABER(mode = 'debug')

if __name__ == "__main__":

    detect.warmupHough()
    detect.main()
    
    og_conditioner.main()
    og_crypto.generateNewKey()
    og_crypto.main()

    transmission.txHandler_SABER.main()
    transmission.rxHandler_SABER.main()
    srv_crypto = Crypto_SABER(mode='server')
    srv_conditioner = DataConditioner_SABER(mode='server')

    srv_crypto.main()
    srv_conditioner.main()


