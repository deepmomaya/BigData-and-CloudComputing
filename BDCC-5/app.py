from flask import Flask, render_template, request
import re
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SecureSecretKey'

def cleanfile():
    file = open("./static/Story1.txt", "r")
    data = file.read()
    new_data = re.sub('[^a-zA-Z\n]', ' ', data)
    open('./static/Story1_remove.txt', 'w').write(new_data)

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('home.html')

@app.route('/q1', methods=['GET', 'POST'])
def q1():
    return render_template('q1.html')

@app.route('/runq1', methods=['GET', 'POST'])
def runq1():
    key = request.form['key']
    cleanfile()
    with open('./static/Story1_remove.txt', 'r') as fileinput:
        for line in fileinput:
            line = line.lower()
    data = open('./static/Story1_remove.txt', 'rt').read().lower()
    occurrences = data.count(key)
    return render_template('q1.html', msg="Success", count=occurrences)

@app.route('/q2', methods=['GET', 'POST'])
def q2():
    return render_template('q2.html')

@app.route('/runq2', methods=['GET', 'POST'])
def runq2():
    try:
        count = int(float(request.form['c']))
        counts = dict()
        cleanfile()
        file = open("./static/Story1_remove.txt", "rt")
        words = file.read().lower().split()
        for word in words:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
        result = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        i = 0
        final_result = []
        tot_count = 0
        for x in result:
            if(i < count):
                final_result.append(x)
                i += 1
            tot_count += x[1]
        return render_template('q2.html', msg="Success", data=final_result, count=tot_count)
    except Exception as e:
        return render_template('q2.html', error=e)

@app.route('/q3', methods=['GET', 'POST'])
def q3():
    return render_template('q3.html')

@app.route('/runq3', methods=['GET', 'POST'])
def runq3():
    try:
        count = int(float(request.form['c']))
        counts = dict()
        cleanfile()
        file = open("./static/Story1_remove.txt", "rt")
        words = file.read().lower().split()
        for word in words:
            narr = re.findall('..', word)
            for x in narr:
                if(x in counts):
                    counts[x] += 1
                else:
                    counts[x] = 1
        result = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        i = 0
        final_result = []
        tot_count = 0
        for x in result:
            if(i < count):
                final_result.append(x)
                i += 1
            tot_count += x[1]
        return render_template('q3.html', msg="Success", data=final_result, count=tot_count)
    except Exception as e:
        return render_template('q3.html', error=e)

@app.route('/q4', methods=['GET', 'POST'])
def q4():
    return render_template('q4.html')

@app.route('/runq4', methods=['GET', 'POST'])
def runq4():
    try:
        w = request.form['c']
        cleanfile()
        splitw = w.lower().split()
        if len(splitw) != 2:
            return render_template('q4.html', error="Please Enter 2 words")
        counts = dict()
        file = open("./static/Story1_remove.txt", "rt")
        words = file.read().lower().split()
        i = 0
        while i < len(words):
            if i+1 > len(words):
                break
            if words[i] == splitw[0] and words[i+1] == splitw[1]:
                if (words[i], words[i+1]) in counts:
                    counts[(words[i], words[i+1])] += 1
                else:
                    counts[(words[i], words[i+1])] = 1
            i += 1
        return render_template('q4.html', msg="Success", data=counts)
    except Exception as e:
        return render_template('q4.html', error="hi")

@app.route('/q5', methods=['GET', 'POST'])
def q5():
    return render_template('q5.html')

@app.route('/runq5', methods=['GET', 'POST'])
def runq5():
    try:
        txtw = request.form['f']
        replacew = request.form['r']
        with open("./static/Story1_remove.txt", "r") as file:
            filedata = file.read()
        filedata = filedata.replace(txtw, replacew)
        with open('./static/Story1_remove.txt', 'w') as file1:
            file1.write(filedata)
        lines = open("./static/Story1_remove.txt", "r").readlines()
        i = 0
        out = []
        for line in lines:
            if(i < 5):
                out.append(line)
                i += 1
            else:
                break
        return render_template('q5.html', msg="Success", data=out)
    except Exception as e:
        return render_template('q5.html', error="hi")

@app.route('/q6', methods=['GET', 'POST'])
def runq6():
    try:
        cleanfile()
        with open("./static/stop_words.csv", "r") as file:
            stop_words = file.read().split(",")
        with open('./static/Story1_remove.txt', 'r') as file:
            lines = file.readlines()
        out = []
        for line in lines:
            l = ""
            for x in line.split():
                if x not in stop_words:
                    l = l + x + " "
            out.append(l)
        with open('./static/Story1_remove.txt', 'w') as file:
            for x in out:
                file.write(x + "\n")
        lines = open("./static/Story1_remove.txt", "r").readlines()
        i = 0
        out = []
        for line in lines:
            if(i < 5):
                out.append(line)
                i += 1
            else:
                break
        return render_template('q6.html', msg="Success", data=out)
    except Exception as e:
        return render_template('q6.html', error=e)

@app.route('/q7', methods=['GET', 'POST'])
def q7():
    return render_template('q7.html')

@app.route('/runq7', methods=['GET', 'POST'])
def runq7():
    try:
        w = request.form['word']
        c = int(float(request.form['line']))
        cleanfile()
        with open('./static/Story1_remove.txt', 'r') as file:
            lines = file.readlines()
        out = []
        for line in lines:
            if w in str(line):
                out.append(line)
        i = 0
        finalout = []
        for line in out:
            if(i < c):
                finalout.append(line + "\n")
                i += 1
            else:
                break
        return render_template('q7.html', msg="Success", data=finalout)
    except Exception as e:
        return render_template('q7.html', error=e)

@app.route('/q8', methods=['GET', 'POST'])
def q8():
    return render_template('q8.html')

@app.route('/runq8', methods=['GET', 'POST'])
def runq8():
    try:
        fname = request.form['fname']
        content = request.form['content']
        with open('./static/' + fname + '.txt', 'w') as file:
            file.write(content)
        with open('./static/' + fname + '.txt', 'r') as file:
            data = file.read().split()
        count = 0
        for x in data:
            count += 1
        fsize = os.path.getsize("./static/" + fname + ".txt")
        return str(fsize)
        with open('./static/Story1_remove.txt', 'r') as file:
            lines = file.readlines()
        out = []
        for line in lines:
            if w in str(line):
                out.append(line)
        i = 0
        finalout = []
        for line in out:
            if(i < c):
                finalout.append(line + "\n")
                i += 1
            else:
                break
        return render_template('q8.html', msg="File created successfully", data=finalout)
    except Exception as e:
        return render_template('q8.html', error=e)

if __name__ == "__main__":
    app.run(debug=True)
