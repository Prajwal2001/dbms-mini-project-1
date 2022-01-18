from flask import Flask, render_template, redirect, request, session
from database import Database

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
db = Database()

@app.route("/")
def redirectPg():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    logout()
    if request.method == 'POST':
        userData = db.checkUser([request.form.get('email'), request.form.get('password')])
        if userData:
            session["uId"] = userData[0]
            session["name"] = userData[3]
            session['cartCount'] = db.getCartCount(session['uId'])
            return redirect('/index')
        else:
            return render_template("login.html", loginError=True, title='Login')
    else:
        return render_template("login.html", title='Login')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        response = db.addUser(request.form)
        return redirect('/login', code=302) if response else render_template("signup.html", status=response)
    else:
        return render_template("signup.html", status=True, title='SignUp')

@app.route("/logout")
def logout():
    session['uId'] = None
    session['name'] = None
    session['cartCount'] = 0
    return redirect('/login')

@app.route("/index")
def home():
    return render_template("index.html", cartCount = session['cartCount'], name=session["name"]) if session['uId'] else redirect('/login', code=302)

@app.route("/changePassword", methods=['GET','POST'])
def changePassword():
    if request.method == 'POST':
        msg = db.changePassword(session['uid'], request.form)
    return render_template("changePassword.html", cartCount = session['cartCount'], name=session["name"], msg=msg) if session['uId'] else redirect('/login', code=302)

@app.route("/editUser", methods = ['GET','POST'])
def editUser():
    if request.method == 'POST':
        session['name'] = db.editUser(session['uId'], request.form)
        return redirect('/editUser')
    else:
        return render_template("editUser.html", cartCount = session['cartCount'], name=session["name"], userData = db.getUser(session['uId']), title='Edit User')

if(__name__=='__main__'):
    app.run(debug=True, port=4000)