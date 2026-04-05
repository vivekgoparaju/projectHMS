from flask import Blueprint, render_template, request, session, url_for, redirect
from app.db import get_db

admin_bp = Blueprint('admin', __name__, template_folder='templates', static_folder='static', url_prefix='/admin')

@admin_bp.before_request
def check_login():
    if not (request.endpoint and (request.endpoint == 'admin.login' or request.endpoint == 'static')):
        if not session.get('admin_id'):
            return redirect(url_for('admin.login'))

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        admin = db.execute('SELECT * FROM admin WHERE username=? AND password=?', (username, password)).fetchone()
        if admin:
            session['admin_id'] = admin['id']
            session['admin_username'] = admin['username']
            return redirect(url_for('admin.dashboard'))
        return render_template('admin_login.html', error="Invalid credentials")
    return render_template('admin_login.html')

@admin_bp.route('/logout')
def logout():
    session.pop('admin_id', None)
    session.pop('admin_username', None)
    return redirect(url_for('admin.login'))

@admin_bp.route('/')
def dashboard():
    db = get_db()
    doctors = db.execute('SELECT * FROM doctors').fetchall()
    stats = {
        'users': db.execute('SELECT COUNT(*) FROM users').fetchone()[0],
        'doctors': len(doctors),
        'appointments': db.execute('SELECT COUNT(*) FROM appointments').fetchone()[0]
    }
    return render_template("admin_dashboard.html", doctors=[dict(d) for d in doctors], stats=stats)

@admin_bp.route('/doctor/add', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        specialization = request.form.get('specialization')
        phone = request.form.get('phone')
        db = get_db()
        db.execute('INSERT INTO doctors(name, email, password, specialization, phone) VALUES (?,?,?,?,?)',
                   (name, email, password, specialization, phone))
        db.commit()
        return redirect(url_for('admin.dashboard'))
    return render_template("admin_add_doctor.html")

@admin_bp.route('/doctor/delete/<int:id>', methods=['POST'])
def delete_doctor(id):
    db = get_db()
    db.execute('DELETE FROM doctors WHERE id=?', (id,))
    db.commit()
    return redirect(url_for('admin.dashboard'))
