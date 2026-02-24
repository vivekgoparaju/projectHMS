import sqlite3

con=sqlite3.connect('database.db', check_same_thread=False)
cur=con.cursor()

def username_exists(username):
    q_check_username=f'''select id,username from users where username="{username}"'''
    res=cur.execute(q_check_username).fetchall()
    if len(res)!=0:
        return True
    else:
        return False

def check_user_exist(username, password):
    q_check_username=f'''select id,username from users where username="{username}"'''
    res=cur.execute(q_check_username).fetchall()
    if len(res)!=0:
        db_userId=res[0][0]
        db_username=res[0][1]
        q=f'select password from users where id={db_userId}'
        db_password=cur.execute(q).fetchone()[0]
        if username==db_username and password==db_password:
            return True
        else:
            return "Invalid credentials"

def create_user(username, email, password, phone):
    if username_exists(username=username):
        return {"status":"user exists"}
    else:
        q=f'''insert into users('username', 'email', 'phone','password') values("{username}","{email}","{phone}", "{password}")'''
        cur.execute(q)
        con.commit()
        return {"status":"user created"}
