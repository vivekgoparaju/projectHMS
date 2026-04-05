from app.db import get_db

def check_user_exists(username, email):
    db = get_db()
    res = db.execute('SELECT 1 FROM users WHERE username=? OR email=?', (username, email)).fetchone()
    return 1 if res else 0

def create_user(username, email, password):
    if check_user_exists(username, email):
        return {'user_created':False, 'status':0, 'message':'user or email already exists'}
    else:
        db = get_db()
        db.execute('INSERT INTO users(username, password, email) VALUES(?, ?, ?)', (username, password, email))
        db.commit()
        return {'user_created':True, 'status':1}

def check_for_signin(email, password):
    db = get_db()
    user = db.execute('SELECT id, username FROM users WHERE email=? AND password=?', (email, password)).fetchone()
    if user:
        return {'user_exists':True, 'status':1, 'user': dict(user)}
    else:
        return {'user_exists':False, 'status':0, 'message':'invalid credentials'}

def user_data(email, password):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE email=? AND password=?', (email, password)).fetchone()
    return dict(user) if user else {}