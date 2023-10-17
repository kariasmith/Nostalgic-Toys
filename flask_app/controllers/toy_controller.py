from flask import Flask, render_template, request, session, redirect, flash
#import requests
from werkzeug.utils import secure_filename
import os
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
        
    uploaded_image = request.files.get('imageInput')
    print(uploaded_image)
    if 'imageInput' not in request.files:
            flash('No file part')
            print("Image not in request files")
            return redirect("/dashboard")
    else:
        print('Image in get files')
        file_name= uploaded_image.filename
        print(file_name)
            # Save the uploaded image to a specific folder on your server
            # Construct the image path based on a filename (e.g., the toy's name)
            # This assumes you have a folder named 'uploads' for storing images
        image_filename = secure_filename(uploaded_image.filename)
        image_path = os.path.join(app.config["upload_folder"], image_filename)
        uploaded_image.save(image_path)
        
    data={
        "toy_name": request.form["toy_name"],
        "description": request.form["description"],
        "image_path" : file_name,
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

    toy=Toy.show_toy(data)
    # user=User.get_by_id(data2)
    return render_template("show_toy.html", toy=toy)


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
        
    uploaded_image = request.files.get('imageInput')
    print(uploaded_image)
    if 'imageInput' not in request.files:
            flash('No file part')
            print("Image not in request files")
            return redirect("/dashboard")
    else:
        print('Image in get files')
        file_name= uploaded_image.filename
        print(file_name)
            # Save the uploaded image to a specific folder on your server
            # Construct the image path based on a filename (e.g., the toy's name)
            # This assumes you have a folder named 'uploads' for storing images
        image_filename = secure_filename(uploaded_image.filename)
        image_path = os.path.join(app.config["upload_folder"], image_filename)
        uploaded_image.save(image_path)

    data={
        "id": id,
        "toy_name": request.form["toy_name"],
        "image_path" : file_name,
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