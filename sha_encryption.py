import hashlib

class SHA_Encryption:
    def sha_encrypt(data):
        encrypted = hashlib.sha256(data.encode()).hexdigest()
        return encrypted