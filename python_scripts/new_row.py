from os import altsep
import sys
sys.path.append("python_lib")
from cryptography.fernet import Fernet

class AppendNewRow():
    def __init__(self):
        super().__init__()
        self.save()
    
    def save(self):
        key = self.read_key()
        with open('userTable.txt', 'a+') as file:
            name = str(sys.argv[1])
            email = str(sys.argv[2])
            password = str(sys.argv[3])
            other = str(sys.argv[4])

            if self.check_name(name) == True:
                print("name arledy exist")
                return False
            else:
                name = self.encrypt(name.encode(), key)
                email = self.encrypt(email.encode(), key)
                password = self.encrypt(password.encode(), key)

                if other == '':
                    string_to_file = repr(name) + '//' + repr(email) + '//' + repr(password)
                    file.write(string_to_file + '\n')
                else:
                    other = self.encrypt(other.encode(), key)
                    string_to_file = repr(name) + '//' + repr(email) + '//' + repr(password) + '//' + repr(other)
                    file.write(string_to_file + '\n')

    # Check if given name exist in file. Function return value True if name exist

    def check_name(self, name):
        condition = False
        key = self.read_key()
        with open('userTable.txt', 'r') as file:
            for line in file:
                line = line.replace('\n', '')
                name_file, *other = line.split('//')
                name_file = self.make_correct(name_file)
                name_file = self.decrypt(name_file.encode(), key).decode()
                if name_file == name:
                    condition = True
        return condition

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
        

AppendNewRow()