from flask import Flask, render_template, request, session, url_for, flash, redirect
from utils.accounts import authenticate, register
from utils.db_builder import tableCreation, checkUsername, getPass, getUserID, getUserName, getConfig, setConfig, addUser
from utils.db_builder import addMoneyTable, getMoneyTable, updateMoneyTable, addAllocateTable, getAllocateTable, updateAllocateTable
from utils.db_builder import addVarCost, getVarCost, addFixCost,getAllFixCost,getAllVarCost
from utils.api import get_apikey, get_info, get_date, get_today, get_last_days

#from markupsafe import Markup

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
    print "User: " + user
    password = request.form['pass']
    print "Pass: " + password
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
    #ID = getUserID(session['user'])
    #setConfig(ID)
    session.pop('user')
    flash('You have been logged out successfully')
    return redirect(url_for('root'))

#============================================================================

@app.route('/home', methods = ['POST','GET'])
def home():
    ID = getUserID(session['user'])
    print "User:"
    print session['user']
    print "UserID:"
    print ID
    configBool = getConfig(ID)
    print "Config Boolean:" 
    print configBool


    print "TESTING \n\n\n"
    vartable = getAllVarCost(ID)
    print vartable
    fixtable = getAllFixCost(ID)

    if vartable == None or fixtable == None:
        return render_template("home.html",config=configBool)
    else:
        print "working"
        return render_template("home.html",config=configBool, vartable = vartable, fixtable = fixtable)


# NOT REAL PAGES ============================================================================
@app.route('/config', methods = ['POST','GET'])
def config():
    ID = getUserID(session['user'])
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


    return render_template("home.html",config=configBool)

@app.route('/budget', methods = ['POST','GET'])
def budget():
    return "This page doesn't work"
    '''
    ID = getUserID(session['user'])
    name = request.form['name']
    inputtype = request.form['type']
    amt = request.form['amt']
    budget = request.form['budget']
    desc = request.form['desc']
    date = request.form['date']
    f = "data/data.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    expCount = c.execute('SELECT COUNT(*) FROM variableCosts;')
    new_expID = 0
    for x in expCount:
        new_expID = x[0]
    c.execute('INSERT INTO variableCosts VALUES (?,?,?,?,?,?,?,?)',[ID, new_expID, name, inputtype, amt, budget, desc, date])
    db.commit()
    db.close()
    '''

@app.route('/varcost', methods = ['POST','GET'])
def varcost():
    ID = getUserID(session['user'])
    expName = request.form['expName']
    expAmt = request.form['expAmt']
    exptype = request.form['type']
    expDesc = request.form['expDesc']
    addVarCost(ID, expName, expAmt, exptype, expDesc)
    return redirect(url_for('root'))

@app.route('/fixcost', methods = ['POST','GET'])
def fixcost():
    ID = getUserID(session['user'])
    fixedName = request.form['fixedName']
    fixedAmt = request.form['fixedAmt']
    fixedtype = request.form['type']
    fixedDesc = request.form['fixedDesc']
    addFixCost(ID, fixedName, fixedAmt, fixedtype, fixedDesc)
    return redirect(url_for('root'))

#============================================================================
@app.route('/settings', methods = ['POST','GET'])
def settings():
    ID = getUserID(session['user'])
    return "This page doesn't work"



#STOCKS=========================================#=============================
@app.route('/stocks', methods = ['POST','GET'])
def stocks():    
    return render_template("stocks.html")

@app.route('/stocksubmit', methods = ['POST','GET'])
def stocksubmit():    
    stockName = request.form['stockName']
    #DATA SPLITTING
    todayData = get_last_days(stockName, "TIME_SERIES_DAILY", 1)
    weekData = get_last_days(stockName, "TIME_SERIES_DAILY", 7)
    #monthData = get_last_days(stockName, "TIME_SERIES_WEEKLY", 8)

    pp = pprint.PrettyPrinter(indent=4)

    todayData = pp.pformat(todayData)
    weekData = pp.pformat(weekData)

    #monthData = pp.pformat(monthData)

    #return render_template("displayStocks.html", today = todayData, week = weekData, month = monthData)
    return render_template("displayStocks.html", today = todayData, week = weekData, month = "filler")
    #return render_template("displayStocks.html", today = Markup(todayData), week = Markup(weekData), month = "filler")


#print(get_info('MSFT', "TIME_SERIES_DAILY"))                                                                                                                                    
#print(get_date('MSFT', '2018-05-14'))                                                                                                                                           
#print(get_today('MSFT'))
#pp.pprint(get_last_days("MSFT", "TIME_SERIES_DAILY", 7))                                                                                                                       
#pp.pprint(get_last_days("MSFT", "TIME_SERIES_WEEKLY", 8))                                                                                                                       
#pp.pprint(get_last_days("MSFT", "TIME_SERIES_MONTHLY", 12))                                                                                                                     
#print add_zero("05")  


#=================================================================
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


#RUNNING==========================================================
if __name__=='__main__':
	app.run(debug=True, host="0.0.0.0")
    
