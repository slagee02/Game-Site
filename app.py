from flask import Flask, request, jsonify, session, render_template, redirect, flash, url_for
from flask_cors import CORS
from flask_session import Session
from __init__ import app, db, bcrypt
from config import ApplicationConfig
from models import *
from forms import *



#CORS(app, supports_credentials=True)



db.init_app(app)
with app.app_context():
    db.create_all()

#server_session = session(app)

Session(app)

@app.route("/", methods=["GET","POST"])
def home():
    return render_template('home.html')

@app.route("/register", methods=["GET", "POST"])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        pwd_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username = form.username.data, email = form.email.data, password = pwd_hash)
        try:
            db.session.add(user)
            db.session.commit()
        except:
            #TODO we need to make this more specific. idk if this is right
            #email_exists = User.query.filter_by(email=email).first() is not None
            #username_exists = User.query.filter_by(username=username).first() is not None
            flash('username or email taken, try again')
            return render_template('register.html', title='Register', form=form)
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
            
 

@app.route("/login", methods=["GET","POST"])
def login():
    
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    
    return render_template('login.html', title='Login', form=form)
            
    
    #session["user_id"] = user.id

@app.route("/logout", methods=["GET", "POST"])
def logout_user():
    session.pop("user_id")
    return redirect(url_for('home'))



@app.route("/@me")
def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "id": user.id,
        "email": user.email
    }) 
    


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)