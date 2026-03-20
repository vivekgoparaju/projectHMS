'''
In this file we have function for signin and signup for doctor

signup:
    create_doctor(doctor_name, specialization, other, password)

signin:
    check_for_signin(doctor_name, password)    
'''

import sqlite3

con=sqlite3.connect('../database/data.db', check_same_thread=False)
cur=con.cursor()


# create a doctor
# 'doctor' table->id doctor_name specialization other password 
def check_doctor_exists(doctor_name):
    ''' return's 0-> doctor doesn't exist \n 1-> if doctor exist's '''
    q=f'select exists(select 1 from doctors where doctor_name="{doctor_name}");'
    res=cur.execute(q).fetchone()[0]
    return res

# signup
def create_doctor(doctor_name, specialization , other, password):
    '''create doctor insert into db \n return 0->doctor already exists, 1->doctor created'''
    if check_doctor_exists(doctor_name=doctor_name):
        return {'doctor_created':False, 'status':0, 'message':'doctor already exists'}
    else:
        q=f'''insert into doctors(doctor_name, specialization, other, password) values("{doctor_name}","{specialization}", "{other}", "{password}")'''
        cur.execute(q)
        con.commit()
        return {'doctor_created':True, 'status':1}

# signin
def check_for_doctor_signin(doctor_name, password):
    '''check for doctor in db \n return 0->doctor doesn't exists, 1->doctor exists'''
    q=f'select exists(select 1 from doctors where doctor_name="{doctor_name}" and password="{password}");'
    res=cur.execute(q).fetchone()[0]
    if res:
        return {'doctor_exists':True, 'status':1}
    else:
        return {'doctor_exists':False, 'status':0, 'message':'invalid credentials'}
