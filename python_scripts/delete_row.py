from os import altsep
import sys
sys.path.append("python_lib")
from cryptography.fernet import Fernet

class DeleteRow():
    def __init__(self):
        super().__init__()
        self.delete()
    
    def delete(self):
        key = self.read_key()
        id = sys.argv[1]
        new_table = []
        with open('userTable.txt', 'r') as file:
            for line in file:
                name, *other = line.split('//')
                name = self.make_correct(name)
                name = self.decrypt(name.encode(), key).decode()
                if name == id:
                    pass
                else:
                    new_table.append(line)
        with open('userTable.txt', 'w') as file:
            for el in new_table:
                file.write(el)

        
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
DeleteRow()