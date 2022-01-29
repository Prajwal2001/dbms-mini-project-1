from flask import Flask, render_template, request, redirect, url_for,session
import re
import mysql.connector

app=Flask(__name__)

app.secret_key = '5791628bb0b13ce0c676dfde280ba245'

db = mysql.connector.connect(
    host="localhost",
    user='root',
    password='root',
    database='hospital',
    autocommit=True
)


cursor = db.cursor()

@app.route("/")
def redirectPg():
    if 'loggedIn' in session:
        if session['loggedIn']==1:
            return redirect(url_for('index'))
        elif session['loggedIn']==2:
            return redirect(url_for('doctorIndex'))
        else:
            return redirect(url_for('adminIndex'))
    return redirect('/home')

@app.route('/home')
def home():
    if 'loggedIn' in session:
        return redirect(url_for('redirectPg'))
    return render_template('home.html')

@app.route('/logout')
def logout():
   session.pop('loggedIn', None)
   session.pop('mailId', None)
   return redirect(url_for('home'))

@app.route("/index",methods=['GET','POST'])
def index():
    return render_template("index.html", loggedIn = session['loggedIn'])

@app.route('/login',methods=['GET','POST'])
def login():
    msg=''
    if request.method=='POST' and 'mailId' in request.form and 'passwd' in request.form:
        cursor.execute(f'''SELECT * FROM patient WHERE mailId = '{request.form['mailId']}' AND passwd= '{request.form['passwd']}' ''')
        patient=cursor.fetchone()
        if patient:
            session['loggedIn'] = 1
            session['mailId'] = patient[0]
            return redirect('/index')
        else:
            msg = 'Wrong Username or Password !'
    return render_template('login.html', msg = msg)

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        mailId = request.form['mailId']
        passwd = request.form['passwd']
        PName = request.form['PName']
        dob = request.form['dob']
        bloodGroup = request.form['bloodGroup']
        sex = request.form['sex']
        cursor.execute(f'''SELECT * FROM patient WHERE mailId = '{mailId}' ''')
        if cursor.fetchone():
            msg = 'Account already exists !'
        else:
            cursor.execute(f'''INSERT INTO patient VALUES ('{mailId}', '{passwd}', '{PName}', '{dob}', '{bloodGroup}', '{sex}')''')
            return redirect(url_for('login'))
    return render_template('register.html', msg = msg)

@app.route("/display")
def display():
    if 'loggedIn' in session:
        cursor.execute(f'''SELECT * FROM patient WHERE mailId = '{session['mailId']}' ''')
        patient = cursor.fetchone()
        return render_template("display.html", loggedIn=session['loggedIn'], patient = patient)
    return redirect(url_for('login'))

@app.route("/update", methods =['GET', 'POST'])
def update():
    msg = ''
    if 'loggedIn' in session:
        if request.method == 'POST':
            mailId = request.form['mailId']
            passwd = request.form['passwd']
            PName = request.form['PName']
            dob = request.form['dob']
            bloodGroup = request.form['bloodGroup']
            sex = request.form['sex']
            cursor.execute(f'''SELECT * FROM patient WHERE mailId = '{mailId}' ''')
            patient = cursor.fetchone()
            if patient:
                msg = 'Mail-Id already in use!'
            else:
                cursor.execute(f'''UPDATE patient SET  mailId = '{mailId}', passwd = '{passwd}', PName = '{PName}', dob = '{dob}', bloodGroup = '{bloodGroup}', sex = '{sex}'  WHERE mailId = '{session['mailId']}' ''')
                msg = 'You have successfully updated !'
        else:
            cursor.execute(f'''SELECT * FROM patient WHERE mailId = '{session['mailId']}' ''')
            patient = cursor.fetchone()
        return render_template("update.html", loggedIn=session['loggedIn'], patient = patient, msg = msg)
    return redirect(url_for('login'))

@app.route("/appointments")
def appointments():
    if 'loggedIn' in session:
        cursor.execute(f'''SELECT * FROM appointment WHERE mailId = '{session['mailId']}' ''')
        appointment=cursor.fetchall()
        return render_template("appointments.html", appointment = appointment)
    return redirect(url_for('login'))

@app.route('/makeappointment' , methods=['GET','POST'])
def makeappointment():
    msg=''
    if 'loggedIn' in session:
        if request.method=='POST' and  'docMailId' in request.form and 'date_appointment' in request.form:
            docMailId=request.form['docMailId']
            date_appointment=request.form['date_appointment']
            cursor.execute('SELECT * FROM appointment WHERE mailId = %s and date_appointment = %s',(session['mailId'],date_appointment))
            appointment=cursor.fetchone()
            if appointment:
                msg="you had already booked an appointment"
            else:
                cursor.execute('INSERT INTO appointment VALUES (%s,%s,%s)',(session['mailId'],date_appointment,docMailId))
                msg='successfully booked your appointment!!'
                return redirect(url_for('index'))
        else:
            msg = 'appointment failed please rebook again!'
        return render_template('makeappointment.html', msg = msg)
    return redirect(url_for('login'))

@app.route('/adminLogin',methods=['GET','POST'])
def adminLogin():
    msg='Enter Login Credentials'
    if request.method=='POST' and 'mailId' in request.form and 'passwd' in request.form:
        mailId=request.form['mailId']
        passwd = request.form['passwd']
        cursor.execute(f'''SELECT * FROM admin WHERE mailId = '{mailId}' and passwd= '{passwd}' ''')
        receptionist=cursor.fetchone()
        if receptionist:
            session['loggedIn'] = 3
            session['mailId'] = receptionist[0]
            return redirect(url_for('adminIndex'))
        else:
            msg = 'Incorrect username / password !'
    return render_template('adminLogin.html', msg = msg)

@app.route('/adminRegister', methods =['GET','POST'])
def adminRegister():
    msg = ''
    if request.method == 'POST' and 'mailId' in request.form and 'passwd' in request.form and 'adminName' in request.form :
        mailId = request.form['mailId']
        passwd = request.form['passwd']
        adminName = request.form['adminName']
        cursor.execute(f'''SELECT * FROM admin WHERE mailId = '{mailId}' ''')
        receptionist = cursor.fetchone()
        if receptionist:
            msg = 'Account already exists !'
        else:
            cursor.execute('INSERT INTO receptionist VALUES (% s, % s, % s)', (mailId, passwd, adminName))
            msg = 'You have successfully registered !'
            return redirect(url_for('adminIndex'))
    else:
        msg = 'Please fill out the form !'
    return render_template('adminRegister.html', msg = msg)

@app.route("/update_tests" , methods=["GET","POST"])
def update_tests():
    msg=" "
    if 'loggedIn' in session:
        if request.method=='POST' and 'mailId' in request.form and 'test_id' in request.form and 'test_date' in request.form and 'test_analysis' in request.form:
            mailId=request.form['mailId']
            test_id=request.form['test_id']
            test_analysis=request.form['test_analysis']
            test_date=request.form['test_date']
            cursor.execute('INSERT INTO test_descrp VALUES(%s,%s,%s,%s)',(mailId,test_id,test_date,test_analysis))
            msg="Successfully updated"
            return render_template('adminIndex.html',msg=msg)
        else:
            msg='please fill out the form'
    return render_template('update_tests.html', msg = msg)

@app.route("/takes",methods=["GET","POST"])
def takes():
    msg=''
    if 'loggedIn' in session:
        if request.method=='POST' and 'mailId' in request.form and 'medicine_id' in request.form and 'quantity' in request.form and 'takes_date' in request.form:
            mailId=request.form['mailId']
            medicine_id=request.form['medicine_id']
            quantity=request.form['quantity']
            takes_date=request.form['takes_date']
            cursor.execute('INSERT INTO takes VALUES(%s,%s,%s,%s)',(mailId,medicine_id,quantity,takes_date))
            msg="successfully booked medicines"
            return render_template('adminIndex.html',msg=msg)
        else:
            msg='please fill out the form'
    return render_template('takes.html', msg = msg)

@app.route("/recordUpdate",methods=['GET','POST'])
def recordUpdate():
    if 'loggedIn' in session:
        if request.method=='POST':
            mailId=request.form['mailId']
            recordId=request.form['recordId']
            Analysis=request.form['Analysis']
            cursor.execute(f''' INSERT INTO record VALUES('{mailId}','{recordId}','{Analysis}') ''')
            msg="Updated Record"
        else:
            msg='Enter new record details'
        return render_template('recordUpdate.html', loggedIn=session['loggedIn'], msg=msg)
    else:
        redirect(url_for('login'))

@app.route("/adminIndex")
def adminIndex():
    if 'loggedIn' in session:
        return render_template("adminIndex.html", loggedIn = session['loggedIn'])
    return redirect(url_for('adminLogin'))

@app.route("/adminDisplay")

def adminDisplay():
    if 'loggedIn' in session:
        cursor.execute(f'''SELECT * FROM admin WHERE mailId = '{session['mailId']}' ''')
        admin = cursor.fetchone()
        return render_template("adminDisplay.html", loggedIn = session['loggedIn'], admin = admin)
    return redirect(url_for('adminLogin'))

@app.route("/adminUpdate", methods =['GET', 'POST'])
def adminUpdate():
    msg = ''
    if 'loggedIn' in session:
        if request.method == 'POST':
            mailId = request.form['mailId']
            passwd = request.form['passwd']
            adminName = request.form['adminName']
            cursor.execute(f'''SELECT * FROM admin WHERE mailId = '{mailId}' ''')
            admin = cursor.fetchone()
            if not admin:
                msg = 'Account already exists !'
            else:
                cursor.execute(f'''UPDATE admin SET  mailId = '{mailId}', passwd = '{passwd}', adminName = '{adminName}' WHERE mailId = '{session['mailId']}' ''')
                msg = 'You have successfully updated !'
        else:
            cursor.execute(f''' SELECT * FROM admin WHERE mailId = '{session['mailId']}' ''')
            admin = cursor.fetchone()
        return render_template("adminUpdate.html", loggedIn = session['loggedIn'], admin=admin,  msg = msg)
    return redirect(url_for('adminLogin'))

@app.route('/nurseUpdate',methods=['GET','POST'])
def nurseUpdate():
    msg=''
    if 'loggedIn' in session:
        if request.method=='POST':
            nurseId=request.form['nurseId']
            nurseName=request.form['nurseName']
            phoneNumber=request.form['phoneNumber']
            cursor.execute(f'''SELECT * FROM nurse WHERE nurseId = '{nurseId}' ''')
            nurse=cursor.fetchone()
            if nurse:
                msg="Nurse account already exists"
            else:
                cursor.execute('INSERT INTO nurse VALUES(%s,%s,%s)',(nurseId,nurseName,phoneNumber))
                msg="successfully nurse has registered"
                return render_template('adminIndex.html', msg=msg)
    return render_template('nurseUpdate.html', msg = msg)

@app.route('/allocate_rooms',methods=['GET','POST'])
def allocate_rooms():
    msg=''
    if 'loggedIn' in session:
        if request.method=='POST' and 'mailId' in request.form and 'room_no' in request.form and 'block_no' in request.form  and'dateIn' in request.form and 'dateOut' in request.form:
            mailId=request.form['mailId']
            room_no=request.form['room_no']
            block_no=request.form['block_no']
            dateIn=request.form['dateIn']
            dateOut=request.form['dateOut']
            cursor.execute('SELECT * FROM bookings WHERE mailId= % s and dateIn = %s',(mailId,dateIn,))
            bookings = cursor.fetchone()
            if bookings:
                msg = 'You already booked your appointment !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', mailId):
                msg = 'Invalid email address !'
            else:
                cursor.execute('INSERT INTO bookings(mailId, room_no, block_no,dateIn,dateOut) VALUES (% s, % s, % s,% s,% s)', (mailId, room_no, block_no,dateIn,dateOut))
                msg = 'You have successfully booked room for the patient !'
                return redirect(url_for('adminIndex'))
        else:
            msg = 'Please fill out the form !'
            return render_template('allocate_rooms.html', msg = msg)



@app.route('/doctorLogin',methods=['GET','POST'])
def doctorLogin():
    msg=''
    if request.method=='POST' and 'docMailId' in request.form and 'passwd' in request.form:
        docMailId=request.form['docMailId']
        passwd = request.form['passwd']
        cursor.execute(f'''SELECT * FROM doctor WHERE docMailId = '{docMailId}' and passwd= '{passwd}' ''')
        doctor=cursor.fetchone()
        if doctor:
            session['loggedIn'] = 2
            session['docMailId'] = doctor[0]
            return redirect(url_for('doctorIndex'))
        msg = 'Incorrect mail-id or password !'
    return render_template('doctorLogin.html', msg = msg)

@app.route('/doctorRegister', methods =['GET','POST'])
def doctorRegister():
    msg = ''
    if request.method == 'POST':
        docMailId = request.form['docMailId']
        passwd = request.form['passwd']
        docName = request.form['docName']
        availableDate = request.form['availableDate']
        cursor.execute(f'''SELECT * FROM doctor WHERE docMailId = '{docMailId}' ''')
        doctor = cursor.fetchone()
        if doctor:
            msg = 'Account already exists !'
        else:
            cursor.execute(f'''INSERT INTO doctor VALUES ('{docMailId}', '{passwd}', '{docName}', '{availableDate}') ''')
            return redirect(url_for('doctorIndex'))
    return render_template('doctorRegister.html', msg = msg)

@app.route("/doctorIndex")
def doctorIndex():
    if 'loggedIn' in session:
        return render_template("doctorIndex.html", loggedIn = session['loggedIn'])
    return redirect(url_for('doctorLogin'))

@app.route("/doctorDisplay")
def doctorDisplay():
    if 'loggedIn' in session:
        cursor.execute(f'''SELECT * FROM doctor WHERE docMailId = '{session['docMailId']}' ''')
        doctor = cursor.fetchone()
        return render_template("doctorDisplay.html", doctor = doctor, loggedIn = session['loggedIn'])
    return redirect(url_for('doctorLogin'))

@app.route("/doctorUpdate", methods =['GET', 'POST'])
def doctorUpdate():
    msg = ''
    if 'loggedIn' in session:
        if request.method == 'POST':
            docMailId = request.form['docMailId']
            docName=request.form['docName']
            passwd = request.form['passwd']
            availableDate = request.form['availableDate']
            cursor.execute(f'''SELECT * FROM doctor WHERE docMailId = '{docMailId}' ''')
            doctor = cursor.fetchone()
            if not doctor:
                msg = 'Account already exists !'
            else:
                cursor.execute(f'''UPDATE doctor SET  docMailId = '{docMailId}', passwd = '{passwd}', docName = '{docName}',availaibleDate= '{availableDate}' WHERE docMailId = '{session['mailId']}' ''')
                msg = 'You have successfully updated !'
        else:
            cursor.execute(f'''SELECT * FROM doctor WHERE docMailId = '{session['docMailId']}' ''')
            doctor = cursor.fetchone()
        return render_template("doctorUpdate.html", loggedIn = session['loggedIn'], doctor=doctor, msg = msg)
    return redirect(url_for('doctorLogin'))


@app.route("/nurseAlloc", methods=['GET','POST'])
def nurseAlloc():
    msg=''
    if 'loggedIn' in session:
        if request.method=='POST':
            mailId = request.form['mailId']
            nurseId = request.form['nurseId']
            dateIn = request.form['dateIn']
            dateOut = request.form['dateOut']
            cursor.execute(f'''INSERT INTO nursealloc VALUES('{session['mailId']}','{nurseId}','{mailId}','{dateIn}','{dateOut}') ''')
            msg="successfully allocated nurse"
        return render_template('nurseAlloc.html', loggedIn = session['loggedIn'], msg = msg)
    return render_template('doctorLogin.html')

@app.route("/records",methods=['GET','POST'])
def records():
    if 'loggedIn' in session:
        cursor.execute(f'''SELECT * FROM record WHERE mailId = '{session['mailId']}' ''')
        record = cursor.fetchall()
        return render_template("patientRecord.html", loggedIn=session['loggedIn'], record = record)
    return redirect(url_for('login'))

@app.route("/patientRecord",methods=['GET','POST'])
def patientRecord():
    if 'loggedIn' in session:
        cursor.execute(f'''SELECT * FROM record WHERE mailId = '{session['patMailId']}' ''')
        record=cursor.fetchall()
        return render_template("patientRecord.html", loggedIn=session['loggedIn'], record=record)
    return redirect(url_for('home'))

@app.route("/selectPatientforRecord",methods=['GET','POST'])
def selectPatientforRecord():
    msg=" "
    if 'loggedIn' in session:
        if request.method=="POST":
            session['patMailId']=request.form['mailId']
            return redirect(url_for('patientRecord'))
        else:
            return render_template("selectPatientforRecord.html", loggedIn=session['loggedIn'], msg=msg)
    return render_template('doctorIndex.html')

temp2=0
@app.route("/rec_appointment",methods=['GET','POST'])
def rec_appointment():
    if 'loggedIn' in session:
        cursor.execute('SELECT * FROM appointment WHERE docMailId = % s', (temp2,))
        appoint=cursor.fetchall()
        return render_template("rec_appointment.html", appoint=appoint)
    return redirect(url_for('home'))

@app.route("/pre_rec_appointment",methods=['GET','POST'])
def pre_rec_appointment():
    msg=" "
    if 'loggedIn' in session:
        if request.method=="POST" and 'docMailId' in request.form:
            docMailId=request.form['docMailId']
            temp2=docMailId
            return redirect(url_for('rec_appointment'))
        else:
            return render_template("pre_rec_appointment.html",msg=msg)
    return render_template('adminIndex.html')

@app.route("/doctorsList",methods=['GET','POST'])
def doctorsList():
    cursor.execute('SELECT docMailId, docName, availableDate FROM doctor')
    return render_template('doctorsList.html', doctors = cursor.fetchall(), loggedIn=session['loggedIn'] if 'loggedIn' in session else None)

if __name__ == "__main__":
    app.debug=True
    app.run(host ="localhost", port = 4000)
