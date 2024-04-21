from flask import Flask, render_template, request
import pyodbc

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
    try:
        conn = connection()
        cursor = conn.cursor()
        execute_query(cursor)
        a1, a2, a3, a4, a5 = fetch_results(cursor)
        return render_template('q1.html', msg='success', a1=a1, a2=a2, a3=a3, a4=a4, a5=a5)
    except Exception as e:
        return render_template('q1.html', error=e)

@app.route("/q2", methods=['GET', 'POST'])
def q2():
    try:
        conn = connection()
        cursor = conn.cursor()
        execute_query(cursor)
        a1, a2, a3, a4, a5 = fetch_results(cursor)
        return render_template('q2.html', msg='success', a1=a1, a2=a2, a3=a3, a4=a4, a5=a5)
    except Exception as e:
        return render_template('q2.html', error=e)

@app.route("/q3", methods=['GET', 'POST'])
def q3():
    return render_template('q3.html') 

@app.route('/runq3', methods=['GET', 'POST'])
def runq3():
    if request.method == 'POST':
        try:
            conn = connection()
            cursor = conn.cursor()
            mag1, mag2, dep1, dep2 = get_form_data(request)
            ccbd, cnt = execute_query_with_params(cursor, mag1, mag2, dep1, dep2)
            return render_template('q3.html', ccbd=ccbd, mag1=mag1, mag2=mag2, dep1=dep1, dep2=dep2, cnt=cnt, msg="success")
        except Exception as e:
            print(e)
            return render_template('q3.html', error='error')
    return render_template('q3.html')

def execute_query(cursor):
    cursor.execute('SELECT COUNT(*) FROM all_month WHERE mag <= 1.0')
    cursor.execute('SELECT COUNT(*) FROM all_month WHERE mag BETWEEN 1.0 AND 2.0')
    cursor.execute('SELECT COUNT(*) FROM all_month WHERE mag BETWEEN 2.0 AND 3.0')
    cursor.execute('SELECT COUNT(*) FROM all_month WHERE mag BETWEEN 3.0 AND 4.0')
    cursor.execute('SELECT COUNT(*) FROM all_month WHERE mag BETWEEN 4.0 AND 5.0')

def fetch_results(cursor):
    results = []
    for row in cursor.fetchall():
        results.append(row[0])
    return results

def get_form_data(request):
    mag1 = float(request.form['mag1'])
    mag2 = float(request.form['mag2'])
    dep1 = float(request.form['dep1'])
    dep2 = float(request.form['dep2'])
    return mag1, mag2, dep1, dep2

def execute_query_with_params(cursor, mag1, mag2, dep1, dep2):
    ccbd = []
    cnt = 0
    cursor.execute('SELECT mag, depth FROM all_month WHERE mag BETWEEN ? AND ? AND depth BETWEEN ? AND ? ORDER BY mag, depth', (mag1, mag2, dep1, dep2))
    for row in cursor.fetchall():
        ccbd.append(row)
        cnt += 1
    return ccbd, cnt

if __name__ == "__main__":
    app.run(debug=True)
