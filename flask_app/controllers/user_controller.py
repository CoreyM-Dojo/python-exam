from flask_app import app
from flask import render_template, redirect, request, session
from flask_bcrypt import Bcrypt
from flask_app.models import user, magazine

bcrypt = Bcrypt(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    if not "logged_in" in session:
        return redirect("/")
    logged_in = user.User.get_by_id(session["logged_in"])
    logged_in = user.User(logged_in)
    magazines = magazine.Magazine.get_magazines_with_user()
    return render_template("dashboard.html", logged_in=logged_in, all_magazines=magazines)

@app.route("/users/edit/<int:id>", methods = ["GET", "POST"])
def update_user(id):
    if not "logged_in" in session:
        return redirect("/")
    data = {
        "id": id
    }
    
    if request.method == "GET":
        logged_in = user.User.get_user_with_magazines(data)
        return render_template("users/edit.html", logged_in=logged_in)
    else:
        if not user.User.validate_update(request.form):
            return redirect("/users/edit/" + str(id))
        update_data = {
            "id": id,
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"]
        }
        user.User.update(update_data)
        return redirect("/dashboard")


@app.route("/process", methods=["POST"])
def process():
    if request.form["which_form"] == "registration":
        if not user.User.validate_user(request.form):
            return redirect("/")
        else:
            data = {
                "first_name": request.form["first_name"],
                "last_name": request.form["last_name"],
                "email": request.form["email"],
                "password": bcrypt.generate_password_hash(request.form["password"]),
            }
            logged_in = user.User.save(data)
            session["logged_in"] = logged_in
            return redirect("/dashboard")
    elif request.form["which_form"] == "login":
        if not user.User.validate_login(request.form):
            return redirect("/")
        else:
            logged_in = user.User.get_by_email(request.form["email"])
            session["logged_in"] = logged_in.id
            return redirect("/dashboard")



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
