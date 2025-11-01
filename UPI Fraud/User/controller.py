import os
import hashlib
import pickle
import mysql.connector as mssql
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt
import os, sys
import socket
import pandas as pd
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
def preprocess(data):
    data1 = pd.read_csv('../Dataset/dataset.csv')
    states = data1['state'].unique()
    k=0
    states = {}
    for i in data1['state'].unique():
        states[i] = k
        k = k+1
    data['state'] = states[data['state']]
    data['category'] = get_categories()[data['category']]
    if data['submit']:
        del data['submit']
    return data

def get_categories():
    categories = {
        'Entertainment': 1,
        'Food/Dining': 2,
        'Gas-Transport':3,
        'Grocery-NET': 4,
        'Grocery-POS': 5,
        'Health/Fitness': 6,
        'Home': 7,
        'Kids/Pets': 8,
        'Miscellaneous-NET': 9,
        'Miscellaneous-POS': 10,
        'Personal-Care': 11,
        'Shopping': 12,
        'Travel':13
    }
    return categories

def get_months():
    months = {
        'January': 1,
        'February': 2,
        'March':3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }
    return months

def predict_rf(data):
    new_df = pd.DataFrame([preprocess(data)])
    print(new_df)
    with open('../Model/rf_model.pkl', 'rb') as f:
        rf_regressor = pickle.load(f)
    predicted_price = rf_regressor.predict(new_df)
    if predicted_price > 0.20:
        print("Fraudulent")
        return "Fraudulent"
    else:
        print("Non Fraudulent")
        return "Non Fraudulent"

def predict_svm(data):
    new_df = pd.DataFrame([preprocess(data)])
    with open('../Model/svm_model.pkl', 'rb') as f:
        rf_regressor = pickle.load(f)
    predicted_price = rf_regressor.predict(new_df)
    if predicted_price > 0.20:
        print("Fraudulent")
        return "Fraudulent"
    else:
        print("Non Fraudulent")
        return "Non Fraudulent"

def predict_dt(data):
    new_df = pd.DataFrame([preprocess(data)])
    with open('../Model/dt_model.pkl', 'rb') as f:
        rf_regressor = pickle.load(f)
    predicted_price = rf_regressor.predict(new_df)
    if predicted_price > 0.20:
        print("Fraudulent")
        return "Fraudulent"
    else:
        print("Non Fraudulent")
        return "Non Fraudulent"

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

def md5(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8'))
    return md5_hash.hexdigest()
