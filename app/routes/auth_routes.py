from flask import Blueprint, request, redirect, url_for, render_template, session, flash
from datetime import timedelta
from app.models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint("auth_routes", __name__)
bp.permanent_session_lifetime = timedelta(minutes=1440)

@bp.route('/')
def home():
    return render_template("signup.html")


@bp.route("/login", methods=["GET", "POST"])
def login(): 
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session.permanent = True
            session["user"] = email
            session["user_id"] = user.id
            flash("Login Successful")
            return redirect(url_for("auth_routes.user"))
        else:
            flash("Invalid email or password")
            return redirect(url_for("auth_routes.login"))
    else:
        if "user" in session:
            flash("Already logged in")
            return redirect(url_for("auth_routes.user"))
        return render_template("login.html")


@bp.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    else:
        flash("you are not Logged in")
        return redirect(url_for("auth_routes.login"))
    
@bp.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        
        # Check if user already exists
        found_user = User.query.filter_by(email=email).first()
        if found_user:
            flash("Email already registered")
            return redirect(url_for("auth_routes.login"))
        
        # Create new user with hashed password
        hashed = generate_password_hash(password)
        user = User(name=name, email=email, password=hashed)
        db.session.add(user)
        db.session.commit()
        
        # Log the user in
        session.permanent = True
        session["user"] = email
        session["user_id"] = user.id
        flash("Registration successful! Welcome!")
        return redirect(url_for("auth_routes.user"))
        
    return render_template("signup.html")
    
@bp.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    flash("You have been logged out!", "info")
    return redirect(url_for("auth_routes.login"))
