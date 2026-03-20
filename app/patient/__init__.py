from flask import Blueprint, render_template, session, request, redirect, url_for
from .auth import patient_auth

from faker import Faker
fake=Faker('en_IN')

patient=Blueprint("patient", __name__, template_folder="templates", static_folder='static')

# ./patient/auth
patient.register_blueprint(patient_auth, url_prefix='/auth')

@patient.before_request
def check_user_login():
    if not (request.endpoint=="patient.auth.signin" or request.endpoint=="patient.auth.signup"):
        if "isLoggedIn" in session:
            if session['isLoggedIn']:
                pass
        else:
            return render_template("auth/signin.html")


@patient.route('/profile')
def profile():
    user={"name":fake.name(),"role":fake.job(),"email":fake.email(),"phone":fake.phone_number(),"location":fake.location_on_land(),"username":fake.name(),"joined_date":fake.date()}
    return render_template("profile.html", user=user)

@patient.route('/update_profile')
def update_profile():
    pass

@patient.route('/doctors')
def doctors():
    doctors=[{"id":fake.iana_id(), "name":fake.name(), "specialization":"specialization", "img_url":"./static/image.png"} for _ in range(15)]
    specializations=[fake.job() for _ in range(10)]
    return render_template("doctors.html", specializations=specializations, doctors=doctors)

@patient.route('/doctor_details')
def doctor_details():
    id=request.args.get('id')
    doctor_details={"id":id, "name":fake.name(), "specialization":"specialization", "img_url":"./static/image.png"}
    return render_template("doctor_details.html", doctor_details=doctor_details)


@patient.route('/book_appointment')
def book_appointment():
    return render_template("appointment.html")

@patient.route('/logout')
def logout_patient():
    if 'isLoggedIn' in session:
        session['isLoggedIn']=False
    session['isLoggedIn']=False
    return redirect(url_for("patient.auth.signin"))
