from flask import Flask, render_template, request
from datetime import datetime as dt
import pyodbc
import redis
import time
import random
import hashlib

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SecureSecretKey'

def connection():
    server = 'server0105.database.windows.net'
    database = 'database2'
    username = 'admin0105'
    password = 'Azure007'
    driver = '{ODBC Driver 18 for SQL Server}'
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}')
    return conn

def redisconnection():
    try:
        r = redis.StrictRedis(host='redis0105.redis.cache.windows.net', port=6380, password='CiEFnkrCPzO3nSge3T5Jb6tHcipzGFIoOAzCaKA3SCw=', ssl=True)
        return r
    except Exception as e:
        print(e)

@app.route("/", methods=['GET', 'POST'])
def main():
    try:
        conn = connection()
        cursor = conn.cursor()
        return render_template('home.html')
    except Exception as e:
        return render_template('home.html', error=e)

@app.route("/q1", methods=['GET', 'POST'])
def q1():
    if request.method == 'POST':
        try:
            conn = connection()
            cursor = conn.cursor()
            nq = request.form['noq']
            time1 = 0
            start = time.time()
            for i in range(int(nq)):
                mag = random.randrange(1, 9)
                cursor.execute(f"SELECT id FROM all_month WHERE mag > {mag}")
            stop = time.time()
            time_diff = time1 + stop - start
            return render_template('q1.html', msg='success', time=time_diff, nq=nq)
        except Exception as e:
            print(e)
            return render_template('q1.html', error=e)
    return render_template('q1.html')

@app.route("/q1redis", methods=['GET', 'POST'])
def q1redis():
    if request.method == 'POST':
        try:
            conn = connection()
            cursor = conn.cursor()
            r = redisconnection()
            nq = request.form['noq']
            time_diff = 0
            for i in range(int(nq)):
                mag = random.randrange(1, 9)
                q = f"SELECT id FROM all_month WHERE mag > {mag}"
                hash = hashlib.sha224(q.encode('utf-8')).hexdigest()
                key = hash
                if (r.get(key)):
                    start1 = time.time()
                    data = r.get(key)
                    end1 = time.time()
                    time_diff = time_diff + (end1 - start1)
                else:
                    start1 = time.time()
                    cursor.execute(q)
                    data = cursor.fetchall()
                    end1 = time.time()
                    r.set(key, len(data))
                    r.expire(key, 30)
                    time_diff = time_diff + (end1 - start1)
            return render_template('q1redis.html', sec=time_diff, nq=nq)
        except Exception as e:
            print(e)
            return render_template('q1redis.html', error=e)
    else:
        return render_template('q1redis.html')

@app.route('/q2', methods=['POST', 'GET'])
def q2():
    if request.method == 'POST':
        try:
            conn = connection()
            cursor = conn.cursor()
            nq = request.form['noq']
            ls = request.form['ls']
            time1 = 0
            start = time.time()
            for i in range(int(nq)):
                mag = random.randrange(1, 9)
                cursor.execute(f"SELECT id FROM all_month WHERE mag > {mag} AND location = '{ls}'")
            stop = time.time()
            time_diff = time1 + stop - start
            return render_template('q2.html', msg='success', sec=time_diff, nq=nq)
        except Exception as e:
            print(e)
            return render_template('q2.html', error=e)
    return render_template('q2.html')

@app.route('/q2redis', methods=['POST', 'GET'])
def q2redis():
    if request.method == 'POST':
        try:
            conn = connection()
            cursor = conn.cursor()
            r = redisconnection()
            nq = request.form['noq']
            ls = request.form['ls']
            time_diff = 0
            for i in range(int(nq)):
                mag = random.randrange(1, 9)
                q = f"SELECT id FROM all_month WHERE mag > {mag} AND location = '{ls}'"
                hash = hashlib.sha224(q.encode('utf-8')).hexdigest()
                key = hash
                if (r.get(key)):
                    start1 = time.time()
                    data = r.get(key)
                    end1 = time.time()
                    time_diff = time_diff + (end1 - start1)
                else:
                    start1 = time.time()
                    cursor.execute(q)
                    data = cursor.fetchall()
                    end1 = time.time()
                    r.set(key, len(data))
                    r.expire(key, 30)
                    time_diff = time_diff + (end1 - start1)
            return render_template('q2redis.html', sec=time_diff, noq=nq, ls=ls)
        except Exception as e:
            print(e)
            return render_template('q2redis.html', error=e)
    else:
        return render_template('q2redis.html')

if __name__ == "__main__":
    app.run(debug=True)
