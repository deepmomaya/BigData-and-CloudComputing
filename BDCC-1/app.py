from flask import Flask,flash, redirect, render_template, request
from werkzeug.utils import secure_filename
import os
import csv

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SecureSecretKey'

app.config['UPLOAD_FOLDER'] = './static/'

@app.route("/")
def main():
    return render_template('home.html')

@app.route("/uploadcsv", methods=['GET','POST'])
def uploadcsv():
    return render_template('uploadcsv.html')

@app.route("/uploader", methods=['GET','POST'])
def uploader():
    if request.method == 'POST':
        fil = request.files['files']
        if fil.filename == '':
            return ('<p>Oops error</p> <br><br><a href = '/'>HOME</a>')
        if fil:
            filename = secure_filename(fil.filename)
            fil.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "<p>File upload was success</p> <br><br><a href = '/'>HOME</a>"
        
@app.route("/viewcsv",methods = ['GET','POST'])
def viewcsv():
    csvdata = []
    csvfile = csv.DictReader(open('./static/people.csv'))
    for x in csvfile:
        csvdata.append(x)
    return render_template('viewcsv.html',data=csvdata,msg="Done",error="error")

@app.route("/q1", methods=['GET','POST'])
def q1():
    return render_template('q1.html')

@app.route("/runq1", methods=['GET','POST'])
def runq1():
    if request.method == 'POST':
        fo = request.form['name']
        pe = csv.DictReader(open('static/people.csv'))
        img_dir = ''
        val = False
        for x in pe:
            if fo == x['Name']:
                val=True
                img_dir = x['Picture']
        if val:
            return render_template('q1.html',img=img_dir,data="Data found!")
        else:
            return render_template('q1.html',error="error")

@app.route('/q2',methods=['GET','POST'])
def q2():
    return render_template('q2.html')   
 
@app.route('/runq2',methods=['GET','POST'])
def runq2():
    if request.method == 'POST':
        sala = request.form['sal']
        pe = csv.DictReader(open('static/people.csv'))
        data = []
        for x in pe:
            if x['Salary'] == '' or x['Salary'] == ' ':
                x['Salary'] = 99000
            if int(float(x['Salary'])) <= int(float(sala)):
                data.append(x['Picture'])
    return render_template('q2.html',data=data)
        
@app.route("/q3", methods=['GET','POST'])
def q3():
    return render_template('q3.html')
        
@app.route("/runq3", methods=['GET','POST'])
def runq3():
    if request.method == 'POST':
        fo = request.form['name']
        pe = csv.DictReader(open('static/people.csv'))
        output = ''
        for x in pe:
            if fo == x['Name']:
                output = x
                break
        if output != '':
            return render_template('q3.html',output=output,data="Data found!")
        else:
            return render_template('q3.html',error="Record Not Found")

@app.route("/updatedetails",methods=['GET','POST'])
def updatedetails():
    if request.method == 'POST':
        name = request.form['name']
        state = request.form['state']
        salary = request.form['salary']
        grade = request.form['grade']
        room = request.form['room']
        telnum = request.form['telnum']
        picture = request.form['picture']
        keyword = request.form['keyword']
        track = 0
        editval = [name,state,salary,grade,room,telnum,picture,keyword]
        countval = len(editval)
        line = list()
        z=0
        with open('static/people.csv','r') as fo:
            pe = csv.reader(fo)
            for x in pe:
                if name == x[0]:
                    track += 1
                    line.append(editval)
                else:
                    line.append(x)
            output = open('static/people.csv','w')
            for i in line:
                for j in i:
                    z+=1
                    if z < countval:
                        output.write(j + ',')
                    else:
                        output.write(j)
                        z=0
                output.write('\n')
            data = []
            csvfile = csv.DictReader(open('./static/people.csv'))
            for r in csvfile:
                data.append(r)
            if track !=0:
                return render_template('viewcsv.html',data=data,msg="Record has been updated")
            else:
                return render_template('viewcsv.html',error="error")

if __name__ == "__main__":
    app.run(debug=True)
    