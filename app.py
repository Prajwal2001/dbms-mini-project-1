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
    session["uId"] = None
    session["email"] = None
    if request.method == 'POST':
        userData =  db.checkUser([request.form.get('mailId'), request.form.get('password')])
        if userData:
            session["uId"] = userData[0]
            session["email"] = userData[1]
            return redirect('/home')
        else:
            return render_template("login.html", status=False, title='Login')
    else:
        return render_template("login.html", status=True, title='Login')


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
    session["email"] = None
    return redirect('/login')

@app.route("/home")
def home():
    return render_template("home.html", email=session["email"]) if session['uId'] else redirect('/login', code=302)

if(__name__=='__main__'):
    app.run(debug=True, port=4000)