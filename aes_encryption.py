import hashlib
from Cryptodome.Cipher import AES
from base64 import b64encode

class AES_Encryption():
    def __init__(self, key):
        self.block_size = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def aes_encrypt(self, plain_text):
        plain_text = self.__pad(plain_text)
        iv = b'R\x94\r\xc5\xa5L\x8dd\x9f}\xc8\x14l*{~'
        print(iv)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted_text = cipher.encrypt(plain_text.encode())
        return b64encode(iv + encrypted_text).decode("utf-8")

    def __pad(self, plain_text):
        number_of_bytes_to_pad = self.block_size - len(plain_text) % self.block_size
        ascii_string = chr(number_of_bytes_to_pad)
        padding_str = number_of_bytes_to_pad * ascii_string
        padded_plain_text = plain_text + padding_str
        return padded_plain_text


