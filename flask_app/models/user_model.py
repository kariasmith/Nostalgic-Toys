from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = "nostalgic_toys"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def add_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        # data is a dictionary that will be passed into the save method from server.py
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        print("Get user by id: ", results)
        return cls(results[0])
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @staticmethod
    def validate_user(user):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(User.DB).query_db(query,user)
        is_valid = True # we assume this is true
        if len(results) >= 1:
            flash("Email already has been used.", "register")
            is_valid = False
        if len(user['first_name']) < 3:
            flash("First name is required and must be at least 3 characters.", "register")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name is required and must be at least 3 characters.", "register")
            is_valid = False
        if (user['first_name']).isalpha() == False:
            flash("First name must be all letters.", "register")
            is_valid = False
        if (user['last_name']).isalpha() == False:
            flash("Last name must be all letters.", "register")
            is_valid = False
        if len(user['email']) <= 0:
            flash("Email is required.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "register")
            is_valid = False
        if len(user["email"]) > 0 and not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email format.", "register")
            is_valid = False
        if len(user['password']) <= 0:
            flash("Password is required.", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters long.", "register")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords don't match", "register")
            is_valid = False
        return is_valid
