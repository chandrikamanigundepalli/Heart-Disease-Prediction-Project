from flask import Flask, request, render_template,redirect,jsonify,url_for
from flask_cors import CORS
import pandas as pd
import joblib
import json
import time
import datetime
from datetime import timedelta
import statsmodels.api as sm
import scipy.stats as stats
# from train import train
import sqlite3
import numpy as np
import pickle as pickle

app = Flask(__name__)

model = joblib.load("model.sav")
scalerX = pickle.load(open("scalerX", "rb"))

@app.route('/')
def home():
    return render_template('login.html')

@app.route("/signup")
def signup():
    name = request.args.get('username','')
    dob = request.args.get('DOB','')
    sex = request.args.get('Sex','')
    contactno = request.args.get('CN','')
    email = request.args.get('email','')
    martial = request.args.get('martial')
    password = request.args.get('psw','')

    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `accounts` (`name`, `dob`,`sex`,`contact`,'martial',`email`, `password`) VALUES (?, ?, ?, ?, ?, ?, ?)",(name,dob,sex,contactno,martial,email,password))
    con.commit()
    con.close()

    return render_template("login.html")

@app.route("/signin")
def signin():
    mail1 = request.args.get('uname','')
    password1 = request.args.get('psw','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `email`, `password` from accounts where `email` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("login.html")

    elif mail1 == data[0] and password1 == data[1]:
        return render_template("home1.html")

    
    else:
        return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/tips')
def tips():
    return render_template("healthtips1.html")

@app.route('/doc')
def doc():
    return render_template("doctor.html")

@app.route('/home1')
def home1():
    return render_template("home1.html")

@app.route('/food')
def food():
    return render_template("food.html")

@app.route('/sym')
def sym():
    return render_template("sym.html")

@app.route('/caution')
def caution():
    return render_template("precaution.html")

@app.route('/style')
def style():
    return render_template("style.html")

@app.route('/prediction')
def prediction():
    return render_template("index.html")


@app.route('/result')
def result():
    return render_template("result.html")

@app.route("/index", methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    elif request.method == 'POST':
        age = request.form['feedback1']
        sex = request.form['feedback2']
        chest_pain_type = request.form['feedback3']
        resting_blood_pressure = request.form['feedback4']
        Serum_cholestrol = request.form['feedback5']
        fasting_blood_sugar = request.form['feedback6']
        resting_ECG = request.form['feedback7']
        Max_heart_rate_achieved = request.form['feedback8']
        Exercise_induced_angina = request.form['feedback9']
        Thalassemmia = request.form['feedback0']
            
        to_predict = [age,sex,chest_pain_type,resting_blood_pressure,Serum_cholestrol,fasting_blood_sugar,resting_ECG,Max_heart_rate_achieved,Exercise_induced_angina,Thalassemmia]
        

        rf_result = model.predict(scalerX.transform([to_predict]))

        

        if rf_result[0] == 0:
            remarks = 'Not Having heart disease'
            to_predict1 = [age,sex,chest_pain_type,resting_blood_pressure,Serum_cholestrol,fasting_blood_sugar,resting_ECG,Max_heart_rate_achieved,Exercise_induced_angina,Thalassemmia,remarks]
            result1 = 'you are not having any heart disease symptoms.'
            return render_template("result.html", rf_result=result1,to_predict=to_predict1)

        else:
            remarks = 'Having Heart disease'
            to_predict1 = [age,sex,chest_pain_type,resting_blood_pressure,Serum_cholestrol,fasting_blood_sugar,resting_ECG,Max_heart_rate_achieved,Exercise_induced_angina,Thalassemmia,remarks]
            result1 = 'Sorry to say that you have a heart problem.'
            return render_template("result.html", rf_result=result1,to_predict=to_predict1)

if __name__ == "__main__":
    app.run(debug=True)