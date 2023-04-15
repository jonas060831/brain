import json
from flask import request, make_response
from application import app, db
from datetime import datetime


@app.route("/web/signup", methods=["POST"])
def signup():
    if request.method == 'POST':
        user = request.json['user']

        try:
            db.users.insert_one({
                "username" : user['username'],
                "password" : user['password'],
                "signup_date" : datetime.utcnow(),
                "name": {
                    "first" : user['first_name'],
                    "middle" : user['middle_name'],
                    "last" : user['last_name']
                }
            })
        except Exception as e:
            print(f"ERROR: {e}")
            response = make_response({ "message" : f"ERROR: {e}" }, 400)
            return response

        print("User Created Successfully")
        response = make_response({ "message" : "User Created Successfully" }, 201)
        return response
