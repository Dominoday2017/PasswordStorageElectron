from os import altsep
import sys
sys.path.append("python_lib")
from cryptography.fernet import Fernet

class ReadData():
    def __init__(self):
        super().__init__()
        self.read()

    def read(self):
        key = self.read_key()
        with open('userData.txt', 'r') as file:
            line = file.readline()
            username, password = line.split(',')
            username = self.make_correct(username)
            password = self.make_correct(password)

            username = self.decrypt(username.encode(), key).decode()
            password = self.decrypt(password.encode(), key).decode()
            print(password, username, end='')

    def encrypt(self, message: bytes, key: bytes) -> bytes:
        return Fernet(key).encrypt(message)

    def decrypt(self, token: bytes, key: bytes) -> bytes:
        return Fernet(key).decrypt(token)

    def read_key(self):
        with open("key.txt", "rb") as file:
            key = file.readline()
            return key

    def make_correct(self, text):
        text = text.replace("\n", "")
        return text[2:] + text[:-1]
ReadData()