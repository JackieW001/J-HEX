from flask import Flask, render_template, request, session, url_for, flash, redirect
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
        return "Hi"
    else:
        return render_template("login.html")


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
        #for x in session:
            #print session[x]
        return redirect( url_for('home') )
    if result == BAD_USER:
        flash('Incorrect username. Please try again.')
        return redirect( url_for('root') )
    if result == BAD_PASS:
        flash('Incorrect password. Please try again.')
        return redirect( url_for('root') )
    return redirect( url_for('root') )

if __name__=='__main__':
	app.run(debug=True)