from os import altsep
import sys
sys.path.append("python_lib")
from cryptography.fernet import Fernet

class ReadTable():
    def __init__(self):
        super().__init__()
        self.read()
    
    def read(self):
        key = self.read_key()
        str_to_return = ''
        with open('userTable.txt', 'r') as file:
            for line in file:
                line = line.replace('\n', '')
                name, email, password, *other = line.split('//')
  
                name = self.make_correct(name)
                email = self.make_correct(email)
                password = self.make_correct(password)
                
                name = self.decrypt(name.encode(), key).decode()
                email = self.decrypt(email.encode(), key).decode()
                password = self.decrypt(password.encode(), key).decode()

                if other:
                    other = other[0]
                    other = self.make_correct(other)
                    other = self.decrypt(other.encode(), key).decode()
                else:
                    other = '-'
                str_to_return += str(name) + ',' + str(email) + ',' + str(password) + ',' + str(other) + '\n'
        print(str_to_return, end="")    

    def read_key(self):
        with open("key.txt", "rb") as file:
            key = file.readline()
            return key

    def make_correct(self, text):
        text = text.replace("\n", "")
        return text[2:] + text[:-1]

    def encrypt(self, message: bytes, key: bytes) -> bytes:
        return Fernet(key).encrypt(message)

    def decrypt(self, token: bytes, key: bytes) -> bytes:
        return Fernet(key).decrypt(token)    

ReadTable()