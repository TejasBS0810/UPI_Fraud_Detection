import matplotlib
matplotlib.use('Agg')
import cv2 
import os
import gc
import hashlib
import pickle
import socket
import mysql.connector as mssql
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt
import os, sys
import time
import random
import string
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
import pandas as pd
from sklearn.svm import SVR
import matplotlib.pyplot as plt
matplotlib.use('Agg')
def getMachine_addr():
	os_type = sys.platform.lower()
	command = "wmic bios get serialnumber"
	return os.popen(command).read().replace("\n","").replace("	","").replace(" ","")

def getUUID_addr():
	os_type = sys.platform.lower()
	command = "wmic path win32_computersystemproduct get uuid"
	return os.popen(command).read().replace("\n","").replace("	","").replace(" ","")

def extract_command_result(key,string):
    substring = key
    index = string.find(substring)
    result = string[index + len(substring):]
    result = result.replace(" ","")
    result = result.replace("-","")
    return result

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

def save_model_rf():
    global model
    house_model = '../Model/rf_model.pkl'
    if os.path.exists(house_model):
        return True
    else:
        return False
    
def save_model_svm():
    global model
    svm_model= '../Model/svm_model.pkl'
    if os.path.exists(svm_model):
        return True
    else:
        return False
    
def save_model_dt():
    global model
    loan_model = '../Model/dt_model.pkl'
    if os.path.exists(loan_model):
        return True
    else:
        return False

def train_rf():
    data = pd.read_csv("../Dataset/dataset.csv")
    data  = data.dropna()
    k=0
    states = {}
    print('Pre-processing')
    time.sleep(2)
    for i in data['state'].unique():
        states[i] = k
        k = k+1
    X = data.drop(columns=['fraud_risk'])
    Y = data['fraud_risk']
    X['state'] = X['state'].map(states)
    print('Pre-processing Complete')
    time.sleep(2)
    starttime = time.time()
    print('Training Started')
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    timetaken = time.time() - starttime
    print('Training Complete, Total time: ' + str(timetaken) + ' seconds')
    y_pred = rf_model.predict(X_test)
    with open("../Model/rf_model.pkl", "wb") as f:
        pickle.dump(rf_model,f)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
# Plot MAE and MSE
    plt.bar(['MAE'], [mae], color=['blue'])
    plt.xlabel('Metric')
    plt.ylabel('Error')
    plt.title('MAE for Random Forest Regressor - UPI fraud')
    plt.savefig('../Plots/mae_rf.png')
    plt.bar(['MSE'], [mse], color=['blue'])
    plt.xlabel('Metric')
    plt.ylabel('Error')
    plt.title('MSE for Random Forest Regressor - UPI fraud')
    plt.savefig('../Plots/mse_rf.png')
    return "training complete"

def train_svm():
    data = pd.read_csv("../Dataset/dataset.csv")
    data  = data.dropna()
    k=0
    states = {}
    print('Pre-processing')
    time.sleep(2)
    for i in data['state'].unique():
        states[i] = k
        k = k+1
    X = data.drop(columns=['fraud_risk'])
    Y = data['fraud_risk']
    X['state'] = X['state'].map(states)
    print('Pre-processing Complete')
    time.sleep(2)
    starttime = time.time()
    print('Training Started')
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    svm_model = SVR(kernel='rbf')
    svm_model.fit(X_train, y_train)
    timetaken = time.time() - starttime
    print('Training Complete, Total time: ' + str(timetaken) + ' seconds')
    y_pred = svm_model.predict(X_test)
    with open("../Model/svm_model.pkl", "wb") as f:
        pickle.dump(svm_model,f)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
# Plot MAE and MSE
    plt.bar(['MAE'], [mae], color=['blue'])
    plt.xlabel('Metric')
    plt.ylabel('Error')
    plt.title('MAE for SVM Regressor - UPI fraud')
    plt.savefig('../Plots/mae_svm.png')
    plt.bar(['MSE'], [mse], color=['blue'])
    plt.xlabel('Metric')
    plt.ylabel('Error')
    plt.title('MSE for SVM Regressor - UPI fraud')
    plt.savefig('../Plots/mse_svm.png')
    return "training complete"

def train_dt():
    data = pd.read_csv("../Dataset/dataset.csv")
    data  = data.dropna()
    k=0
    states = {}
    print('Pre-processing')
    time.sleep(2)
    for i in data['state'].unique():
        states[i] = k
        k = k+1
    X = data.drop(columns=['fraud_risk'])
    Y = data['fraud_risk']
    X['state'] = X['state'].map(states)
    print('Pre-processing Complete')
    time.sleep(2)
    starttime = time.time()
    print('Training Started')
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    dtr = DecisionTreeRegressor(max_depth=11)
    dtr.fit(X_train, y_train)
    timetaken = time.time() - starttime
    print('Training Complete, Total time: ' + str(timetaken))
    y_pred = dtr.predict(X_test)
    with open("../Model/dt_model.pkl", "wb") as f:
        pickle.dump(dtr,f)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
# Plot MAE and MSE
    plt.bar(['MAE'], [mae], color=['blue'])
    plt.xlabel('Metric')
    plt.ylabel('Error')
    plt.title('MAE for Decision Tree Regressor - UPI fraud')
    plt.savefig('../Plots/mae_dt.png')
    plt.bar(['MSE'], [mse], color=['blue'])
    plt.xlabel('Metric')
    plt.ylabel('Error')
    plt.title('MSE for Decision Tree Regressor - UPI fraud')
    plt.savefig('../Plots/mse_dt.png')
    return "training complete"
 
def md5(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8'))
    return md5_hash.hexdigest()
