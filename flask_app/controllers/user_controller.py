from flask import render_template, request, session, redirect, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt

bcrypt=Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")



@app.route('/register', methods=['post'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    
    pw_hash=bcrypt.generate_password_hash(request.form["password"])

    data={
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash
    }
    user_id=User.add_user(data)
    session["user_id"]=user_id
    return redirect('/dashboard')



@app.route('/login', methods=['post'])
def login():
    user=User.get_by_email(request.form)

    if not user:
        flash("Invalid Email")
        return redirect('/')
    
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid Password")
        return redirect('/')
    
    session["user_id"]=user.id
    return redirect('/dashboard')    



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
