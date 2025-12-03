from circle_detection.CircleRec_SABER import CircleRec_SABER
from transmission.DataConditioner_SABER import DataConditioner_SABER
from transmission.Crypto_SABER import Crypto_SABER

detect = CircleRec_SABER()
og_conditioner = DataConditioner_SABER(mode = 'origin')
og_crypto = Crypto_SABER(mode = 'origin')

if __name__ == "__main__":

    detect.main()
    og_conditioner.main()
    og_crypto.main()


