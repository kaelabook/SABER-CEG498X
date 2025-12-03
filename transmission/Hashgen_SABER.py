"""
Document me
"""
import hashlib


class Hashgen_SABER:
    def __init__(self):
        self.hash = hashlib.sha256()
    def generateHash(self,data):
        self.hash.update(data)
        return self.hash.hexdigest()
