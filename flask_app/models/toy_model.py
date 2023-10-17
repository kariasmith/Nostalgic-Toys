from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user_model import User

class Toy:
    DB = "nostalgic_toys"
    def __init__(self,data):
        self.id = data["id"]
        self.toy_name = data["toy_name"]
        self.description = data["description"]
        self.year = data["year"]
        self.image_path = data["image_path"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

    @classmethod
    def show_toy(cls, data):
        query = "SELECT * FROM toys LEFT JOIN users on toys.user_id = users.id WHERE toys.id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        print("Raw data for one toy: ", results)
        toy = results[0]
        print("The initiated toy result:", toy)
        return toy

    @classmethod
    def view_toys(cls):
        query = "SELECT * FROM toys;"
        results = connectToMySQL(cls.DB).query_db(query)
        # print("Raw data for all toys: ", results)
        toys = []
        for x in results:
            toys.append(x)
        # print("The initiated toys result:", toys)
        return toys
    
    @classmethod
    def add_toy(cls, data):
        if not cls.validate_toy(data):
            print("in save if not valid...")
            return False
        # print("Data passed into create add_toy METHOD: ", data)
        query = "INSERT into toys (toy_name, description, year, image_path, created_at, updated_at, user_id) values (%(toy_name)s, %(description)s, %(year)s, %(image_path)s, NOW(), NOW(), %(user_id)s);"
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result

    @classmethod
    def edit_toy(cls, data):
        print("Data passed into edit_toy METHOD: ", data)
        query = "UPDATE toys SET toy_name=%(toy_name)s, description=%(description)s, year=%(year)s, image_path=%(image_path)s, updated_at=NOW() WHERE id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result

    @classmethod
    def delete_toy(cls, data):
        query = "DELETE from toys WHERE id = %(id)s;"
        connectToMySQL(cls.DB).query_db(query, data)
        return id

    @staticmethod
    def validate_toy(data):
        is_valid = True
        if len(data["toy_name"]) == 0:
            flash("Name of the toy is required.", "new_toy")
            is_valid = False
        if len(data["description"]) == 0:
            flash("Description is required.", "new_toy")
            is_valid = False
        if len(data["year"]) == 0:
            flash("Year is required.", "new_toy")
            is_valid = False
        return is_valid
