from flask import Flask, render_template, request, session, url_for, flash, redirect
from utils.accounts import authenticate, register
from utils.db_builder import checkUsername, getPass, getUserID, getUserName, getConfig, setConfig, addUser

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
    ID = getUserID(session['user'])
    setConfig(ID)
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
    return render_template("home.html",config=configBool)

@app.route('/budget', methods = ['POST','GET'])
def budget():
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
    
    

if __name__=='__main__':
	app.run(debug=True)
