from flask import Blueprint, render_template, request, session, url_for, redirect
from app.db import get_db

doctor_bp = Blueprint('doctor', __name__, template_folder='templates', static_folder='static', url_prefix='/doctor')

@doctor_bp.before_request
def check_login():
    if not (request.endpoint and (request.endpoint == 'doctor.login' or request.endpoint == 'static')):
        if not session.get('doctor_id'):
            return redirect(url_for('doctor.login'))

@doctor_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        db = get_db()
        doctor = db.execute('SELECT * FROM doctors WHERE email=? AND password=?', (email, password)).fetchone()
        if doctor:
            session['doctor_id'] = doctor['id']
            session['doctor_name'] = doctor['name']
            return redirect(url_for('doctor.dashboard'))
        return render_template('doctor_login.html', error="Invalid credentials")
    return render_template('doctor_login.html')

@doctor_bp.route('/logout')
def logout():
    session.pop('doctor_id', None)
    session.pop('doctor_name', None)
    return redirect(url_for('doctor.login'))

@doctor_bp.route('/')
def dashboard():
    doctor_id = session['doctor_id']
    db = get_db()
    appointments = db.execute('''
        SELECT a.*, u.username as patient_name 
        FROM appointments a 
        JOIN users u ON a.patient_id = u.id 
        WHERE a.doctor_id = ?
        ORDER BY a.date, a.time
    ''', (doctor_id,)).fetchall()
    return render_template("doctor_dashboard.html", appointments=[dict(a) for a in appointments])

@doctor_bp.route('/patients')
def patients():
    doctor_id = session['doctor_id']
    db = get_db()
    # Patients who have had an appointment with this doctor
    patients = db.execute('''
        SELECT DISTINCT u.id, u.username, u.email, u.phone 
        FROM users u 
        JOIN appointments a ON u.id = a.patient_id 
        WHERE a.doctor_id = ?
    ''', (doctor_id,)).fetchall()
    return render_template("doctor_patients.html", patients=[dict(p) for p in patients])

@doctor_bp.route('/history/<int:patient_id>', methods=['GET', 'POST'])
def history(patient_id):
    doctor_id = session['doctor_id']
    db = get_db()
    if request.method == 'POST':
        date = request.form.get('date')
        diagnosis = request.form.get('diagnosis')
        prescription = request.form.get('prescription')
        db.execute('INSERT INTO medical_history(patient_id, doctor_id, date, diagnosis, prescription) VALUES (?,?,?,?,?)',
                   (patient_id, doctor_id, date, diagnosis, prescription))
        db.commit()
        return redirect(url_for('doctor.history', patient_id=patient_id))
    
    patient = db.execute('SELECT * FROM users WHERE id=?', (patient_id,)).fetchone()
    history = db.execute('SELECT * FROM medical_history WHERE patient_id=?', (patient_id,)).fetchall()
    return render_template("doctor_history.html", patient=dict(patient) if patient else None, history=[dict(h) for h in history])

@doctor_bp.route('/appointment/<int:id>/status', methods=['POST'])
def update_status(id):
    status = request.form.get('status')
    db = get_db()
    db.execute('UPDATE appointments SET status=? WHERE id=?', (status, id))
    db.commit()
    return redirect(url_for('doctor.dashboard'))
