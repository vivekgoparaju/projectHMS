from flask import Blueprint, render_template, request, jsonify, session, url_for, redirect
from .auth_db_logic import check_for_signin, user_data

patient_auth=Blueprint('auth', __name__, template_folder='./templates')

# url ./patient/auth/.....
@patient_auth.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method=="POST":
        # core logic
        email=request.form['email']
        password=request.form['password']
        res=check_for_signin(email, password)
        if res['user_exists']:
            session['isLoggedIn']=True
            session['userData']=user_data(email, password)
            return redirect(url_for('patient.profile'))
    else:
        return render_template('./auth/signin.html')


@patient_auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=="POST":
        # core logic

        session['isLoggedIn']=True
    return render_template('./auth/signup.html')