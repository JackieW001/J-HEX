
import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O
import hashlib
import uuid
import datetime
import os

DIR = os.path.dirname(__file__) or '.'
DIR += '/../data/data.db'

def tableCreation():
    if not os.path.isfile('data/data.db'):
        db = sqlite3.connect(DIR) #open if f exists, otherwise create
        c = db.cursor()         #facilitates db ops

        users_table = 'CREATE TABLE  users (username TEXT PRIMARY KEY, password BLOB, userID INTEGER, name TEXT, config INTEGER);'
        c.execute(users_table)

        money_table = 'CREATE TABLE  money (userID INTEGER, currentMoney REAL, monthIncome REAL, otherIncome REAL, savings REAL, savingPercent REAL);'
        c.execute(money_table)

        allocated_table = 'CREATE TABLE allocate (userID INTEGER, entertainment REAL, eatOut REAL, shop REAL, misc REAL, grocery REAL, event REAL);'
        c.execute(allocated_table)
     
        fixedcost_table = 'CREATE TABLE fixedcost (userID INTEGER, fixedID INTEGER, fixedName TEXT, fixedAmt REAL, fixedType TEXT, fixedDesc TEXT);'
        c.execute(fixedcost_table)

        variablecost_table = 'CREATE TABLE variablecost (userID INTEGER, expID INTEGER, expName TEXT, expType TEXT, expAmt REAL, expDesc TEXT, dateof TEXT);'
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
def addUser(new_username, new_password, new_name, new_config):
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
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
    c.execute('INSERT INTO users VALUES (?,?,?,?,?)',[new_username, hash_pass, new_userID, new_name, new_config])
    db.commit()
    db.close() 


def setConfig(ID):
    db = sqlite3.connect(DIR)
    c = db.cursor()
    command = 'UPDATE users SET config = 1 WHERE userID = '+str(ID)+';'
    c.execute(command)
    db.commit()
    db.close()

def addMoneyTable (ID, currentMoney, monthIncome, otherIncome, savings, savingPercent):
    db = sqlite3.connect(DIR)
    c = db.cursor()
    command = 'INSERT INTO money VALUES (?,?,?,?,?,?);'
    c.execute(command,[ID,currentMoney,monthIncome,otherIncome,savings,savingPercent])
    db.commit()
    db.close()  

def updateMoneyTable(ID, currentMoney, monthIncome, otherIncome, savings, savingPercent):
    db = sqlite3.connect(DIR)
    c = db.cursor()
    c.execute('UPDATE money SET currentMoney = {}, monthIncome = {}, otherIncome = {}, savings = {}, savingPercent = {} WHERE userID = {}'.format(currentMoney, monthIncome, otherIncome, savings, savingPercent, ID))
    db.commit()
    db.close()

def addAllocateTable (ID, entertainment, eatOut, shop, misc, grocery, event):
    db = sqlite3.connect(DIR)
    c = db.cursor()
    command = 'INSERT INTO allocate VALUES (?,?,?,?,?,?,?);'
    c.execute(command,[ID,entertainment, eatOut, shop, misc, grocery,event])
    db.commit()
    db.close()   

def updateAllocateTable(ID, entertainment, eatOut, shop, misc, grocery,event):  
    db = sqlite3.connect(DIR)
    c = db.cursor()
    c.execute('UPDATE allocate SET entertainment = {}, eatOut = {}, shop = {}, misc = {}, grocery = {}, event = {} WHERE userID = {}'.format(ID, entertainment, eatOut, shop, misc, grocery,event))
    db.commit()
    db.close()

#userID INTEGER, expID INTEGER, expName TEXT, expType TEXT, expAmt REAL, expDesc TEXT, dateof TEXT
def addVarCost(ID, expName, expType, expAmt, expDesc):
    date = (datetime.datetime.now()).strftime('%Y-%m-%d')
    db = sqlite3.connect(DIR)
    c = db.cursor() 

    expID = c.execute('SELECT max(expID) FROM variablecost WHERE userID = {}'.format(ID)).fetchone()[0]
    if expID == None:
        expID = 0
    else:
        expID = int(expID) + 1

    print "\n\n\n"
    c.execute('INSERT INTO variablecost VALUES (?,?,?,?,?,?,?);',[ID, expID, expName, expType, expAmt, expDesc, date])
    db.commit()
    db.close()
#userID INTEGER, expID INTEGER, fixedName TEXT, fixedAmt REAL, fixedDesc TEXT
def addFixCost(ID, fixedName, fixedAmt, fixedtype, fixedDesc):
    db = sqlite3.connect(DIR)
    c = db.cursor() 

    fixedID = c.execute('SELECT max(fixedID) FROM fixedcost WHERE userID = {}'.format(ID)).fetchone()[0]
    if fixedID == None:
        fixedID = 0
    else:
        fixedID = int(fixedID) + 1

    print "\n\n\n"
    c.execute('INSERT INTO fixedcost VALUES (?,?,?,?,?,?);',[ID, fixedID, fixedName, fixedAmt, fixedtype, fixedDesc])
    db.commit()
    db.close()   
 
#========================================================================================================

#ACCESSORS

def checkUsername(userN):
    db = sqlite3.connect(DIR)
    c = db.cursor()
    users = c.execute('SELECT username FROM users;')
    result = False
    for x in users:
        if (x[0] == userN):
            result = True
    db.close()
    return result

def getPass(username):
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
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
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    command = 'SELECT userID FROM users WHERE username ="' + username + '";'
    info = c.execute(command)
    retVal = info.fetchall()[0][0]

    db.close()
    return retVal

def getUserName(ID):
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    command = 'SELECT userID FROM users WHERE userID ="' + str(ID) + '";'
    info = c.execute(command)

    retVal = None
    for user in info:
        #print user
        retVal = user[0]
    db.close()
    return retVal

def getConfig(ID):
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    info = c.execute('SELECT config FROM users WHERE userID =' + str(ID) + ';')
    retVal = None
    for user in info:
        print "user:"
        print user
        retVal = user[0]

    db.close()
    return retVal

#userID INTEGER, currentMoney REAL, monthIncome REAL, 
#otherIncome REAL, savings REAL, savingPercent REAL
def getMoneyTable(ID):
    ret = {}
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    ret['currentMoney'] = c.execute('SELECT currentMoney FROM money WHERE userID ={};'.format(ID)).fetchone()[0]
    ret['monthIncome'] = c.execute('SELECT monthIncome FROM money WHERE userID ={};'.format(ID)).fetchone()[0]
    ret['otherIncome'] = c.execute('SELECT otherIncome FROM money WHERE userID ={};'.format(ID)).fetchone()[0]
    ret['savings'] = c.execute('SELECT savings FROM money WHERE userID ={};'.format(ID)).fetchone()[0]
    ret['savingPercent'] = c.execute('SELECT savingPercent FROM money WHERE userID ={};'.format(ID)).fetchone()[0]

    return ret

def getAllocateTable(ID):
    ret = {}
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    ret['entertainment'] = c.execute('SELECT entertainment FROM allocate WHERE userID ={};'.format(ID)).fetchone()[0]
    ret['eatOut'] = c.execute('SELECT eatOut FROM allocate WHERE userID ={};'.format(ID)).fetchone()[0]
    ret['shop'] = c.execute('SELECT shop FROM allocate WHERE userID ={};'.format(ID)).fetchone()[0]
    ret['misc'] = c.execute('SELECT misc FROM allocate WHERE userID ={};'.format(ID)).fetchone()[0]
    db.close()
    return ret

# expName TEXT, expType TEXT, expAmt REAL, expDesc TEXT, dateof TEXT
def getVarCost(ID, expID):
    ret = {}
    ret['ID'] = ID
    ret['expID'] = expID
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops    
    ret['expName'] = c.execute('SELECT expName FROM variablecost WHERE userID ={} AND expID = {};'.format(ID,expID)).fetchone()[0]
    ret['expType'] = c.execute('SELECT expType FROM variablecost WHERE userID ={} AND expID = {};'.format(ID,expID)).fetchone()[0]
    ret['expAmt'] = c.execute('SELECT expAmt FROM variablecost WHERE userID ={} AND expID = {};'.format(ID,expID)).fetchone()[0]
    ret['expDesc'] = c.execute('SELECT expDesc FROM variablecost WHERE userID ={} AND expID = {};'.format(ID,expID)).fetchone()[0]
    ret['dateof'] = c.execute('SELECT dateof FROM variablecost WHERE userID ={} AND expID = {};'.format(ID,expID)).fetchone()[0]
    db.close()
    return ret

def getAllVarCost(ID):
    ret = []
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
    c = db.cursor()    
    maxID = c.execute('SELECT max(expID) FROM variablecost WHERE userID = {};'.format(ID)).fetchone()[0]
    if maxID == None:
        print "No var cost exist"
        return None
    else:
        for i in range(maxID+1):
            ret.append(getVarCost(ID,i))
    db.close()
    return ret

# userID INTEGER, fixedID INTEGER, fixedName TEXT, fixedAmt REAL, fixedType TEXT, fixedDesc TEXT
def getFixCost(ID, fixedID):
    ret = {}
    ret['ID'] = ID
    ret['fixedID'] = fixedID
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops    
    ret['fixedName'] = c.execute('SELECT fixedName FROM fixedcost WHERE userID ={} AND fixedID = {};'.format(ID, fixedID)).fetchone()[0]
    ret['fixedType'] = c.execute('SELECT fixedType FROM fixedcost WHERE userID ={} AND fixedID = {};'.format(ID, fixedID)).fetchone()[0]
    ret['fixedAmt'] = c.execute('SELECT fixedAmt FROM fixedcost WHERE userID ={} AND fixedID = {};'.format(ID, fixedID)).fetchone()[0]
    ret['fixedDesc'] = c.execute('SELECT fixedDesc FROM fixedcost WHERE userID ={} AND fixedID = {};'.format(ID, fixedID)).fetchone()[0]
    db.close()
    return ret   

def getAllFixCost(ID):
    ret = []
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
    c = db.cursor()    
    maxID = c.execute('SELECT max(fixedID) FROM fixedcost WHERE userID = {};'.format(ID)).fetchone()[0]
    if maxID == None:
        print "No fix cost exist"
        return None
    else:
        for i in range(maxID+1):
            ret.append(getFixCost(ID,i))
    db.close()
    return ret 
#========
#TESTING

if __name__ == '__main__':     
    #TESTING

    tableCreation()

    #print getAllVarCost(0)
    #print getVarCost(0,0)
    #print getAllocateTable(0)
    #print getUserID("x")

    #updateMoneyTable(3,4,4,4,4,4)
    #print getMoneyTable(3)

    #add users
    #addUser('eric12', '123', 'eric')
    #print getUserID('eric1')
