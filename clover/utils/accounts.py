import sqlite3
from db_builder import getPass, addUser, check_password


def authenticate(user, passw):
     info = getPass(user)
     if info == None:
         return -1
     elif check_password(info, passw):
          return 1
     else:
          return -2
     

def register(user, passw, name):
     addUser(user,passw, name)