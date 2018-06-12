
import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O
import hashlib
import uuid
import datetime
import os

DIR = os.path.dirname(__file__) or '.'
DIR += '/../data/data.db'

def tableCreation():
    if not os.path.isfile(DIR):
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

        variablecost_table = 'CREATE TABLE variablecost (userID INTEGER, expID INTEGER, expName TEXT, expAmt TEXT, expType TEXT, expDesc TEXT, dateof TEXT);'
        c.execute(variablecost_table)

        stocks_table = 'CREATE TABLE stocks (userID INTEGER, stockID INTEGER, ticker TEXT, shares INTEGER, purdate TEXT, purprice DATE);'
        c.execute(stocks_table)

        update_table = 'CREATE TABLE update_table (userID INTEGER, updateID INTEGER, month INT, day INT, year INT, currentMoney REAL, savings REAL);'
        c.execute(update_table)


        db.commit()
        db.close()

        dummyUser()

def dummyUser():
    addUser('z', 'z', 'z', 1)
    addMoneyTable (0, 1000, 500, 0, 7000, 10.8)
    addAllocateTable (0, 100, 150, 200, 300, 500, 700)
    addVarCost(0, "Went to the spa", 'shop', 35, "Cucumbers",'2017-06-17')
    addVarCost(0, "Vacation to Laos", 'entertainment', 5000, "Vacation time~",'2017-08-17')
    addVarCost(0, "Halloween costume", 'entertainment', 40, "Boo!!!",'2017-10-20')
    addVarCost(0, "Infinity Wars", 'entertainment', 40, "Thanos.",'2017-12-25')
    addVarCost(0, "Dinner at Dorsia", 'eatOut', 500, "Nice dinner.", '2018-01-30')
    addVarCost(0, "Wedding", 'event', 1500, "Went to Frank's wedding.", '2018-02-04')
    addVarCost(0, "60 pounds of mac and cheese", 'grocery', 500, "Dinner for the rest of the year.",'2018-03-05')
    addFixCost(0, "Electricity", 150 , "utility", "Basic utility.")
    addFixCost(0, "Heating", 70 , "utility", "Basic utility.")
    addFixCost(0, "Water", 50 , "utility", "Basic utility.")
    addFixCost(0, "Health Insurance", 100 , "insurance", "In case I die.")
    addFixCost(0, "Netflix", 10 , "membership", "TV and movies.")
    addFixCost(0, "Subway", 120 , "Transportation", "Monthly subway rides.")



#===========================================================================================================================================

#MUTATORS/ADD VALUES TO TABLES

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
    c.execute('DELETE FROM money WHERE userID = {};'.format(ID))
    command = 'INSERT INTO money VALUES (?,?,?,?,?,?);'
    c.execute(command,[ID,currentMoney,monthIncome,otherIncome,savings,savingPercent])


    #userID INTEGER, updateID INTEGER, month INT, day INT, year INT, currentMoney REAL, savings REAL
    today = datetime.datetime.now()
    mon = today.month
    day = today.day
    yr = today.year
    command = 'INSERT INTO update_table VALUES (?,?,?,?,?,?,?);'
    c.execute(command, [ID, 0, mon, day, yr, currentMoney, savings])

    db.commit()
    db.close()  

def updateMoneyTable(ID, currentMoney, monthIncome, otherIncome, savings, savingPercent):
    db = sqlite3.connect(DIR)
    c = db.cursor()
    c.execute('DELETE FROM allocate WHERE userID = {};'.format(ID))
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
def addVarCost(ID, expName, expType, expAmt, expDesc, date = None):
    #print "========================="
    #print date
    #print "========================="
    if date == None:
        date = (datetime.datetime.now()).strftime('%Y-%m-%d')
    db = sqlite3.connect(DIR)
    c = db.cursor() 

    expID = c.execute('SELECT max(expID) FROM variablecost WHERE userID = {}'.format(ID)).fetchone()[0]
    if expID == None:
        expID = 0
    else:
        expID = int(expID) + 1

    print "\n\n\n"
    c.execute('INSERT INTO variablecost VALUES (?,?,?,?,?,?,?);',[ID, expID, expName, expAmt, expType, expDesc, date])
    db.commit()
    db.close()

    changeMoney(ID, -1, 0, expAmt, date)

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
    changeMoney(ID, -1, 0, fixedAmt)

def addStock(ID, ticker, shares, purprice):
    date = (datetime.datetime.now()).strftime('%Y-%m-%d')
    db = sqlite3.connect(DIR)
    c = db.cursor() 

    stockID = c.execute('SELECT max(stockID) FROM stocks WHERE userID = {}'.format(ID)).fetchone()[0]
    if stockID == None:
        stockID = 0
    else:
        stockID = int(stockID) + 1

    print "\n\n\n"
    c.execute('INSERT INTO stocks VALUES (?,?,?,?,?,?);',[ID, stockID, ticker, shares, date, purprice])
    db.commit()
    db.close()  

#sign
#   -1 = subtract
#   +1 = increase
#location
#    0 = currentMoney
#    1 = savings


def changeMoney(ID, sign, location, amt, date = None):
    db = sqlite3.connect(DIR)
    c = db.cursor()

    currentMoney = c.execute('SELECT currentMoney FROM money WHERE userID = {}'.format(ID)).fetchone()[0]
    savings = c.execute('SELECT savings FROM money WHERE userID = {}'.format(ID)).fetchone()[0]


    if location == 0:
        currentMoney = currentMoney + float(amt)*sign
        #print "========"
        #print float(amt)*sign
        #print "========"
        c.execute('UPDATE money SET currentMoney = {} WHERE userID = {}'.format(currentMoney, ID))

    else:
        savings = savings + float(amt)*sign
        c.execute('UPDATE money SET savings = {} WHERE userID = {}'.format(savings, ID))

    db.commit()
    db.close() 

    addUpdate(ID, currentMoney, savings, date)

def addUpdate(ID, currentMoney, savings, date=None):
    print "Adding Update===================================="
    print date
    print "================================================="
    db = sqlite3.connect(DIR)
    c = db.cursor()

    #userID INTEGER, updateID INTEGER, month INT, day INT, year INT, currentMoney REAL, savings REAL
    if date == None:
        today = datetime.datetime.now()
        mon = today.month
        day = today.day
        yr = today.year
    else:
        yr = int(date.split('-')[0])
        mon = int(date.split('-')[1])
        day = int(date.split('-')[2])

    updateID = c.execute('SELECT max(updateID) FROM update_table WHERE userID = {}'.format(ID)).fetchone()[0]
    if updateID == None:
        updateID = 0
    else:
        updateID = int(updateID) + 1


    command = 'INSERT INTO update_table VALUES (?,?,?,?,?,?,?);'
    c.execute(command, [ID, updateID, mon, day, yr, currentMoney, savings])

    db.commit()
    db.close()  



def bigUpdater(ID):

    moneyTable = getMoneyTable(ID)
    updateTable = getRecentUpdateTable(ID)
    fixcost =  getAllFixCost(ID)
    #for i in range(len(fixcost)):
    #    print fixcost[i]['fixedAmt']



    today = datetime.datetime.now()
    mon = today.month
    yr = today.year 

    multiplier = (yr - updateTable['year'])*12 + (mon - updateTable['month'])
    #print "Multiplier==============================="
    #print multiplier
    #print "========================================="

    if multiplier > 0:
        totalIncome = float(moneyTable['monthIncome']) + float(moneyTable['otherIncome'])
        addSaving = float("%.2f" % (float(moneyTable['savingPercent'])*0.01*totalIncome)) * multiplier
        addition = float("%.2f" % ((1.0-float(moneyTable['savingPercent']))*0.01*totalIncome)) * multiplier
        changeMoney(ID, 1, 0, addition)
        changeMoney(ID, 1, 1, addSaving)

        for i in range(len(fixcost)):
            costOf = multiplier * float(fixcost[i]['fixedAmt'])
            #print "Fixed Amounts===================="
            print costOf
            changeMoney(ID, -1, 0, costOf)
        #print "======================="

    print "All cost were updated"
 
#==================================================================================================================================

#ACCESSORS/GETTING

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
        #print "user:"
        #print user
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
    ret['grocery'] = c.execute('SELECT grocery FROM allocate WHERE userID ={};'.format(ID)).fetchone()[0]
    ret['event'] = c.execute('SELECT event FROM allocate WHERE userID ={};'.format(ID)).fetchone()[0]
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


def getAllVarCost(ID, timerange = 'all'):
    today = datetime.datetime.now()
    mon = today.month
    yr = today.year

    ret = []
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
    c = db.cursor()    
    maxID = c.execute('SELECT max(expID) FROM variablecost WHERE userID = {};'.format(ID)).fetchone()[0]
    if maxID == None:
        print "No var cost exist"
        return None
    else:
        for i in range(maxID+1):
            try:
                tempMonth = int(getVarCost(ID,i)['dateof'].split('-')[1])
                tempYear = int(getVarCost(ID,i)['dateof'].split('-')[0])
                if timerange == 'all':
                    ret.append(getVarCost(ID,i))
                elif timerange == 'month':
                    if tempYear == yr and tempMonth == mon:
                        ret.append(getVarCost(ID,i))
                elif timerange == 'year':
                    if tempYear == yr:
                        ret.append(getVarCost(ID,i))
            except:
                pass

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
            try:
                ret.append(getFixCost(ID,i))
            except:
                pass
    db.close()
    return ret 


#CREATE TABLE stocks (userID INTEGER, stockID INTEGER, ticker TEXT, shares INTEGER, purdate TEXT, purprice DATE)'
#ONLY BY TICKER
def getStock(ID, stockID):
    ret = {}
    ret['ID'] = ID
    ret['stockID'] = stockID
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops    
    ret['ticker'] = c.execute('SELECT ticker FROM stocks WHERE userID ={} AND stockID = {};'.format(ID, stockID)).fetchone()[0]
    ret['shares'] = c.execute('SELECT shares FROM stocks WHERE userID ={} AND stockID = {};'.format(ID, stockID)).fetchone()[0]
    ret['purdate'] = c.execute('SELECT purdate FROM stocks WHERE userID ={} AND stockID = {};'.format(ID, stockID)).fetchone()[0]
    ret['purprice'] = c.execute('SELECT purprice FROM stocks WHERE userID ={} AND stockID = {};'.format(ID, stockID)).fetchone()[0]
    db.close()
    return ret    

def getAllStocks(ID):
    ret = []
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
    c = db.cursor()    
    maxID = c.execute('SELECT max(stockID) FROM stocks WHERE userID = {};'.format(ID)).fetchone()[0]
    if maxID == None:
        print "No stocks exist"
        return None
    else:
        for i in range(maxID+1):
            ret.append(getStock(ID,i))
    db.close()
    return ret   


#userID INTEGER, updateID INTEGER, month INT, day INT, year INT, currentMoney REAL, savings REAL
def getUpdateTable(ID, updateID):
    ret = {}
    ret['ID'] = ID
    ret['updateID'] = updateID
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops    
    ret['month'] = c.execute('SELECT month FROM update_table WHERE userID ={} AND updateID = {};'.format(ID, updateID)).fetchone()[0]
    ret['day'] = c.execute('SELECT day FROM update_table WHERE userID ={} AND updateID = {};'.format(ID, updateID)).fetchone()[0]
    ret['year'] = c.execute('SELECT year FROM update_table WHERE userID ={} AND updateID = {};'.format(ID, updateID)).fetchone()[0]
    ret['currentMoney'] = c.execute('SELECT currentMoney FROM update_table WHERE userID ={} AND updateID = {};'.format(ID, updateID)).fetchone()[0]
    ret['savings'] = c.execute('SELECT savings FROM update_table WHERE userID ={} AND updateID = {};'.format(ID, updateID)).fetchone()[0]
    db.close()
    return ret 

def getAllUpdateTable(ID):
    ret = []
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
    c = db.cursor()    
    maxID = c.execute('SELECT max(updateID) FROM update_table WHERE userID = {};'.format(ID)).fetchone()[0]
    if maxID == None:
        print "No update table exist"
        return None
    else:
        for i in range(maxID+1):
            ret.append(getUpdateTable(ID,i))
    db.close()
    return ret

def getRecentUpdateTable(ID):
    db = sqlite3.connect(DIR)
    c = db.cursor()    
    maxID = c.execute('SELECT max(updateID) FROM update_table WHERE userID = {};'.format(ID)).fetchone()[0]
    db.close()
    return getUpdateTable(ID, maxID)


def getPercentageByAllocation(ID, timerange = "all"):
    entertain = 0
    eat = 0
    shop = 0
    misc = 0
    groc = 0
    event = 0

    allocate = getAllocateTable(ID)
    vartable = getAllVarCost(ID, timerange)


    today = datetime.datetime.now()
    mon = today.month
    yr = today.year
    updateTable = getUpdateTable(ID, 0)
    datedifference = (yr - updateTable['year'])*12 + (mon - updateTable['month'])
    multiplier = 1

    if timerange == 'year' and datedifference > 12:
        multiplier = 12
    elif timerange == 'year' and datedifference < 12:
        multiplier = multiplier + 1
    elif timerange == 'all':
        multiplier = multiplier + 1
    else:
        multiplier = 1


    for each in vartable:
        if each['expType'] == 'eatOut':
            eat+= float(each['expAmt'])
        elif each['expType'] == 'entertainment':
            entertain+= float(each['expAmt'])
        elif each['expType'] == 'shop':
            shop+= float(each['expAmt'])
        elif each['expType'] == 'misc':
            misc+= float(each['expAmt'])
        elif each['expType'] == 'grocery':
            groc+= float(each['expAmt'])
        elif each['expType'] == 'event':
            event+= float(each['expAmt'])                   

    #prevent division by zero
    for each in allocate:
        if allocate[each] == 0:
            allocate[each] == 0.01


    entertain = float("%.2f" % (entertain / (allocate['entertainment'] * multiplier) * 100))
    eat = float("%.2f" % (eat / (allocate['eatOut'] * multiplier) * 100))
    shop = float("%.2f" % (shop / (allocate['shop'] * multiplier) * 100))
    misc = float("%.2f" % (misc / (allocate['misc'] * multiplier) * 100))
    groc = float("%.2f" % (groc / (allocate['grocery'] * multiplier) * 100))
    event = float("%.2f" % (event / (allocate['event'] * multiplier) * 100))

    percentDict = {}
    percentDict['eatOut'] = eat
    percentDict['entertain'] = entertain
    percentDict['shop'] = shop
    percentDict['misc'] = misc
    percentDict['grocery'] = groc
    percentDict['event'] = event

    return percentDict

    #print percentDict



   

#==================================================================================================================================
#REMOVING


def removeVarCost(ID, expID):
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
    c = db.cursor() 
    command = 'DELETE FROM variablecost WHERE userID ={} AND expID = {};'    
    c.execute(command.format(ID, expID))
    db.commit()         
    db.close()
    print "Removed ID {} from entry {} successfully".format(ID, expID)


def removeFixedCost(ID, fixedID):
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
    c = db.cursor() 
    command = 'DELETE FROM fixedcost WHERE userID ={} AND  fixedID = {};'    
    c.execute(command.format(ID, fixedID))
    db.commit()
    db.close()
    print "Removed ID {} from entry {} successfully".format(ID, fixedID)

def removeStock(ID, stockID):
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
    c = db.cursor() 
    command = 'DELETE FROM stocks WHERE userID ={} AND stockID = {};'    
    c.execute(command.format(ID, stockID))
    db.commit()
    db.close()
    print "Removed ID {} from entry {} successfully".format(ID, stockID)





#==================================================================================================================================

if __name__ == '__main__':  

    tableCreation()
    dummyUser()  

    #print getPercentageByAllocation(0,'all')
    #print getPercentageByAllocation(0,'year')
    #print getPercentageByAllocation(0,'month')


    #print getAllVarCost(0)


    #print getAllVarCost(0)
    #getPercentageByAllocation(0)
    #print getAllVarCost(0, 'year')
    #print getAllUpdateTable(0)
    #changeMoney(0, 1, 1, 10000)

    #bigUpdater(0)

    #print getRecentUpdateTable(0)
    #print getMoneyTable(0)
    #print getAllUpdateTable(0) 
    #TESTING

    #changeMoney(0,1,0,9999)
    #removeFixedCost(0,1)
    #tableCreation()

    #print getAllVarCost(0)
    #print getVarCost(0,0)
    #print getAllocateTable(0)
    #print getUserID("x")

    #updateMoneyTable(3,4,4,4,4,4)
    #print getMoneyTable(3)

    #add users
    #addUser('eric12', '123', 'eric')
    #print getUserID('eric1')
    pass