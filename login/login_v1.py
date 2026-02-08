from flask import Flask, render_template, request, redirect, session
from db import check_user_exist,create_user
from flask_session import Session

app=Flask(__name__, template_folder='templates')
app.config['SESSION_PERMANENT']=False
app.config['SESSION_TYPE']='filesystem'
app.secret_key='askdjbh<[98sd7asd867765a$;234bq2'
Session(app)

@app.before_request
def sessions():
    if 'isLoggedIn' not in session:
        session['isLoggedIn']=False
    print(session['isLoggedIn'])

@app.route('/home')
@app.route('/')
def home():
    print(session['isLoggedIn'])
    if session['isLoggedIn']:
        return render_template('home.html')
    else:
        return redirect("login")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        username=request.form['username']
        passowrd=request.form['password']
        if check_user_exist(username=username, password=passowrd)==True:
            session['isLoggedIn']=True
            return redirect("home")
        else:
            return {"status":False}
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session['isLoggedIn']=False
    return redirect('login')
@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method=='POST':
        username=request.form['username']
        passowrd=request.form['password']
        email=request.form['email']
        phone=request.form['phone']
        if create_user(username=username, password=passowrd, email=email, phone=phone):
            session['isLoggedIn']=True            
            return redirect("home")
    else:
        return render_template("signin.html")

@app.route('/t')
def t():
    return render_template('t.html')

if __name__=='__main__':
    app.run(debug=True)