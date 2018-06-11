from flask import Flask, render_template, request, session, url_for, flash, redirect
from utils.accounts import authenticate, register
from utils.db_builder import tableCreation, checkUsername, getPass, getUserID, getUserName, getConfig, setConfig, addUser
from utils.db_builder import addMoneyTable, getMoneyTable, updateMoneyTable, addAllocateTable, getAllocateTable, updateAllocateTable
from utils.db_builder import addVarCost, getVarCost, addFixCost,getAllFixCost,getAllVarCost, removeVarCost, removeFixedCost, bigUpdater
from utils.db_builder import getAllUpdateTable
from utils.api import get_apikey, get_info, get_date, get_today, get_last_days, add_zero
from utils.table_builder import addZero

#from markupsafe import Markup


#   getMoneyTable -> gets currentmoney/savings etc

import pprint
import sqlite3
import os
app = Flask(__name__)


#Login Stuff
app.secret_key = os.urandom(32)
BAD_USER = -1
BAD_PASS = -2
GOOD = 1
user = ""



@app.route('/')
def root():
    #redirect to home if there is a session
    #otherwise display login/register page
    tableCreation()


    if session.has_key('user'):
        return redirect( url_for('home') )
    else:
        return render_template("login.html")

#LOGIN/REGISTER==========================================================
@app.route('/login', methods = ['POST','GET'])
def login():
    user = request.form['user']
    #print user
    passw = request.form['pass']
    #print passw

    result = authenticate(user, passw)
    #print result

    #if successful, redirect to home
    #otherwise redirect back to root with flashed message 
    if result == GOOD:
        session['user'] = user
        #ID = getUserID(user)
        #print "ID: " + ID
        #for x in session:
            #print session[x]
        return redirect( url_for('home') )
    if result == BAD_USER:
        flash('Incorrect username. Please try again.')
        return redirect( url_for('root') )
    if result == BAD_PASS:
        flash('Incorrect password. Please try again.')
        return redirect( url_for('root') )
    #print "not supposed to get here" + str(ID)
    return redirect( url_for('root') )

@app.route('/register', methods = ['POST', 'GET'])
def register():
    user = request.form['user']
    #print "User: " + user
    password = request.form['pass']
    #print "Pass: " + password
    name = request.form['name']

    if checkUsername(user):
        flash('Username unavailable. Please try another username.')
        return redirect(url_for('root'))
    else:
        addUser(user,password,name, 0)
        session['user'] = user
        #ID = getUserID(user)
        #print "ID: " + ID
        return redirect( url_for('home'))


@app.route('/logout', methods = ['POST','GET'])
def logout():
    try:
        ID = getUserID(session['user'])
    except:
        return redirect( url_for('root'))
    session.pop('user')
    flash('You have been logged out successfully')
    return redirect(url_for('root'))

#============================================================================

@app.route('/home', methods = ['POST','GET'])
def home():
    try:
        ID = getUserID(session['user'])
    except:
        return redirect( url_for('root'))
    #print "User:"
    #print session['user']
    #print "UserID:"
    #print ID
    configBool = getConfig(ID)
    #print "Config Boolean:" 
    #print configBool

    vartable = addZero(getAllVarCost(ID),"var")

    fixtable = addZero(getAllFixCost(ID),"fix")

    try:
        moneyTable = getMoneyTable(ID)
        moneyTable['currentMoney'] = '${:,.2f}'.format(float(moneyTable['currentMoney']))
        moneyTable['savings'] = '${:,.2f}'.format(float(moneyTable['savings']))

    except:
        moneyTable = {'otherIncome': 0, 'currentMoney': 0, 'savings': 0, 'monthIncome': 0, 'savingPercent': 0}

    try:
        bigUpdater(ID)
    except:
        pass

    if vartable == None:
        vartable = []
    if fixtable == None:
        fixtable = []

    graphData = getAllUpdateTable(ID)
    print "before"
    print graphData
    print "after"

    years = []
    months = []
    days = []
    dates = []
    currMon = []
    saving = []

    for dict in graphData:
        years.append(dict['year']) 
        months.append(dict['month']) 
        days.append(dict['day']) 
        currMon.append(dict['currentMoney']) 
        saving.append(dict['savings']) 

    print years
    print months
    print days
    print currMon
    print saving

    return render_template("home.html",config=configBool, vartable = vartable, fixtable = fixtable, moneyTable = moneyTable)

    #=====GRAPHIN STUFF====
'''
'''
    #======================        




# NOT REAL PAGES ============================================================================
@app.route('/config', methods = ['POST','GET'])
def config():
    try:
        ID = getUserID(session['user'])
    except:
        return redirect( url_for('root'))
    setConfig(ID)
    configBool = getConfig(ID)

    currentMoney = str(request.form['currentMoney'])
    monthIncome = str(request.form['monthIncome'])
    otherIncome = str(request.form['otherIncome'])
    savings = str(request.form['savings'])
    savingPercent = str(request.form['savingPercent'])

    addMoneyTable(ID, currentMoney,monthIncome,otherIncome,savings,savingPercent)

    entertain = str(request.form['entertainment'])
    eatOut = str(request.form['eatOut'])
    shop = str(request.form['shop'])
    misc =  str(request.form['misc'])
    event = str(request.form['event'])
    grocery = str(request.form['grocery'])

    addAllocateTable(ID, entertain, eatOut, shop, misc, grocery, event)
    try:
        moneyTable = getMoneyTable(ID)
    except:
        moneyTable = {'otherIncome': 0, 'currentMoney': 0, 'savings': 0, 'monthIncome': 0, 'savingPercent': 0}

    return redirect(url_for('home'))

@app.route('/budget', methods = ['POST','GET'])
def budget():
    return render_template("budget_form.html")


@app.route('/varcost', methods = ['POST','GET'])
def varcost():
    try:
        ID = getUserID(session['user'])
    except:
        return redirect( url_for('root'))
    expName = request.form['expName']
    expAmt = request.form['expAmt']
    exptype = request.form['type']
    expDesc = request.form['expDesc']
    addVarCost(ID, expName,exptype, expAmt, expDesc)
    return redirect(url_for('root'))

@app.route('/fixcost', methods = ['POST','GET'])
def fixcost():
    try:
        ID = getUserID(session['user'])
    except:
        return redirect( url_for('root'))
    fixedName = request.form['fixedName']
    fixedAmt = request.form['fixedAmt']
    fixedtype = request.form['type']
    fixedDesc = request.form['fixedDesc']
    addFixCost(ID, fixedName, fixedAmt, fixedtype, fixedDesc)
    return redirect(url_for('root'))


#============================================================================
@app.route('/settings', methods = ['POST','GET'])
def settings():
    try:
        ID = getUserID(session['user'])
    except:
        return redirect( url_for('root'))
    configBool = getConfig(ID)

    vartable = addZero(getAllVarCost(ID),"var")

    fixtable = addZero(getAllFixCost(ID),"fix")

    try:
        moneyTable = getMoneyTable(ID)
        allocateTable = getAllocateTable(ID)

        for each in moneyTable:
            moneyTable[each] = '{:,.2f}'.format(moneyTable[each])
        for each in allocateTable:
            allocateTable[each] = '{:,.2f}'.format(allocateTable[each])

    except:
        moneyTable = {'otherIncome': 0, 'currentMoney': 0, 'savings': 0, 'monthIncome': 0, 'savingPercent': 0}
        allocateTable = {'eatOut': 0, 'entertain': 0, 'shop':0, 'misc':0, 'grocery':0, 'event':0}


    if vartable == None:
        vartable = []
    if fixtable == None:
        fixtable = []

    return render_template("settings.html", vartable = vartable, fixtable = fixtable, moneyTable = moneyTable, allocateTable = allocateTable)

@app.route('/removevar', methods = ['POST','GET'])
def removevar():
    ID = getUserID(session['user'])
    for expID in request.form:
        removeVarCost(ID, expID)
    
    return redirect(url_for('settings'))

@app.route('/removefix', methods = ['POST','GET'])
def removefix():
    ID = getUserID(session['user'])
    for fixedID in request.form:
        removeFixedCost(ID, fixedID)
    
    return redirect(url_for('settings'))

#STOCKS=========================================#=============================
@app.route('/stocks', methods = ['POST','GET'])
def stocks(): 
    try:
        ID = getUserID(session['user'])
    except:
        return redirect( url_for('root'))

    return render_template("stocks.html")

@app.route('/stockdisplay', methods = ['POST','GET'])
def stockdisplay():
    try:
        ID = getUserID(session['user'])
    except:
        return redirect( url_for('root'))

    stockName = request.form['stockName']
    period = request.form['period']
    #print stockName
    #print period
    period = "TIME_SERIES_" + period
    #print period
    data = get_last_days(stockName, period, 12)
    #monthlyData = get_last_days("MSFT", "TIME_SERIES_WEEKLY", 12)
    #yearlyData = get_last_days("MSFT", "TIME_SERIES_MONTHLY", 12)
    return render_template('stockDisplay.html', data_var = data)

#=================================================================
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    flash('You are on a bad page! Return back to login.')
    return render_template('404.html'), 404


#RUNNING==========================================================
if __name__=='__main__':
	app.run(debug=True, host="0.0.0.0")
    
