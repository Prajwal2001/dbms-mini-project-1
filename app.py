from flask import Flask, render_template, request, redirect, url_for,session
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
            return redirect(url_for('display'))
        elif session['loggedIn']==2:
            return redirect(url_for('doctorIndex'))
        else:
            return redirect(url_for('patients'))
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'loggedIn' in session:
        return redirect(url_for('redirectPg'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
   session.pop('loggedIn', None)
   session.pop('mailId', None)
   return redirect(url_for('home'))

@app.route('/login',methods=['GET','POST'])
def login():
    msg=''
    if request.method=='POST':
        userType = request.form['userType']
        mailId = request.form['mailId']
        passwd = request.form['passwd']
        cursor.execute(f'''SELECT * FROM {userType} WHERE {'docMailId' if userType == 'doctor' else 'mailId'} = '{mailId}' AND passwd= '{passwd}' ''')
        user=cursor.fetchone()
        if user:
            session['loggedIn'] = 1 if userType=='patient' else (2 if userType == 'doctor' else 3)
            session['mailId'] = user[0]
            return redirect(url_for('home'))
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

@app.route('/makeappointment' , methods=['GET','POST'])
def makeappointment():
    msg=''
    if 'loggedIn' in session:
        if request.method=='POST':
            docMailId=request.form['docMailId']
            appointmentDate=request.form['appointmentDate']
            cursor.execute('SELECT * FROM appointment WHERE mailId = %s and appointmentDate = %s',(session['mailId'],appointmentDate))
            appointment=cursor.fetchone()
            if appointment:
                msg="You have already booked an Appointment"
            else:
                cursor.execute(f'''INSERT INTO appointment VALUES ('{session['mailId']}', '{appointmentDate}', '{docMailId}') ''')
                return redirect(url_for('patientAppointments'))
        cursor.execute('SELECT * FROM doctor')
        doctors = cursor.fetchall()
        return render_template('patient/makeappointment.html', doctors=doctors, loggedIn=session['loggedIn'], msg = msg)
    return redirect(url_for('login'))

@app.route('/adminLogin',methods=['GET','POST'])
def adminLogin():
    msg='Enter Login Credentials'
    if request.method=='POST' and 'mailId' in request.form and 'passwd' in request.form:
        mailId=request.form['mailId']
        passwd = request.form['passwd']
        cursor.execute(f'''SELECT * FROM admin WHERE mailId = '{mailId}' and passwd= '{passwd}' ''')
        admin=cursor.fetchone()
        if admin:
            session['loggedIn'] = 3
            session['mailId'] = admin[0]
            return redirect(url_for('patients'))
        else:
            msg = 'Incorrect username / password !'
    return render_template('admin/adminLogin.html', msg = msg)

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
            return redirect(url_for('patients'))
    else:
        msg = 'Please fill out the form !'
    return render_template('admin/adminRegister.html', msg = msg)

@app.route("/adminDisplay")
def adminDisplay():
    if 'loggedIn' in session:
        cursor.execute(f'''SELECT * FROM admin WHERE mailId = '{session['mailId']}' ''')
        admin = cursor.fetchone()
        return render_template("admin/adminDisplay.html", loggedIn = session['loggedIn'], admin = admin)
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
        return render_template("admin/adminUpdate.html", loggedIn = session['loggedIn'], admin=admin,  msg = msg)
    return redirect(url_for('adminLogin'))

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
            session['mailId'] = doctor[0]
            return redirect(url_for('doctorIndex'))
        msg = 'Incorrect mail-id or password !'
    return render_template('doctorLogin.html', msg = msg)

@app.route("/doctorIndex")
def doctorIndex():
    if 'loggedIn' in session:
        return render_template("doctorIndex.html", loggedIn = session['loggedIn'])
    return redirect(url_for('doctorLogin'))

@app.route("/doctorDisplay")
def doctorDisplay():
    if 'loggedIn' in session:
        cursor.execute(f'''SELECT * FROM doctor WHERE docMailId = '{session['mailId']}' ''')
        doctor = cursor.fetchone()
        return render_template("doctorDisplay.html", doctor = doctor, loggedIn = session['loggedIn'])
    return redirect(url_for('doctorLogin'))

@app.route("/myRecords",methods=['GET','POST'])
def myRecords():
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

@app.route("/docAppointments",methods=['GET','POST'])
def docAppointments():
    if 'loggedIn' in session:
        docMailId = True
        cursor.execute(f'''SELECT * FROM appointment WHERE docMailId = '{docMailId}' ''')
        appoint=cursor.fetchall()
        return render_template("docAppointments.html", appoint=appoint)
    return redirect(url_for('home'))

@app.route("/doctorsList",methods=['GET','POST'])
def doctorsList():
    cursor.execute('SELECT docMailId, docName, availableDate FROM doctor')
    return render_template('doctorsList.html', doctors = cursor.fetchall(), loggedIn=session['loggedIn'] if 'loggedIn' in session else None)

@app.route("/doctorUpdate", methods =['GET', 'POST'])
def doctorUpdate():
    msg = ''
    if 'loggedIn' not in session or session['loggedIn']<2:
        return redirect(url_for('home'))
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
        cursor.execute(f'''SELECT * FROM doctor WHERE docMailId = '{session['mailId']}' ''')
        doctor = cursor.fetchone()
    return render_template("admin/doctorUpdate.html", loggedIn = session['loggedIn'], doctor=doctor, msg = msg)

@app.route("/patients", methods=['GET', 'POST'])
def patients():
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    cursor.execute(f'''SELECT * FROM patient ''')
    patients=cursor.fetchall()
    return render_template("admin/patients.html", loggedIn=session['loggedIn'], patients=patients)

@app.route("/patientAdd", methods=['GET', 'POST'])
def patientAdd():
    #if 'loggedIn' not in session or session['loggedIn']!=3:
    #    return redirect(url_for('home'))
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
            return redirect(url_for('home'))
    return render_template("admin/patientAdd.html", msg=msg, loggedIn=session['loggedIn'] if 'loggedIn' in session else None)

@app.route("/patientUpdate/<patMailId>", methods=['GET', 'POST'])
def patientUpdate(patMailId):
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    msg = ''
    if request.method == 'POST':
            mailId = request.form['mailId']
            passwd = request.form['passwd']
            PName = request.form['PName']
            dob = request.form['dob']
            bloodGroup = request.form['bloodGroup']
            sex = request.form['sex']
            cursor.execute(f'''SELECT * FROM patient WHERE mailId = '{mailId}' ''')
            patient = cursor.fetchone()
            if patient and patient[0]!=patMailId:
                msg = 'Mail-Id already in use!'
            else:
                cursor.execute(f'''UPDATE patient SET  mailId = '{mailId}', passwd = '{passwd}', PName = '{PName}', dob = '{dob}', bloodGroup = '{bloodGroup}', sex = '{sex}'  WHERE mailId = '{patMailId}' ''')
            return redirect(url_for('patients'))
    else:
        cursor.execute(f"SELECT * FROM patient WHERE mailId = '{patMailId}'")
        patient = cursor.fetchone()
        return render_template("admin/patientUpdate.html", patient=patient, loggedIn = session['loggedIn'], msg=msg)

@app.route("/patientDelete/<patMailId>")
def patientDelete(patMailId):
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    cursor.execute(f'''DELETE FROM patient WHERE mailId = '{patMailId}' ''')
    return redirect(url_for('patients'))

#Admin Doctor Methods
@app.route("/doctors", methods=['GET', 'POST'])
def doctors():
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    cursor.execute(f'''SELECT * FROM doctor ''')
    doctors=cursor.fetchall()
    return render_template("admin/doctors.html", loggedIn=session['loggedIn'], doctors=doctors)

@app.route("/doctorAdd", methods=['GET', 'POST'])
def doctorAdd():
    msg = ''
    #if 'loggedIn' not in session or session['loggedIn']!=3:
    #    return redirect(url_for('home'))
    if request.method == 'POST':
        docMailId = request.form['docMailId']
        passwd = request.form['passwd']
        docName = request.form['docName']
        sex = request.form['sex']
        cursor.execute(f'''SELECT * FROM doctor WHERE docMailId = '{docMailId}' ''')
        doctor = cursor.fetchone()
        if doctor:
            msg = 'Account already exists !'
        else:
            cursor.execute(f'''INSERT INTO doctor(docMailId, passwd, docName, sex) VALUES ('{docMailId}', '{passwd}', '{docName}', '{sex}') ''')
            return redirect(url_for('home'))
    return render_template("admin/doctorAdd.html", msg=msg, loggedIn=session['loggedIn'] if 'loggedIn' in session else None)

@app.route("/doctorUpdate/<mailId>", methods=['GET', 'POST'])
def admindoctorUpdate(mailId):
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    msg = ''
    if request.method == 'POST':
            docMailId = request.form['docMailId']
            passwd = request.form['passwd']
            docName = request.form['docName']
            sex = request.form['sex']
            cursor.execute(f'''SELECT * FROM doctor WHERE docMailId = '{mailId}' ''')
            doctor = cursor.fetchone()
            if doctor and doctor[0]!=mailId:
                msg = 'Mail-Id already in use!'
            else:
                cursor.execute(f'''UPDATE doctor SET  docMailId = '{docMailId}', passwd = '{passwd}', docName = '{docName}', sex = '{sex}' WHERE docMailId = '{mailId}' ''')
            return redirect(url_for('doctors'))
    else:
        cursor.execute(f"SELECT * FROM doctor WHERE docMailId = '{mailId}'")
        doctor = cursor.fetchone()
        return render_template("admin/doctorUpdate.html", doctor=doctor, loggedIn = session['loggedIn'], msg=msg)

@app.route("/doctorDelete/<mailId>")
def doctorDelete(mailId):
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    cursor.execute(f'''DELETE FROM doctor WHERE docMailId = '{mailId}' ''')
    return redirect(url_for('doctors'))

#Admin Nurse Methods
@app.route("/nurses", methods=['GET', 'POST'])
def nurses():
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    cursor.execute(f'''SELECT * FROM nurse ''')
    nurses=cursor.fetchall()
    return render_template("admin/nurses.html", loggedIn=session['loggedIn'], nurses=nurses)

@app.route('/nurseAdd', methods=['GET','POST'])
def nurseAdd():
    msg=''
    if 'loggedIn' in session and session['loggedIn']==3:
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
                return redirect(url_for('nurses'))
        return render_template('admin/nurseAdd.html', loggedIn=session['loggedIn'], msg = msg)
    return redirect(url_for('home'))


@app.route("/nurseUpdate/<mailId>", methods=['GET', 'POST'])
def nurseUpdate(mailId):
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    msg = ''
    if request.method == 'POST':
            nurseId = request.form['nurseId']
            phoneNumber = request.form['phoneNumber']
            nurseName = request.form['nurseName']
            cursor.execute(f'''SELECT * FROM nurse WHERE nurseId = '{mailId}' ''')
            nurse = cursor.fetchone()
            if nurse and nurse[0]!=mailId:
                msg = 'Mail-Id already in use!'
            else:
                cursor.execute(f'''UPDATE nurse SET nurseId = '{nurseId}', phoneNumber = '{phoneNumber}', nurseName = '{nurseName}' WHERE nurseId = '{mailId}' ''')
            return redirect(url_for('nurses'))
    else:
        cursor.execute(f"SELECT * FROM nurse WHERE nurseId = '{mailId}'")
        nurse = cursor.fetchone()
        return render_template("admin/nurseUpdate.html", nurse=nurse, loggedIn = session['loggedIn'], msg=msg)

@app.route("/nurseDelete/<mailId>")
def nurseDelete(mailId):
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    cursor.execute(f'''DELETE FROM nurse WHERE nurseId = '{mailId}' ''')
    return redirect(url_for('nurses'))

#Nurse Allocation Methods
@app.route("/nurseAlloc", methods=['GET', 'POST'])
def nurseAlloc():
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    cursor.execute(f'''SELECT * FROM nursealloc ''')
    allocations=cursor.fetchall()
    return render_template("admin/nurseAlloc.html", loggedIn=session['loggedIn'], allocations=allocations)

@app.route("/nurseAllocAdd", methods=['GET','POST'])
def nurseAllocAdd():
    msg=''
    if 'loggedIn' in session:
        if request.method=='POST':
            mailId = request.form['mailId']
            nurseId = request.form['nurseId']
            dateIn = request.form['dateIn']
            dateOut = request.form['dateOut']
            cursor.execute(f'''SELECT * FROM nursealloc WHERE mailId = '{mailId}' OR AND dateIn BETWEEN '{dateIn}' AND '{dateOut}' ''')
            allocation = cursor.fetchone()
            if allocation:
                msg = 'Nurse already allocated!'
            else:
                try:
                    cursor.execute(f'''INSERT INTO nursealloc VALUES('{nurseId}','{mailId}','{dateIn}','{dateOut}') ''')
                    msg="successfully allocated nurse"
                except:
                    msg='invalid entry'
        cursor.execute(f'''SELECT nurseId, nurseName FROM nurse ''')
        nurses = cursor.fetchall()
        cursor.execute(f'''SELECT mailId, Pname FROM patient ''')
        patients = cursor.fetchall()
        return render_template('admin/nurseAllocAdd.html', patients = patients, nurses = nurses, loggedIn = session['loggedIn'], msg = msg)
    return redirect(url_for('home'))

# @app.route("/nurseAllocUpdate/<args>", methods=['GET', 'POST'])
# def nurseAllocUpdate(args):
#     if 'loggedIn' not in session or session['loggedIn']!=3:
#         return redirect(url_for('home'))
#     msg = ''
#     args = args.split()
#     if request.method == 'POST':
#             mailId = request.form['mailId']
#             nurseId = request.form['nurseId']
#             dateIn = request.form['dateIn']
#             dateOut = request.form['dateOut']
#             cursor.execute(f'''SELECT * FROM nursealloc WHERE mailId = '{mailId}' AND dateIn BETWEEN '{dateIn}' AND '{dateOut}' ''')
#             allocation = cursor.fetchone()
#             if allocation:
#                 msg = 'Nurse already allocated!'
#             else:
#                 cursor.execute(f'''UPDATE nursealloc SET mailId = '{mailId}', nurseId = '{nurseId}', dateIn = '{dateIn}', dateOut = '{dateOut}' WHERE mailId = '{args[0]}' AND dateIn = '{args[1]}' ''')
#             return redirect(url_for('nurseAlloc'))
#     else:
#         cursor.execute(f"SELECT * FROM nursealloc WHERE mailId = '{args[0]}' AND dateIn = '{args[1]}' ")
#         allocations = cursor.fetchone()
#         return render_template("admin/nurseAllocUpdate.html", allocations=allocations, loggedIn = session['loggedIn'], msg=msg)

@app.route("/nurseAllocDelete/<args>")
def nurseAllocDelete(args):
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    args = args.split()
    cursor.execute(f'''DELETE FROM nursealloc WHERE mailId = '{args[0]}' AND dateIn = '{args[1]}' ''')
    return redirect(url_for('nurseAlloc'))

#Admin Appointments Methods
@app.route("/appointments", methods=['GET', 'POST'])
def appointments():
    if 'loggedIn' not in session:
        return redirect(url_for('home'))
    if session['loggedIn']==1:
        cursor.execute(f'''SELECT * FROM appointment WHERE mailId = '{session['mailId']}' ''')
    else:
        cursor.execute(f'''SELECT * FROM appointment ''')
    appointments=cursor.fetchall()
    return render_template("admin/appointments.html", loggedIn=session['loggedIn'], appointments=appointments)

@app.route("/appointmentAdd", methods=['GET', 'POST'])
def appointmentAdd():
    msg=''
    if 'loggedIn' in session and session['loggedIn']==3:
        if request.method=='POST':
            mailId=request.form['mailId']
            appointmentDate=request.form['appointmentDate']
            docMailId=request.form['docMailId']
            cursor.execute(f'''SELECT * FROM appointment WHERE mailId = '{mailId}' AND appointmentDate = '{appointmentDate}' AND docMailId = '{docMailId}' ''')
            appointment=cursor.fetchone()
            if appointment:
                msg="Appointment already exists"
            else:
                cursor.execute('INSERT INTO appointment VALUES(%s,%s,%s)',(mailId, appointmentDate, docMailId))
                return redirect(url_for('appointments'))
        cursor.execute(f'''SELECT docMailId, docName FROM doctor ''')
        doctors = cursor.fetchall()
        cursor.execute(f'''SELECT mailId, Pname FROM patient ''')
        patients = cursor.fetchall()
        return render_template('admin/appointmentAdd.html', doctors = doctors, patients=patients, loggedIn=session['loggedIn'], msg = msg)
    return redirect(url_for('home'))


@app.route("/appointmentUpdate/<args>", methods=['GET', 'POST'])
def appointmentUpdate(args):
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    msg = ''
    appoint = args.split()
    if request.method == 'POST':
            mailId = request.form['mailId']
            appointmentDate = request.form['appointmentDate']
            docMailId = request.form['docMailId']
            cursor.execute(f'''SELECT * FROM appointment WHERE mailId = '{mailId}' AND appointmentDate = '{appointmentDate}' AND docMailId = '{docMailId}' ''')
            appointment = cursor.fetchone()
            if appointment:
                msg = 'Appointment already exists!'
            else:
                cursor.execute(f'''UPDATE appointment SET mailId = '{mailId}', appointmentDate = '{appointmentDate}', docMailId = '{docMailId}' WHERE mailId = '{appoint[0]}' AND appointmentDate = '{appoint[1]}' AND docMailId = '{appoint[2]}' ''')
            return redirect(url_for('appointments'))
    else:
        cursor.execute(f"SELECT * FROM appointment WHERE mailId = '{appoint[0]}' AND appointmentDate = '{appoint[1]}' AND docMailId = '{appoint[2]}' ")
        appointment = cursor.fetchone()
        return render_template("admin/appointmentUpdate.html", appointment=appointment, loggedIn = session['loggedIn'], msg=msg)

@app.route("/appointmentDelete/<args>")
def appointmentDelete(args):
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    args = args.split()
    cursor.execute(f'''DELETE FROM appointment WHERE mailId = '{args[0]}' AND appointmentDate = '{args[1]}' AND docMailId = '{args[2]}' ''')
    return redirect(url_for('appointments'))

#Admin Records Methods
@app.route("/records", methods=['GET', 'POST'])
def records():
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    cursor.execute(f'''SELECT * FROM record ''')
    records=cursor.fetchall()
    return render_template("admin/records.html", loggedIn=session['loggedIn'], records=records)

@app.route("/recordAdd", methods=['GET', 'POST'])
def recordAdd():
    if 'loggedIn' in session and session['loggedIn']==3:
        if request.method=='POST':
            mailId=request.form['mailId']
            Analysis=request.form['Analysis']
            cursor.execute(f'''INSERT INTO record(mailId, Analysis) VALUES('{mailId}','{Analysis}')''')
            return redirect(url_for('records'))
        cursor.execute(f'''SELECT mailId, Pname FROM patient ''')
        patients = cursor.fetchall()
        return render_template('admin/recordAdd.html', patients=patients, loggedIn=session['loggedIn'])
    return redirect(url_for('home'))


@app.route("/recordUpdate/<recordId>", methods=['GET', 'POST'])
def recordUpdate(recordId):
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    msg = ''
    if request.method == 'POST':
            mailId = request.form['mailId']
            Analysis = request.form['Analysis']
            cursor.execute(f'''SELECT * FROM record WHERE recordId = '{recordId}' ''')
            record = cursor.fetchone()
            if record and record[1]!=recordId:
                msg = 'Record-Id already in use!'
            else:
                cursor.execute(f'''UPDATE record SET mailId = '{mailId}', Analysis = '{Analysis}' WHERE recordId = '{recordId}' ''')
            return redirect(url_for('records'))
    else:
        cursor.execute(f"SELECT * FROM record WHERE recordId = '{recordId}'")
        record = cursor.fetchone()
        cursor.execute(f'''SELECT mailId, Pname FROM patient WHERE mailId <> (SELECT mailId FROM record WHERE recordId='{recordId}') ''')
        patients = cursor.fetchall()
        return render_template("admin/recordUpdate.html", patients=patients, record=record, loggedIn = session['loggedIn'], msg=msg)

@app.route("/recordDelete/<recordId>")
def recordDelete(recordId):
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    cursor.execute(f'''DELETE FROM record WHERE recordId = '{recordId}' ''')
    return redirect(url_for('records'))

#Admin Test Methods
@app.route("/tests", methods=['GET', 'POST'])
def tests():
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    cursor.execute(f'''SELECT * FROM test ''')
    tests=cursor.fetchall()
    return render_template("admin/tests.html", loggedIn=session['loggedIn'], tests=tests)

@app.route("/testAdd", methods=['GET', 'POST'])
def testAdd():
    if 'loggedIn' in session and session['loggedIn']==3:
        if request.method=='POST':
            testName=request.form['testName']
            testCategory=request.form['testCategory']
            cursor.execute(f'''INSERT INTO test(testName, testCategory) VALUES('{testName}', '{testCategory}')''')
            return redirect(url_for('tests'))
        return render_template('admin/testAdd.html', loggedIn=session['loggedIn'])
    return redirect(url_for('home'))

@app.route("/testUpdate/<testId>", methods=['GET', 'POST'])
def testUpdate(testId):
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    msg = ''
    if request.method == 'POST':
            testName=request.form['testName']
            testCategory=request.form['testCategory']
            cursor.execute(f'''SELECT * FROM record WHERE testId = {testId} ''')
            test = cursor.fetchone()
            if test and test[1]!=testId:
                msg = 'Test-Id already in use!'
            else:
                cursor.execute(f'''UPDATE test SET testName = '{testName}', testCategory = '{testCategory}' WHERE testId = {testId} ''')
            return redirect(url_for('tests'))
    else:
        cursor.execute(f"SELECT * FROM test WHERE testId = {testId}")
        test = cursor.fetchone()
        return render_template("admin/testUpdate.html", test=test, loggedIn = session['loggedIn'], msg=msg)

@app.route("/testDelete/<testId>")
def testDelete(testId):
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    cursor.execute(f'''DELETE FROM test WHERE testId = {testId} ''')
    return redirect(url_for('tests'))

#Admin Diagnosis Methods
@app.route("/diagnosis", methods=['GET', 'POST'])
def diagnosis():
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    cursor.execute(f'''SELECT * FROM diagnosis ''')
    diagnosis=cursor.fetchall()
    return render_template("admin/diagnosis.html", loggedIn=session['loggedIn'], diagnosis=diagnosis)

@app.route("/diagnosisAdd", methods=['GET', 'POST'])
def diagnosisAdd():
    msg=''
    if 'loggedIn' in session and session['loggedIn']==3:
        if request.method=='POST':
            mailId=request.form['mailId']
            testId=request.form['testId']
            testDate=request.form['testDate']
            analysis=request.form['analysis']
            cursor.execute(f'''SELECT * FROM diagnosis WHERE mailId = '{mailId}' AND testId = '{testId}' AND testDate = '{testDate}' ''')
            appointment=cursor.fetchone()
            if appointment:
                msg="Diagnosis already exists"
            else:
                cursor.execute('INSERT INTO diagnosis VALUES(%s, %s, %s, %s)',(mailId, testId, testDate, analysis))
                return redirect(url_for('diagnosis'))
        cursor.execute(f'''SELECT testId, testName FROM test ''')
        tests = cursor.fetchall()
        cursor.execute(f'''SELECT mailId, Pname FROM patient ''')
        patients = cursor.fetchall()
        return render_template('admin/diagnosisAdd.html', tests=tests, patients=patients, loggedIn=session['loggedIn'], msg = msg)
    return redirect(url_for('home'))

@app.route("/diagnosisUpdate/<args>", methods=['GET', 'POST'])
def diagnosisUpdate(args):
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    msg = ''
    test = args.split()
    if request.method == 'POST':
            mailId=request.form['mailId']
            testId=request.form['testId']
            testDate=request.form['testDate']
            analysis=request.form['analysis']
            cursor.execute(f'''SELECT * FROM diagnosis WHERE mailId = '{mailId}' AND testId = '{testId}' AND testDate = '{testDate}' ''')
            diagnosis = cursor.fetchone()
            if diagnosis:
                msg = 'Appointment already exists!'
            else:
                cursor.execute(f'''UPDATE diagnosis SET mailId = '{mailId}', testId = '{testId}', testDate = '{testDate}', analysis = '{analysis}' WHERE mailId = '{test[0]}' AND testId = '{test[1]}' AND testDate = '{test[2]}' ''')
            return redirect(url_for('diagnosis'))
    else:
        cursor.execute(f"SELECT * FROM diagnosis WHERE mailId = '{test[0]}' AND testId = '{test[1]}' AND testDate = '{test[2]}' ")
        diagnosis = cursor.fetchone()
        return render_template("admin/diagnosisUpdate.html", diagnosis=diagnosis, loggedIn = session['loggedIn'], msg=msg)

@app.route("/diagnosisDelete/<args>")
def diagnosisDelete(args):
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    args = args.split()
    cursor.execute(f'''DELETE FROM diagnosis WHERE mailId = '{args[0]}' AND testId = '{args[1]}' AND testDate = '{args[2]}' ''')
    return redirect(url_for('diagnosis'))

#Admin Medicines Methods
@app.route("/medicines", methods=['GET', 'POST'])
def medicines():
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    cursor.execute(f'''SELECT * FROM medicine ''')
    medicines=cursor.fetchall()
    return render_template("admin/medicines.html", loggedIn=session['loggedIn'], medicines=medicines)

@app.route("/medicineAdd", methods=['POST'])
def medicineAdd():
    if 'loggedIn' in session and session['loggedIn']==3:
        if request.method=='POST':
            medicineName=request.form['medicineName']
            cursor.execute(f'''INSERT INTO medicine(medicineName) VALUES('{medicineName}')''')
        return redirect(url_for('medicines'))
    return redirect(url_for('home'))

@app.route("/medicineDelete/<medicineId>")
def medicineDelete(medicineId):
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    cursor.execute(f'''DELETE FROM medicine WHERE medicineId = '{medicineId}' ''')
    return redirect(url_for('medicines'))

#Admin Dosages Methods
@app.route("/dosages", methods=['GET', 'POST'])
def dosages():
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    cursor.execute(f'''SELECT * FROM dosage ''')
    dosages=cursor.fetchall()
    return render_template("admin/dosages.html", loggedIn=session['loggedIn'], dosages=dosages)

@app.route("/dosageAdd",methods=["GET","POST"])
def dosageAdd():
    msg=''
    if 'loggedIn' in session and session['loggedIn']==3:
        if request.method=='POST':
            mailId=request.form['mailId']
            medicineId=request.form['medicineId']
            quantity=request.form['quantity']
            doseDate=request.form['doseDate']
            cursor.execute(f'''SELECT * FROM dosage WHERE mailId = '{mailId}' AND medicineId = '{medicineId}' AND quantity = '{quantity}' AND doseDate = '{doseDate}' ''')
            dosage=cursor.fetchone()
            if dosage:
                msg="Entry already exists"
            else:
                cursor.execute('INSERT INTO dosage VALUES(%s,%s,%s,%s)',(mailId, medicineId, quantity, doseDate))
                return redirect(url_for('dosages'))
        cursor.execute(f'''SELECT medicineId, medicineName FROM medicine ORDER BY medicineName ''')
        medicines = cursor.fetchall()
        cursor.execute(f'''SELECT mailId, Pname FROM patient ''')
        patients = cursor.fetchall()
        return render_template('admin/dosageAdd.html', patients=patients, medicines=medicines, loggedIn=session['loggedIn'], msg = msg)
    return redirect(url_for('home'))

@app.route("/dosageUpdate/<args>", methods=['GET', 'POST'])
def dosageUpdate(args):
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    msg = ''
    dose = args.split()
    if request.method == 'POST':
            mailId=request.form['mailId']
            medicineId=request.form['medicineId']
            quantity=request.form['quantity']
            doseDate=request.form['doseDate']
            cursor.execute(f'''SELECT * FROM dosage WHERE mailId = '{mailId}' AND medicineId = '{medicineId}' AND doseDate = '{doseDate}' ''')
            dosage = cursor.fetchone()
            if dosage:
                msg = 'Appointment already exists!'
            else:
                cursor.execute(f'''UPDATE appointment SET mailId = '{mailId}', medicineId = '{medicineId}', quantity = '{quantity}', doseDate = '{doseDate}' WHERE mailId = '{dose[0]}' AND  medicineId = '{dose[1]}' AND doseDate = '{dose[2]}' ''')
            return redirect(url_for('dosages'))
    else:
        cursor.execute(f"SELECT * FROM appointment WHERE mailId = '{dose[0]}' AND  medicineId = '{dose[1]}' AND doseDate = '{dose[2]}' ")
        dosage = cursor.fetchone()
        return render_template("admin/appointmentUpdate.html", dosage=dosage, loggedIn = session['loggedIn'], msg=msg)

@app.route("/dosageDelete/<args>")
def dosageDelete(args):
    if 'loggedIn' not in session or session['loggedIn']!=3:
        return redirect(url_for('home'))
    args = args.split()
    cursor.execute(f'''DELETE FROM dosage WHERE mailId = '{args[0]}' AND medicineId = '{args[1]}' AND doseDate = '{args[2]}' ''')
    return redirect(url_for('dosages'))

if __name__ == "__main__":
    app.debug=True
    app.run(host ="localhost", port = 4000)
