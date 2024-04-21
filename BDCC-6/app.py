from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecureSecretKey'

valid_form = {}
invalid_characters = ['/', '*', '#']

@app.route("/", methods=['GET', 'POST'])
def main():
    try:
        conn = connection()
        cursor = conn.cursor()
        return render_template('home.html')
    except Exception as e:
        return render_template('home.html', error=e)

@app.route('/q1', methods=['GET', 'POST'])
def q1():
    return render_template('q1.html')

@app.route('/runq1', methods=['POST'])
def runq1():
    password = request.form['password']
    is_valid = check_validity(password)
    if is_valid:
        return 'Valid'
    else:
        return 'NotValid'

def check_validity(password):
    if len(password) < valid_form['L']:
        return False

    if not any(char.isdigit() for char in password):
        return False

    if not any(char.isupper() for char in password):
        return False

    invalid_chars = invalid_characters + valid_form['IV']
    if any(char in invalid_chars for char in password):
        return False

    return True

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        valid_form['L'] = int(request.form['length'])
        valid_form['IV'] = list(request.form['additional_chars'])
        return 'Form VF submitted successfully!'
    else:
        return render_template('admin.html')

@app.route('/q2', methods=['GET', 'POST'])
def q2():
    return render_template('q2.html')

@app.route('/runq2', methods=['POST'])
def validate_text():
    text = request.form['text']
    m = int(request.form['m'])
    x = int(request.form['x'])
    p = int(request.form['p'])
    l = int(request.form['l'])

    is_valid, invalid_sentences, invalid_words = validate_text_content(text, m, x, p, l)

    if is_valid:
        return 'Valid'
    else:
        error_message = 'Invalid:'

        if invalid_sentences:
            error_message += ' The following sentences have issues: ' + ', '.join(invalid_sentences) + '.'

        if invalid_words:
            error_message += ' The following words exceed the maximum length: ' + ', '.join(invalid_words) + '.'

        return error_message

def validate_text_content(text, m, x, p, l):
    sentences = text.split('.')
    is_valid = True
    invalid_sentences = []
    invalid_words = []

    for sentence in sentences:
        sentence = sentence.strip()

        if not m <= len(sentence.split()) <= x:
            is_valid = False
            invalid_sentences.append(sentence)

        if not (sentence[0].isupper() and sentence[-1] in ['?', '!', '.']):
            is_valid = False
            invalid_sentences.append(sentence)

        words = sentence.split()
        for word in words:
            if len(word) > l:
                is_valid = False
                invalid_words.append(word)

        parts = sentence.split(',')
        for part in parts:
            if len(part.split()) > p:
                is_valid = False
                invalid_sentences.append(part)

    return is_valid, invalid_sentences, invalid_words

@app.route('/q3', methods=['GET', 'POST'])
def q3():
    return render_template('q3.html')

@app.route('/runq3', methods=['POST'])
def censor_text():
    text = request.form['text']
    banned_words = [word.lower() for word in request.form.getlist('banned_words')]
    banned_phrases = [phrase.lower() for phrase in request.form.getlist('banned_phrases')]
    max_banned = int(request.form['max_banned'])

    cleaned_text, alert_message = censor_text_content(text, banned_words, banned_phrases, max_banned)

    return render_template('censored.html', cleaned_text=cleaned_text, alert_message=alert_message)

def censor_text_content(text, banned_words, banned_phrases, max_banned):
    cleaned_text = text.lower()
    alert_message = ""

    for word in banned_words:
        cleaned_text = cleaned_text.replace(word, "")

    for phrase in banned_phrases:
        cleaned_text = cleaned_text.replace(phrase, "")

    cleaned_text = cleaned_text.translate(str.maketrans("", "", ".,!?"))

    cleaned_text = " ".join(cleaned_text.split())

    num_banned = len(banned_words) + len(banned_phrases)
    if num_banned > max_banned:
        alert_message = "Alert: Number of banned words/phrases exceeds the maximum limit. Please call the authorities."

    return cleaned_text, alert_message

if __name__ == "__main__":
    app.run(debug=True)
