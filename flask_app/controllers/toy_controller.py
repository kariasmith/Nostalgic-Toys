from flask import Flask, render_template, request, session, redirect, flash
import requests
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.toy_model import Toy



@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect('/logout')
    
    data={
        "id": session["user_id"]
    }
    toys=Toy.view_toys()
    user=User.get_by_id(data)
    return render_template("dashboard.html", user=user, toys=toys)



@app.route('/toys/new', methods=['GET', 'POST']) 
def new_toy():
    if "user_id" not in session:
        return redirect('/logout') 
    
    if request.method=='GET':
        return render_template("new_toy.html")
    
    else:
        if not Toy.validate_toy(request.form):
            return render_template("new_toy.html")
        
        data={
            "toy_name": request.form["toy_name"],
            # "image": request.form["image"],------------------------------Not sure for a blob file
            "description": request.form["description"],
            "year": request.form["year"],
            "user_id": session["user_id"]
            }
        Toy.add_toy(data)
        print(data)
    return redirect('/dashboard')
    
    
@app.route('/toys/<int:id>')
def view_toy(id):
    if "user_id" not in session: 
        return redirect('/logout') 
    
    data={
        "id": id
    }
    # data2={
    #     "id": session["user_id"]
    # }

    Toy=Toy.show_toy(data)
    # user=User.get_by_id(data2)
    return render_template("show_toy.html", Toy=Toy)


@app.route('/toys/edit/<int:id>')
def edit_toy(id):
    if "user_id" not in session:
        return redirect('/logout')
    
    data={
        "id": id
    }
    toy=Toy.show_toy(data)
    print(data)
    
    # data2={
    #     "id": session["user_id"]
    # }
    # user=User.get_by_id(data2)
    return render_template("edit_toy.html", toy=toy)


@app.route('/toys/update/<int:id>', methods=['POST'])
def update_toy(id):
    if "user_id" not in session:
        return redirect('/logout')

    else:
        if not Toy.validate_toy(request.form):
            print("validation failed")
            return redirect(f'/toys/edit/{id}')

    data={
        "id": id,
        "toy_name": request.form["toy_name"],
        # "image": request.form["image"],------------------------------Not sure for a blob file
        "description": request.form["description"],
        "year": request.form["year"]
    }
    Toy.edit_toy(data)    
    return redirect('/dashboard')



@app.route('/toys/delete/<int:id>')
def delete_toy(id):
    if "user_id" not in session: 
        return redirect('/logout')
    
    data={
        "id": id
    }
    Toy.delete_toy(data)
    return redirect('/dashboard')