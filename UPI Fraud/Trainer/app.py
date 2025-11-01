from flask import *
import time
import os
import cv2
from functools import wraps
from werkzeug.utils import secure_filename
import numpy as np
import numpy as np
import pandas as pd
from flask_mysqldb import MySQL
import socket
import controller as ct
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

@app.route('/login',methods=['POST','GET'])
def login():
    status=True
    if request.method=='POST':
        uname=request.form["email"]
        pwd=request.form["upass"]
        cur=mysql.connection.cursor()
        cur.execute("select * from admin where email=%s and password=%s",(uname,ct.md5(pwd)))
        data=cur.fetchone()
        if data:
            session['logged_in']=True
            session['username']=data["username"]
            flash('Login Successfully','success')
            return redirect('home')
        else:
            flash('Invalid Login credentials. Try Again','danger')
    return render_template("login.html",url = url)


@app.route('/')
def index():
    return render_template('login.html')

def is_logged_in(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('Unauthorized, Please Login','danger')
			return redirect(url_for('login'))
	return wrap
@app.route("/random_forest",methods=['POST','GET'])
@is_logged_in
def random_forest():
    return render_template('random_forest.html',url = url,data = session['username'])

@app.route("/s_v_m",methods=['POST','GET'])
@is_logged_in
def s_v_m():
    return render_template('s_v_m.html',url = url,data = session['username'])

@app.route("/dt",methods=['POST','GET'])
@is_logged_in
def dt():
    return render_template('decision_tree.html',url = url,data = session['username'])


@app.route('/get_dataset', methods=['GET', 'POST'])
@is_logged_in
def get_dataset():
    if (os.listdir('../Dataset')):
        df = pd.read_csv('../Dataset/dataset.csv')
        time.sleep(3)
        return str(df.shape[0]) + " Rows found"
    else:
        return "No dataset Found in the path specified. Copy the files to path and refresh and try again"
@app.route('/start_training_rf', methods=['GET', 'POST'])
@is_logged_in
def start_training_rf():
    ct.train_rf()
    return "Training Completed"

@app.route('/start_training_svm', methods=['GET', 'POST'])
@is_logged_in
def start_training_svm():
    ct.train_svm()
    return "Training Completed"

@app.route('/start_training_dt', methods=['GET', 'POST'])
@is_logged_in
def start_training_dt():
    ct.train_dt()
    return "Training Completed"

@app.route('/save_model_rf', methods=['GET', 'POST'])
@is_logged_in
def save_model_rf():
    if(ct.save_model_rf()):
        return "Model Saved Successfully"
    else:
        return "Failed to save model"

@app.route('/save_model_svm', methods=['GET', 'POST'])
@is_logged_in
def save_model_svm():
    if(ct.save_model_svm()):
        return "Model Saved Successfully"
    else:
        return "Failed to save model"

@app.route('/save_model_dt', methods=['GET', 'POST'])
@is_logged_in
def save_model_dt():
    if(ct.save_model_dt()):
        return "Model Saved Successfully"
    else:
        return "Failed to save model"

@app.route('/show_rmse_rf', methods=['GET', 'POST'])
@is_logged_in
def show_rmse_rf():
    time.sleep(2)
    return send_file('../Plots/mse_rf.png', mimetype='image/jpg')

@app.route('/show_rmse_svm', methods=['GET', 'POST'])
@is_logged_in
def show_rmse_svm():
    time.sleep(2)
    return send_file('../Plots/mse_svm.png', mimetype='image/jpg')

@app.route('/show_rmse_dt', methods=['GET', 'POST'])
@is_logged_in
def show_rmse_dt():
    time.sleep(2)
    return send_file('../Plots/mse_dt.png', mimetype='image/jpg')

@app.route('/show_mae_rf', methods=['GET', 'POST'])
@is_logged_in
def show_mae_rf():
    time.sleep(2)
    return send_file('../Plots/mae_rf.png', mimetype='image/jpg')

@app.route('/show_mae_svm', methods=['GET', 'POST'])
@is_logged_in
def show_mae_svm():
    time.sleep(2)
    return send_file('../Plots/mae_svm.png', mimetype='image/jpg')

@app.route('/show_mae_dt', methods=['GET', 'POST'])
@is_logged_in
def show_mae_dt():
    time.sleep(2)
    return send_file('../Plots/mae_dt.png', mimetype='image/jpg')


#Home page
@app.route("/home",methods=['POST','GET'])
@is_logged_in
def home():
    if request.method=='POST':
        if request.form.get("submit") == "Train with RF":
            return redirect('random_forest')
        if request.form.get("submit") == "Train with SVM":
            return redirect('s_v_m')
        if request.form.get("submit") == "Train with DT":     
            return redirect('dt')
    return render_template('index.html',data = session['username'],url = url)

@app.route("/logout")
def logout():
	session.clear()
	flash('You are now logged out','success')
	return redirect(url_for('login'))

if __name__ == '__main__':
    global url
    app.secret_key='secret123'
    myIP = ct.get_ip_address_of_host()
    url = 'http://' + myIP + ':5001'
    app.run(debug=False, host='0.0.0.0',port = 5002)
