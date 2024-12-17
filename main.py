import re
from flask import Flask, jsonify, redirect, render_template, request, session
from secrets import token_urlsafe
from random import randint

from werkzeug.security import check_password_hash

from db import *
from util import *

app = Flask(__name__)
app.secret_key = "GIET, best university in eastern odisha"

is_student_mail = lambda x: bool(re.match(r"^[1-9]+[a-z]+[1-9]+\.", x))

@app.route("/")
def index():
    if "id" not in session:
        return redirect("/login")
    if session["is_student"]:
        complaints = select_student_complaints(session["id"])
        complaints.reverse()
        return render_template("student.html", complaints = complaints)
    done, ongoing = [], []
    for complaint in select_faculty_complaints(session["id"]):
        if complaint[4] == "Rejected" or complaint[4] == "Resolved":
            done.append(complaint)
        else:
            ongoing.append(complaint)
    ongoing.reverse()
    done.reverse()
    return render_template("faculty.html", done = done, ongoing = ongoing)

@app.route("/get_otp", methods = ["POST"])
def get_otp():
    body = request.get_json()
    email = body['email']
    if not email.endswith("@giet.edu"):
        return "giet@edu mail is required", 401
    token = token_urlsafe(16)
    otp = randint(1000, 9999)
    send_otp(email, otp)
    insert_otp(token + email, otp)
    return jsonify({ 'token': token })

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    body = request.get_json() 
    if not validate_otp(body['token'] + body['email'], body['otp']):
        return "invalid otp", 401
    if execute_query("select * from users where email = ?", False, body["email"]):
        return "email already present", 401

    is_student = is_student_mail(body["email"])
    session["id"] = add_user(body["name"], body["email"], body["password"], is_student)
    session["name"] = body["name"]
    session["email"] = body["email"]
    session["is_student"] = is_student

    return redirect("/")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    row = execute_query("select * from users where email = ?", False, request.form['email'])
    if not row:
        return render_template("login.html", message = "email is invalid or not present")
    if not check_password_hash(row[3], request.form["password"]):
        return render_template("login.html", message = "invalid password")

    session["id"] = row[0]
    session["name"] = row[2]
    session["email"] = row[1]
    session["is_student"] = bool(row[4])
    return redirect("/")

@app.route("/raise", methods = ["GET", "POST"])
def raise_complain():
    if "id" not in session or not session["is_student"]:
        return redirect("/")
    if request.method == "GET":
        return render_template("raise.html", faculties = select_faculty())
    body = request.form
    insert_complaint(session["id"], body["fid"], body["title"], body["body"])
    row = execute_query("select email from users where id = ?", False, body["fid"])
    add_faculty_update(row[0], body["title"])
    return redirect("/")

@app.route("/status", methods = ["PATCH"])
def status():
    if "id" not in session or session["is_student"]:
        return "Unauthorised", 401
    body = request.get_json()
    update_status(body["cid"], body["status"])
    if body["status"] in ("Rejected", "Resolved"):
        row = execute_query("select email,title from complains join users on complains.sid = users.id and complains.id = ?", False, body["cid"])
        add_student_update(row[0], row[1], body["status"])
    return "Successfull", 200

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

app.run()
