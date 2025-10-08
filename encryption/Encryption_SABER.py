from cryptography.fernet import Fernet

#Use Fernet to load in public keys and encrypt/decrypt data
#Blackside = encrypted, Redside = unencrypted
class Encrytion_SABER:
    def __init__(self):
        self.red_side_files = None #not encrypted files
        self.black_side_files = None #encrypted files 
        self.public_key = None 
        self.private_key = None

    #Needs to function in a way to be communicative with the image_rec indexes

    def load_red_files(self):
        pass
    #Needs to function in a way to eventually deal with whatever we come up with for the receiver stack
    def load_black_files(self):
        pass
    
    def load_public_key(self):
        pass
    def load_private_key(self):
        pass
    #sends the stored data in the key variables to the garabage collector
    def dump_keys(self):
        self.public_key = None
        self.private_key = None
    #intentionally seperated because I feel like it I guess, in a real world scenario this would have to be true 
    # since redside/blackside hardware wouldn't be interfacing to a device in the same way, in this case they are
    def save_red_files(self):
        pass
    def save_black_files(self):
        pass

    
    def encrypt(self):
        f = Fernet(self.public_key)
        for file in self.red_side_files:
            with open(file,"rb"):
                red = file.read()
            self.black_side_files.append(f.encrypt(red))
        self.dump_keys()
        del f

    def decrypt(self):
        f = Fernet(self.private_key)
        for file in self.black_side_files:
            with open(file,"rb"):
                black = file.read()
            self.black_side_files.append(f.encrypt(black))
        self.dump_keys()
        del f