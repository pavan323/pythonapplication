#!/usr/bin/python3
# -*- coding: utf-8 -*-


from flask import (Flask, request, jsonify, session, render_template, flash,
                    redirect, url_for, make_response)
from uuid import uuid4
from os import path
from datetime import datetime as DT


import sqlite3
import base64
import time
import os
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'			# Creates a random key





def insert_users(email,username,password):
    try:
        conn = sqlite3.connect('users.db');#print("Users")
        cur = conn.cursor()
        now = DT.now();#print(now)
        creation_date = now.strftime('%Y-%m-%d %H:%M:%S');#print("Hello")
        encrypt_password = str(base64.b64encode(password.encode('utf-8', errors='ignore')));
        newUserQuery = '''INSERT INTO users(email,username, password, creation_date) values (?, ?, ?, ?)'''
        cur.execute(newUserQuery, (email, username, encrypt_password, creation_date))
        conn.commit()
        query = """SELECT user_id, username, password from users"""
        data = cur.execute(query)
        #print(data)
        conn.commit()
        return 0
    except Exception as e:
        print(e)
        return 1
def users_table():
    try:
        if 'users.db' not in os.listdir(os.getcwd()):
            conn = sqlite3.connect('users.db');
            cur = conn.cursor()
            HPU_create = """CREATE TABLE "users" ("user_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "email" NVARCHAR(100) NOT NULL UNIQUE, "username" TEXT(100) NOT NULL UNIQUE,
            "password" NVARCHAR(100) NOT NULL, "creation_date" TEXT(100), "flag" TEXT DEFAULT "Active");"""
            data=cur.execute(HPU_create)
            #print(data)
            conn.commit()
            insert_users('admin@admin.com','admin','admin')
    except Exception as e:
        print(e)
        return 1









def db_connect():                                   
	
    # If the DB file already exists it just returns the connection else
    dbfile = "users.db"

    if path.isfile(dbfile):
        conn = sqlite3.connect(dbfile)
        return conn
    
  


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        conn = db_connect()
        cur = conn.cursor()
        email = request.form.get("email")
        password = request.form.get("password")
        username = request.form.get("username")
        inserted=insert_users(email,username,password)
        if inserted == 0:
            flash ("User has been added successfully")
            return render_template("adduser.html") 
        else:
            flash ("User has been Failed to add")
            return render_template("adduser.html")  
    else:
       return render_template("adduser.html") 

@app.route('/login', methods=['GET','POST'])
def login():
    
    if request.method == 'POST':
        conn = db_connect()
        cur = conn.cursor()
        email = request.form.get("email")
        password = request.form.get("password").encode('utf-8', errors='ignore')    
        encryptPassword = str( base64.standard_b64encode( password ))
        query = """SELECT user_id, username, password from users where email = '{uname}' and flag= 'Active'""".format(uname=email)
        data = cur.execute(query)
        res = cur.fetchall();#print(res)
        conn.close()

        if any(res):
            data = [dat[0] for dat in data.description]
            response = dict(zip(data, res[0]))
            #print(response['username'])
            passDB = response['password']
            if passDB == encryptPassword:
             
                session[ response["username"] ] = int( time.time() )
                #print(response['username'])
                return redirect( url_for( "welcome", user=response['username'] ))
                

            else:

                flash ("Login Failed Incorrect password")
                return render_template("login.html")
    
        else:
            flash ("Email does not exists")
            return render_template("login.html")
            
    else:
        return render_template("login.html")



@app.route('/logout/<string:user>', methods=['DELETE'])
def logout(user):
    if user in session.keys():
        session.pop(user,None)
        return make_response(jsonify({"status":"success", "response":"logged out"}), 200)
    else:
        return render_template("index.html")





@app.route("/<string:user>")
def welcome(user):
    # redirects to the dashboard page if the user available in session
    # else it will be redirected to the home page
    if user in session.keys() :
        return render_template("welcome.html",user=user)
    
    else:
        return render_template("index.html")
        
@app.route("/")
def index() :
    
    #redirects you to the home page
    return render_template("index.html")


if __name__ == '__main__':
    #This will run if the application has been run as a main file.
	users_table()
	app.run( host="0.0.0.0",debug=True, port=8000 )


