
import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O
import hashlib
import uuid


def tableCreation():
    f="data/data.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    #Create the users table
    users_table = 'CREATE TABLE users (username TEXT PRIMARY KEY, password BLOB, userID INTEGER, name TEXT);'
    c.execute(users_table)
    #Create the stories table
    money_table = 'CREATE TABLE money (userID INTEGER, currentMoney REAL, monthIncome REAL, otherIncome REAL, savings REAL);'
    c.execute(money_table)
    #Create the updates table
    fixedcost_table = 'CREATE TABLE fixedcost (userID INTEGER, expID INTEGER, fixedName TEXT, fixedAmt REAL, fixedDesc TEXT);'
    c.execute(fixedcost_table)

    variablecost_table = 'CREATE TABLE variablecost (userID INTEGER, expID INTEGER, expName TEXT, expAmt REAL, expBud REAL, expDesc TEXT, dateof TEXT);'
    c.execute(variablecost_table)

    stocks_table = 'CREATE TABLE stocks (userID INTEGER, expID INTEGER, shares INTEGER, purdate TEXT, purprice DATE);'
    c.execute(stocks_table)


    db.commit()
    db.close()

#==========================================================================

#ADD VALUES TO TABLES

def hash_password(password):
    key = uuid.uuid4().hex
    return hashlib.sha256(key.encode() + password.encode()).hexdigest()+':' + key

def check_password(hashed_password, user_password):
    password, key = hashed_password.split(':')
    return password == hashlib.sha256(key.encode()+user_password.encode()).hexdigest()

#add a user
def addUser(new_username, new_password, new_name):
    f="data/data.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    #global userID_counter
    #new_userID = userID_counter
    #userID_counter += 1
    userCount = c.execute('SELECT COUNT(*) FROM users;')
    new_userID = 0
    for x in userCount:
        new_userID = x[0]
    #new_userID += 1
    hash_pass = hash_password(new_password)
    #print ('The string to store in the db is: ' + hash_pass)
    c.execute('INSERT INTO users VALUES (?,?,?,?)',[new_username, hash_pass, new_userID, new_name])
    db.commit()
    db.close()


#==========================================================================

#ACCESSORS

def checkUsername(userN):
    f="data/data.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    users = c.execute('SELECT username FROM users;')
    result = False
    for x in users:
        if (x[0] == userN):
            result = True
    db.close()
    return result

def getPass(username):
    f="data/usersandstories.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    command = "SELECT username, password FROM users"
    info = c.execute(command)

    retVal = None
    for entry in info:
        if str(entry[0]) == username:
            retVal = str(entry[1])
    db.close()
    return retVal

def getUserID(username):
    f="data/data.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    command = "SELECT username, userID FROM users"
    info = c.execute(command)

    retVal = None
    for user in info:
        if str(user[0]) == username:
            retVal = str(user[1])
    db.close()
    return retVal

def getUserName(ID):
    f="data/data.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    info = c.execute('SELECT username FROM users WHERE userID =' + str(ID) + ';')
    retVal = None
    for user in info:
        #print user
        retVal = user[0]
    db.close()
    return retVal

#========
#TESTING

if __name__ == '__main__':     
    #TESTING

    #tableCreation()


    #add users
    addUser('eric12', '123', 'eric')
    print getUserID('eric1')



