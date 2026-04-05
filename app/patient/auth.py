from flask import Blueprint, render_template, request, session, url_for, redirect
from .auth_db_logic import check_for_signin, user_data, create_user

patient_auth=Blueprint('auth', __name__, template_folder='./templates')

# url ./patient/auth/.....
@patient_auth.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method=="POST":
        email=request.form.get('email')
        password=request.form.get('password')
        res=check_for_signin(email, password)
        if res['user_exists']:
            session['isLoggedIn']=True
            session['userData']=res['user']
            return redirect(url_for('patient.profile'))
        else:
            return render_template('./auth/signin.html', error=res.get('message'))
    else:
        return render_template('./auth/signin.html')


@patient_auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=="POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        res=create_user(username, email, password)
        if res['user_created']:
            return redirect(url_for('patient.auth.signin'))
        else:
            return render_template('./auth/signup.html', error=res.get('message'))
    return render_template('./auth/signup.html')