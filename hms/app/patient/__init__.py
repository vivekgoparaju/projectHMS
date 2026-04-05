from flask import Blueprint, render_template, session, request, redirect, url_for
from .auth import patient_auth
from app.db import get_db

patient=Blueprint("patient", __name__, template_folder="templates", static_folder='static')

patient.register_blueprint(patient_auth, url_prefix='/auth')

@patient.before_request
def check_user_login():
    if not (request.endpoint and (request.endpoint.startswith("patient.auth.") or request.endpoint == 'static')):
        if "isLoggedIn" in session and session['isLoggedIn']:
            pass
        else:
            return redirect(url_for('patient.auth.signin'))

@patient.route('/profile')
def profile():
    if 'userData' not in session: return redirect(url_for('patient.auth.signin'))
    user_id = session['userData']['id']
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id=?', (user_id,)).fetchone()
    return render_template("profile.html", user=dict(user))

@patient.route('/update_profile', methods=['POST'])
def update_profile():
    if 'userData' not in session: return redirect(url_for('patient.auth.signin'))
    user_id = session['userData']['id']
    phone = request.form.get('phone')
    location = request.form.get('location')
    email = request.form.get('email')
    
    db = get_db()
    db.execute('UPDATE users SET phone=?, location=?, email=? WHERE id=?', (phone, location, email, user_id))
    db.commit()
    return redirect(url_for('patient.profile'))

@patient.route('/doctors')
def doctors():
    db = get_db()
    doctors = db.execute('SELECT * FROM doctors').fetchall()
    specializations = [r['specialization'] for r in db.execute('SELECT DISTINCT specialization FROM doctors').fetchall() if r['specialization']]
    return render_template("doctors.html", specializations=specializations, doctors=[dict(d) for d in doctors])

@patient.route('/doctor_details')
def doctor_details():
    id=request.args.get('id')
    db = get_db()
    doctor = db.execute('SELECT * FROM doctors WHERE id=?', (id,)).fetchone()
    return render_template("doctor_details.html", doctor_details=dict(doctor) if doctor else None)

@patient.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    id = request.args.get('id')
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        date = request.form.get('date')
        time = request.form.get('time')
        user_id = session['userData']['id']
        db = get_db()
        db.execute('INSERT INTO appointments(patient_id, doctor_id, date, time, status) VALUES (?,?,?,?,?)',
                   (user_id, doctor_id, date, time, 'pending'))
        db.commit()
        return redirect(url_for('patient.appointments'))
    
    db = get_db()
    doctors = db.execute('SELECT * FROM doctors').fetchall()
    user_id = session['userData']['id']
    user = db.execute('SELECT * FROM users WHERE id=?', (user_id,)).fetchone()
    return render_template("appointment.html", doctors=[dict(d) for d in doctors], selected_doctor_id=id, user=dict(user))

@patient.route('/appointments')
def appointments():
    user_id = session['userData']['id']
    db = get_db()
    appointments = db.execute('''
        SELECT a.*, d.name as doctor_name, d.specialization 
        FROM appointments a 
        JOIN doctors d ON a.doctor_id = d.id 
        WHERE a.patient_id = ?
    ''', (user_id,)).fetchall()
    return render_template("appointments.html", appointments=[dict(a) for a in appointments])

@patient.route('/logout')
def logout_patient():
    session.pop('isLoggedIn', None)
    session.pop('userData', None)
    return redirect(url_for("patient.auth.signin"))
