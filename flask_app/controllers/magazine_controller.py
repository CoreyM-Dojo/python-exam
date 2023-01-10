from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, magazine

@app.route("/magazines", methods=["GET", "POST"])
def create_magazine():
    if not "logged_in" in session:
        return redirect("/")
    
    if request.method == "GET":
        return render_template("magazines/create.html", logged_in = user.User.get_by_id(session["logged_in"]))
    elif request.method == "POST":
        if not magazine.Magazine.validate_magazine(request.form):
            return redirect("/magazines")
        magazine.Magazine.save(request.form)
        return redirect("/dashboard")

@app.route("/magazines/<int:id>")
def show_magazine(id):
    if not "logged_in" in session:
        return redirect("/")
    data = {
        "id": id
    }
    mag = magazine.Magazine.get_magazine_with_user_and_subscribers(data)
    return render_template("magazines/show.html", mag=mag,logged_in=user.User.get_by_id(session["logged_in"]))

@app.route("/magazines/delete/<int:id>")
def delete_magazine(id):
    if not "logged_in" in session:
        return redirect("/")
    magazine.Magazine.destroy(id)
    return redirect("/dashboard")

@app.route("/subscribe/<int:users_id>/<int:magazines_id>")
def subscribe(users_id, magazines_id):
    if not "logged_in" in session:
        return redirect("/")
    data = {
        "users_id": users_id,
        "magazines_id": magazines_id
    }
    magazine.Magazine.subscribe(data)
    return redirect("/dashboard")