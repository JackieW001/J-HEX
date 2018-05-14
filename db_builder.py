
import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O
import hashlib
import uuid


def tableCreation():
    f="data/data.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    #Create the users table
    users_table = 'CREATE TABLE users (username TEXT, password BLOB, userID INTEGER, name TEXT);'
    c.execute(user_table)
    #Create the stories table
    money_table = 'CREATE TABLE money (userID INTEGER, currentMoney REAL, monthIncome REAL, otherIncome REAL, savings REAL);'
    c.execute(stories_table)
    #Create the updates table
    fixedcost_table = 'CREATE TABLE fixedcost (userID INTEGER, expID INTEGER, fixedName TEXT, fixedAmt REAL, fixedDesc TEXT);'
    c.execute(update_table)

    variablecost_table = 'CREATE TABLE variablecost (userID INTEGER, expID INTEGER, expName TEXT, expAmt REAL, expBud REAL, expDesc TEXT, dateof TEXT);'
    c.execute(update_table)

    stocks_table = 'CREATE TABLE stocks (userID INTEGER, expID INTEGER, shares INTEGER, purdate TEXT, purprice DATE);'
    c.execute(update_table)


    db.commit()
    db.close()