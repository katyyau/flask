from flask import Flask, request, make_response
import pandas as pd
import os

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!Happy</p>"

@app.route("/page2")
def page2():
    return "<p>Hello, World! Page 2</p>"

@app.route("/page3/<username>")
def page3(username):
    return f"This is a profile of {username}"

@app.route("/page4/")
def page4():
    userid = request.args.get("userid")
    return f"This is a profile of {userid}"

@app.route("/register/")
def register():
    username = request.args.get('username')
    password = request.args.get('password')

    if username is None:
        return "User name cannot be None."
    if password is None:
        return "Password cannot be None."

    df = pd.DataFrame([
        [username, password, ""]
    ], columns=['username', 'password', 'description'])

    if os.path.exists("username_and_pw.csv"):
        old_df = pd.read_csv("username_and_pw.csv")

        number_of_same_username = len(old_df[old_df['username'] == username])

        if number_of_same_username == 0:
            df = old_df.append(df)
        else:
            return "Fail, same username already exist."

    df.to_csv("username_and_pw.csv", index=False)

    return "Success!"

@app.route("/login/")
#http://127.0.0.1:5000/login/?username=bobby&password=bobby
def login ():
    username = request.args.get("username")
    password = request.args.get("password")

    login_register_book = pd.read_csv("username_and_pw.csv")

    if sum((username == login_register_book.username) & (password == login_register_book.password)) >=1:
        resp = make_response("Success")
        resp.set_cookie('username', username)
        return resp
    else:
        return "Your username or password is wrong"


@app.route("/set_description/")
#http://127.0.0.1:5000/set_description/?description=iambobby
def set_description():
    username = request.cookies.get('username')
    description = request.args.get('description')

    df = pd.read_csv("username_and_pw.csv")

    if len(df[df.username == username]) == 1:
        df.loc[df.username == username, "description"] = description
    else:
        return f"Fail"

    df.to_csv("username_and_pw.csv", index=False)

    return f"{username}'s description updated: {description}"

@app.route("/view_description/")
#http://127.0.0.1:5000/view_description/?username=bobby
def view_description():
    username = request.cookies.get('username')

    df = pd.read_csv("username_and_pw.csv")

    if len(df[df.username == username]) == 1:
        return f"{username}'s description is {df[df.description]}"
    else:
        return f"Fail"
