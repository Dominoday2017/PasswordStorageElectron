from os import altsep
import sys
sys.path.append("python_lib")
from cryptography.fernet import Fernet

class EditRow():
    def __init__(self):
        super().__init__()
        self.edit_row()
    
    def edit_row(self):
        key = self.read_key()
        table = []
        with open('userTable.txt', 'r') as file_read:
            for line in file_read:
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
                to_table = name, email, password, other
                table.append(to_table)

        with open('userTable.txt', 'w') as file_write:
            key = self.read_key()
            id = str(sys.argv[1])
            new_name = str(sys.argv[2])
            new_email = str(sys.argv[3])
            new_password = str(sys.argv[4])
            new_other = str(sys.argv[5])
            new_table = []

            for line in table:
                if line[0] == id:
                    name = line[0]
                    email = line[1]
                    password = line[2]
                    other = line[3]

                    if new_name:
                        name = new_name
                    if new_password:
                        password = new_password
                    if new_email:
                        email = new_email
                    if new_other:
                        other = new_other
                    name = self.encrypt(name.encode(), key)
                    email = self.encrypt(email.encode(), key)
                    password = self.encrypt(password.encode(), key)
                    other = self.encrypt(other.encode(), key)

                    file_write.write(repr(name) + "//" + repr(email) + "//" + repr(password) + "//" + repr(other) + "\n")
                else:
                    name = line[0]
                    email = line[1]
                    password = line[2]
                    other = line[3]

                    name = self.encrypt(name.encode(), key)
                    email = self.encrypt(email.encode(), key)
                    password = self.encrypt(password.encode(), key)
                    other = self.encrypt(other.encode(), key)
                    file_write.write(repr(name) + "//" + repr(email) + "//" + repr(password) + "//" + repr(other) + "\n")
        print('successfully edited')

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

EditRow()