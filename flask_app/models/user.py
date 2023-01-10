from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models import queries, magazine
from flask import flash
import re
bcrypt = Bcrypt(app)
db = "subscriptions"
table = "users"
REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.{8,}$)(?=.*?[A-Z])(?=.*?[0-9])')

class User:
    def __init__(self, data):
        self.id=data["id"]
        self.first_name=data["first_name"]
        self.last_name=data["last_name"]
        self.email=data["email"]
        self.password=data["password"]
        self.magazines=[]

    @classmethod
    def save(cls, data):
        # query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        query = queries.create_query(table, data)
        print(query)
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_user_with_magazines(cls, data):
        query = "SELECT * FROM users LEFT JOIN users_has_magazines AS subscriptions ON users.id = subscriptions.users_id LEFT JOIN magazines ON magazines.id = subscriptions.magazines_id WHERE users.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        user = cls(results[0])
        for row in results:

            magazine_data = {
                "id": row["magazines.id"],
                "title": row["title"],
                "description": row["description"]
            }
            new_magazine = magazine.Magazine(magazine_data)
            new_magazine.subscribers = magazine.Magazine.get_magazine_with_user_and_subscribers({"id":new_magazine.id}).subscribers
            
            user.magazines.append(new_magazine)
        return user

    @classmethod
    def get_by_id(cls, id):
        data ={"id":id}
        query=queries.get_by(table, "id")
        return connectToMySQL(db).query_db(query, data)[0]
    @classmethod
    def get_by_email(cls, email):
        data ={"email":email}
        query=queries.get_by(table,"email")
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s WHERE id=%(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def remove_magazine(cls, data):
        query = "DELETE FROM users_has_magazines WHERE users_id=%(users_id)s AND magazines_id=%(magazines_id)s;"
        return connectToMySQL(query, data)

    @staticmethod
    def validate_user(user):
        is_valid=True
        if len(user["first_name"]) < 2:
            flash("First name must have at least 2 characters", "register")
            is_valid=False
        if len(user["last_name"]) < 2:
            flash("Last name must have at least 2 characters", "register")
            is_valid=False
        if len(user["email"]) < 2:
            flash("Email must have at least 2 characters", "register")
            is_valid=False
        if not REGEX.match(user["email"]):
            flash("Invalid email format", "register")
            is_valid=False
        if User.get_by_email(user["email"]) != False:
            flash("Email is already taken", "register")
            is_valid = False
        if len(user["password"]) < 8:
            flash("Password must have at least 8 characters", "register")
            is_valid=False
        # if not PASSWORD_REGEX.match(user["password"]):
        #     flash("Password must contain 1 capital letter and one number", "register")
        #     is_valid=False
        if user["password"] != user["confirm"]:
            flash("Passwords must match", "register")
            is_valid=False
        return is_valid
    @staticmethod
    def validate_update(user):
        is_valid=True
        if len(user["first_name"]) < 2:
            flash("First name must have at least 2 characters", "register")
            is_valid=False
        if len(user["last_name"]) < 2:
            flash("Last name must have at least 2 characters", "register")
            is_valid=False
        if len(user["email"]) < 2:
            flash("Email must have at least 2 characters", "register")
            is_valid=False
        if not REGEX.match(user["email"]):
            flash("Invalid email format", "register")
            is_valid=False
        return is_valid

    @staticmethod
    def validate_login(user):
        user_in_db = User.get_by_email(user["email"])
        if user_in_db == False:
            flash("Invalid login attempt", "login")
            return False
        if not bcrypt.check_password_hash(user_in_db.password, user["password"]):
            flash("Invalid login attempt", "login")
            return False
        return True

    def full_name(self):
        return self.first_name + " " + self.last_name
        


        
        
        
