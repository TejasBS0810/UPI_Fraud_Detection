from flask import *
import numpy as np
from sklearn.model_selection import train_test_split
from time import sleep
import random
import os
from functools import wraps
import webbrowser
import ctypes
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
import numpy as np
import pandas as pd
import controller as ct
from time import sleep
from flask_mysqldb import MySQL
from tqdm import tqdm
import socket
def get_ip_address_of_host():
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        mySocket.connect(('10.255.255.255', 1))
        myIPLAN = mySocket.getsockname()[0]
    except:
        myIPLAN = '127.0.0.1'
    finally:
        mySocket.close()
    return myIPLAN
app=Flask(__name__, template_folder='templates', static_folder='static')
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='root'
app.config['MYSQL_DB']='upi'
app.config['MYSQL_CURSORCLASS']='DictCursor'
app.config['TEMPLATES_AUTO_RELOAD'] = True
mysql=MySQL(app)
#index route
@app.route('/')
def index():
    return render_template('login.html',error_message = '',url = url,)
#login to the application
@app.route('/login',methods=['POST','GET'])
def login():
    status=True
    if request.method=='POST':
        email=request.form["email"]
        pwd=request.form["upass"]
        cur=mysql.connection.cursor()
        cur.execute("select * from user where email=%s and password=%s",(email,pwd))
        data=cur.fetchone()
        if data:
            session['logged_in']=True
            session['username']=data["username"]
            flash('Login Successfully','success')
            return redirect('home')
        else:
            flash('Invalid Login Credentials. Try Again','danger')
    return render_template("login.html",url = url,)



#login validation
def is_logged_in(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('Unauthorized, Please Login','danger')
			return redirect(url_for('login'))
	return wrap
  
#Registration routing
@app.route('/reg',methods=['POST','GET'])
def reg():
    status=False
    if request.method=='POST':
        name=request.form["uname"]
        email=request.form["email"]
        pwd=request.form["upass"]
        cur=mysql.connection.cursor()
        cur.execute("select * from user where username=%s",[name])
        data=cur.fetchone()
        if not data:
            cur.execute("insert into user(username,password,email) values(%s,%s,%s)",(name,pwd,email))
            mysql.connection.commit()
            cur.close()
            flash('Registration Successfully. Login Now...','success')
        else:
            flash('Username Exists...Kindly use different username','danger')
        return redirect('login')
    return render_template("login.html",status=status,url = url,data = session['username'])

@app.route("/random_forest",methods=['POST','GET'])
@is_logged_in
def random_forest():
    data = pd.read_csv('../Dataset/dataset.csv')
    states = data['state'].unique()
    categories = ct.get_categories().keys()
    months = ct.get_months()
    return render_template('random_forest.html',url = url,data = session['username'],states = states, categories =categories, months = months)

@app.route("/s_v_m",methods=['POST','GET'])
@is_logged_in
def s_v_m():
    data = pd.read_csv('../Dataset/dataset.csv')
    states = data['state'].unique()
    categories = ct.get_categories().keys()
    months = ct.get_months()
    return render_template('s_v_m.html',url = url,data = session['username'],states = states, categories =categories, months = months)

@app.route("/decision_tree",methods=['POST','GET'])
@is_logged_in
def decision_tree():
    data = pd.read_csv('../Dataset/dataset.csv')
    states = data['state'].unique()
    categories = ct.get_categories().keys()
    months = ct.get_months()
    return render_template('decision_tree.html',url = url,data = session['username'],states = states, categories =categories, months = months)
global formdata
global output_file
@app.route('/rf_predict', methods=['GET', 'POST'])
@is_logged_in
def rf_predict():
    global data
    global formdata
    if request.method == 'POST':
        data = request.form.to_dict()
        form_data = {}
        form_data['Transaction Hour'] = data['trans_hour']
        form_data['Transaction Day'] = data['trans_day']
        form_data['Transaction Year'] = data['trans_year']
        form_data['Transaction Month'] = int(data['trans_month'])  # The month value will already be an integer string
        form_data['Category'] = data['category']
        form_data['UPI number'] = data['upi_number']
        form_data['Age'] = data['age']
        form_data['Transaction Amount'] = data['trans_amount']
        form_data['State'] = data['state']
        form_data['Pin Code'] = data['zip']     
    return render_template('rf_predict.html',url=url, data = session['username'],filename = form_data)
@app.route('/svm_predict', methods=['GET', 'POST'])
@is_logged_in
def svm_predict():
    global data
    global formdata
    if request.method == 'POST':
        data = request.form.to_dict()
        form_data = {}
        form_data['Transaction Hour'] = data['trans_hour']
        form_data['Transaction Day'] = data['trans_day']
        form_data['Transaction Year'] = data['trans_year']
        form_data['Transaction Month'] = int(data['trans_month'])  # The month value will already be an integer string
        form_data['Category'] = data['category']
        form_data['UPI number'] = data['upi_number']
        form_data['Age'] = data['age']
        form_data['Transaction Amount'] = data['trans_amount']
        form_data['State'] = data['state']
        form_data['Pin Code'] = data['zip']     
    return render_template('svm_predict.html',url=url, data = session['username'],filename = form_data)

@app.route('/dt_predict', methods=['GET', 'POST'])
@is_logged_in
def dt_predict():
    global data
    global formdata
    if request.method == 'POST':
        data = request.form.to_dict()
        form_data = {}
        form_data['Transaction Hour'] = data['trans_hour']
        form_data['Transaction Day'] = data['trans_day']
        form_data['Transaction Year'] = data['trans_year']
        form_data['Transaction Month'] = int(data['trans_month'])  # The month value will already be an integer string
        form_data['Category'] = data['category']
        form_data['UPI number'] = data['upi_number']
        form_data['Age'] = data['age']
        form_data['Transaction Amount'] = data['trans_amount']
        form_data['State'] = data['state']
        form_data['Pin Code'] = data['zip']     
    return render_template('dt_predict.html',url=url, data = session['username'],filename = form_data)

@app.route('/get_result_rf', methods=['GET'])
def get_result_rf():
    global data
    global formdata
    output = ct.predict_rf(data)
    print(output)
    # Replace 'path_to_image' with the actual path to your image file
    return str(output)

@app.route('/get_result_svm', methods=['GET'])
def get_result_svm():
    global data
    output = ct.predict_svm(data)
    print(output)
    # Replace 'path_to_image' with the actual path to your image file
    return str(output)

@app.route('/get_result_dt', methods=['GET'])
def get_result_dt():
    global data
    output = ct.predict_dt(data)
    print(output)
    # Replace 'path_to_image' with the actual path to your image file
    return str(output)


@app.route("/home",methods=['POST','GET'])
@is_logged_in
def home():
    global url
    if request.method=='POST':
        if request.form.get("submit") == "Predict with RF":
            return redirect('random_forest')
        if request.form.get("submit") == "Predict with SVM":
            return redirect('s_v_m')
        if request.form.get("submit") == "Predict with DT":     
            return redirect('decision_tree')
    return render_template('index.html',data = session['username'],url = url)

#logout
@app.route("/logout")
def logout():
	session.clear()
	flash('You are now logged out','success')
	return redirect(url_for('login'))

if __name__ == '__main__':
    global url
    app.secret_key='secret123'
    myIP = ct.get_ip_address_of_host()
    url = 'http://' + myIP + ':5000'
    app.run(debug=False, host='0.0.0.0',port = 5000)
