from flask import Flask
from flask_session import Session

app=Flask(__name__)

app=Flask(__name__, template_folder='templates')
app.config['SESSION_TYPE']='filesystem'
app.config['SESSION_PERMANENT']=False
app.config['secret_key']="1f11fb61-bf30-637e-aecc-80000b2f460c"
Session(app=app)

if __name__=="__main__":
    app.run(debug=True)