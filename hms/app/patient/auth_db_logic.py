
'''
In this file we have function for signin and signup

signup:
    create_user(username, mail, password)

signin:
    check_for_signin(mail, password)    
'''

import sqlite3

# con=sqlite3.connect('../database/data.db', check_same_thread=False)
con=sqlite3.connect('app/database/data.db', check_same_thread=False)
cur=con.cursor()

# create a user
# 'users' table->id username password mail
def check_user_exists(username, mail):
    ''' return's 0-> user doesn't exist \n 1-> if user exist's '''
    q=f'select exists(select 1 from users where username="{username}" and mail="{mail}");'
    res=cur.execute(q).fetchone()[0]
    return res

# signup
def create_user(username, mail, password):
    '''create user insert into db \n return 0->user already exists, 1->user created'''
    if check_user_exists(username=username, mail=mail):
        con.close()
        return {'user_created':False, 'status':0, 'message':'user already exists'}
    else:
        q=f'insert into users(username, password, mail) values("{username}", "{password}", "{mail}")'
        cur.execute(q)
        con.commit()
        con.close()
        return {'user_created':True, 'status':1}

# signin
def check_for_signin(mail, password):
    '''check for user in db \n return 0->user doesn't exists, 1->user exists'''
    q=f'select exists(select 1 from users where mail="{mail}" and password="{password}");'
    res=cur.execute(q).fetchone()[0]
    if res:
        return {'user_exists':True, 'status':1}
    else:
        return {'user_exists':False, 'status':0, 'message':'invalid credentials'}

def user_data(mail, password):
    return {}