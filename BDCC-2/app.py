from flask import Flask, render_template, request
from geopy.distance import geodesic
from datetime import datetime as dt
import pyodbc

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecureSecretKey'

def connection():
    server = 'server0105.database.windows.net'
    database = 'database2'
    username = 'admin0105'
    password = 'Azure007'
    driver = '{ODBC Driver 18 for SQL Server}'   
    conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+password)
    return conn

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
    return render_template('q1.html')

@app.route("/runq1", methods=['GET', 'POST'])
def runq1():
    try:
        conn = connection()
        cursor = conn.cursor()
        mag = request.form['mag']
        m = float(mag)
        cursor.execute('SELECT * FROM all_month WHERE mag > ?', m)
        data = cursor.fetchall()
        count = len(data)
        if count > 0:
            return render_template('q1.html', data=data, count=count, msg="Data Found")
        elif count <= 0:
            return render_template('q1.html', error="No data found!!")
    except Exception as e:
        return render_template('q1.html', error=e)

@app.route("/q2", methods=['GET', 'POST'])
def q2():
    return render_template('q2.html')    

@app.route("/runq2", methods=['GET', 'POST'])
def runq2():
    try:
        conn = connection()
        cursor = conn.cursor()
        mag1 = float(request.form['mag1'])
        mag2 = float(request.form['mag2'])
        date1 = request.form['date1']
        date2 = request.form['date2']
        cursor.execute('SELECT * FROM all_month WHERE time BETWEEN ? AND ? AND mag BETWEEN ? AND ?', date1, date2, mag1, mag2)
        data = cursor.fetchall()
        count = len(data)
        if count > 0:
            return render_template('q2.html', data=data, count=count, msg="Data Found")
        elif count <= 0:
            return render_template('q2.html', error="No data found!!")
    except Exception as e:
        return render_template('q2.html', error=e)

@app.route("/q3", methods=['GET', 'POST'])
def q3():
    return render_template('q3.html')    

@app.route("/runq3", methods=['GET', 'POST'])
def runq3():
    try:
        conn = connection()
        cursor = conn.cursor()
        distance = float(request.form['dist'])
        lat = float(request.form['lat'])
        long = float(request.form['long'])
        count = 0
        result = []
        cursor.execute('SELECT time, latitude, longitude, mag, place FROM all_month')
        while True:
            row = cursor.fetchone()
            if not row:
                break
            if geodesic((float(row[1]), float(row[2])), (lat, long)).km <= distance:
                result.append(row)
                count += 1
        if count > 0:
            return render_template('q3.html', data=result, count=count, msg="Data Found")
        elif count <= 0:
            return render_template('q3.html', error="No data found!!")
    except Exception as e:
        return render_template('q3.html', error=e)

@app.route("/q4", methods=['GET', 'POST'])
def q4():
    return render_template('q4.html')    

@app.route("/runq4", methods=['GET', 'POST'])
def runq4():
    try:
        conn = connection()
        cursor = conn.cursor()
        cluster = request.form['cluster']
        cursor.execute('SELECT * FROM all_month WHERE type = ?', cluster)
        data = cursor.fetchall()
        count = len(data)
        if count > 0:
            return render_template('q4.html', data=data, count=count, msg="Data Found")
        elif count <= 0:
            return render_template('q4.html', error="No data found!!")
    except Exception as e:
        return render_template('q4.html', error=e)

@app.route("/q5", methods=['GET', 'POST'])
def q5():
    try:
        conn = connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM all_month WHERE mag > 4.0')
        data = cursor.fetchall()
        count = len(data)
        result = []
        for x in data:
            l = x[0].strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            hr = dt.strptime(l, '%Y-%m-%dT%H:%M:%S.%fZ').hour
            if (hr > 18 or hr < 7):
                result.append(x)
        if count > 0:
            return render_template('q5.html', data=result, count=count, msg="Data Found")
        elif count <= 0:
            return render_template('q5.html', error="No data found!!")
    except Exception as e:
        return render_template('q5.html', error=e)  

if __name__ == "__main__":
    app.run(debug=True)
