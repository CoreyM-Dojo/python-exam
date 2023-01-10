from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import queries, user
from flask import flash

db = "subscriptions"
table = "magazines"

class Magazine:
    def __init__(self, data):
        self.id =data["id"]
        self.title = data["title"]
        self.description = data["description"]
        self.creator = None
        self.subscribers = []

    @classmethod
    def get_magazines_with_user(cls):
        query = "SELECT * FROM magazines LEFT JOIN users ON users.id = magazines.users_id;"

        results = connectToMySQL(db).query_db(query)
        print(results)
        magazines = []
        for row in results:
            magazine = cls(row)
            user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"]
            }

            magazine.creator = user.User(user_data)
            magazines.append(magazine)
        print("Magazines", magazines)
        return magazines

    @classmethod
    def get_magazine_with_user_and_subscribers(cls, data):
        query = "SELECT * FROM magazines LEFT JOIN users AS creator ON creator.id = magazines.users_id LEFT JOIN users_has_magazines AS subscriptions ON magazines.id = subscriptions.magazines_id LEFT join users ON users.id = subscriptions.users_id WHERE magazines.id = %(id)s;"

        results = connectToMySQL(db).query_db(query, data)

        magazine = cls(results[0])
        for row in results:
            print(row)
            subscriber_data = {
                "id": row["users.id"],
                "first_name": row["users.first_name"],
                "last_name": row["users.last_name"],
                "email": row["users.email"],
                "password": row["users.password"]
            }
            user_data = {
                "id": row["creator.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"]
            }
            magazine.creator = user.User(user_data)
            magazine.subscribers.append(user.User(subscriber_data))
        return magazine

    @classmethod
    def subscribe(cls, data):
        query = "INSERT INTO users_has_magazines (users_id, magazines_id) VALUES (%(users_id)s, %(magazines_id)s)"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def save(cls, data):
        query = queries.create_query(table, data)
        print(query)
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def destroy(cls, id):
        query = queries.delete_query(table)
        return connectToMySQL(db).query_db(query, {"id": id})

    @staticmethod
    def validate_magazine(mag):
        is_valid = True
        if len(mag["title"]) < 2:
            flash("Title is required and must have at least 2 characters")
            is_valid = False
        if len(mag["description"]) < 10:
            flash("Description is required and must have at least 10 characters")
            is_valid = False
        return is_valid

