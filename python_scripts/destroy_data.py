from os import altsep
import sys
sys.path.append("python_lib")
from cryptography.fernet import Fernet

class DestroyData():
    def __init__(self):
        super().__init__()
        self.destroy()
    
    def destroy(self):
        with open("userTable.txt", "w") as file:
            pass
DestroyData()