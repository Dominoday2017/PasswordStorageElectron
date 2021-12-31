from os import altsep
import sys
sys.path.append("python_lib")
from cryptography.fernet import Fernet

class RegistationSystem():
    def __init__(self):
        super().__init__()
        self.gen_key()
        self.save_to_file()

    def save_to_file(self):
        key = self.read_key()
        with open('userData.txt', 'w') as file:
            username = str(sys.argv[1])
            password = str(sys.argv[2])

            username_en = self.encrypt(username.encode(), key)
            password_en = self.encrypt(password.encode(), key)

            file.write(repr(username_en) + "," + repr(password_en))

    def read(self):
        key = self.read_key()
        with open('userData.txt', 'r') as file:
            line = file.readline()

            username, password = line.split(',')
            username = self.make_correct(username)
            password = self.make_correct(password)

            username = self.decrypt(username.encode(), key).decode()
            password = self.decrypt(password.encode(), key).decode()
            
            print(username, password)

    def encrypt(self, message: bytes, key: bytes) -> bytes:
        return Fernet(key).encrypt(message)

    def decrypt(self, token: bytes, key: bytes) -> bytes:
        return Fernet(key).decrypt(token)

    def gen_key(self):
        with open("key.txt", "wb+") as file:
            key = Fernet.generate_key()
            file.write(key)

    def read_key(self):
        with open("key.txt", "rb") as file:
            key = file.readline()
            return key

    def make_correct(self, text):
        text = text.replace("\n", "")
        return text[2:] + text[:-1]
RegistationSystem()