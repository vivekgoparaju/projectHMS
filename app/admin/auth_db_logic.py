'''
In this file we have function for signin and signup for admin

signup:
    create_admin(admin_name, password)

signin:
    check_for_admin_signin(admin_name, password)    
'''

import sqlite3

con=sqlite3.connect('../database/data.db', check_same_thread=False)
cur=con.cursor()


# create a admin
# 'admin' table->id admin_name password
def check_admin_exists(admin_name):
    ''' return's 0-> admin doesn't exist \n 1-> if admin exist's '''
    q=f'select exists(select 1 from admin where admin_name="{admin_name}");'
    res=cur.execute(q).fetchone()[0]
    return res

# signup
def create_admin(admin_name, password):
    '''create admin insert into db \n return 0->admin already exists, 1->admin created'''
    if check_admin_exists(admin_name=admin_name):
        return {'admin_created':False, 'status':0, 'message':'admin already exists'}
    else:
        q=f'insert into admin(admin_name, password) values("{admin_name}", "{password}")'
        cur.execute(q)
        con.commit()
        return {'admin_created':True, 'status':1}

# signin
def check_for_admin_signin(admin_name, password):
    '''check for admin in db \n return 0->admin doesn't exists, 1->admin exists'''
    q=f'select exists(select 1 from admin where admin_name="{admin_name}" and password="{password}");'
    res=cur.execute(q).fetchone()[0]
    if res:
        return {'admin_exists':True, 'status':1}
    else:
        return {'admin_exists':False, 'status':0, 'message':'invalid credentials'}
