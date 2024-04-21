from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecureSecretKey'

socketio = SocketIO(app)

pile1 = 0
pile2 = 0
pile3 = 0
maxs = 0
mins = 0

@app.route('/listuser', methods=["GET", "POST"])
def listuser():
    return render_template('listu.html')

@socketio.on('listu')
def on_listu():
    print("Hi")

@socketio.on('my event')
def my_event(json):
    print('received json: ' + str(json))

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', to=room)

@socketio.on('next_turn')
def on_next_turn(id):
    socketio.emit('turn_next', id)

@socketio.on('setvar')
def on_setvar(data):
    global pile1, pile2, pile3, maxs, mins
    room = data["room"]
    join_room(room)
    pile1 = data["pile1"]
    pile2 = data["pile2"]
    pile3 = data["pile3"]
    maxs = data["maxs"]
    mins = data["mins"]
    room = data["room"]
    e = f"Pile 1:{pile1}\nPile 2: {pile2}\nPile 3:{pile3}"
    socketio.emit('score1', e)
    join_room(room)
    send('Variables set', to=room)

@socketio.on('score')
def on_score(data):
    global pile1, pile2, pile3, maxs, mins
    pnum = int(float(data['pnum']))
    pstone = int(float(data['pstone']))
    pname = data['pname']
    e = "Hi"
    if pstone > int(float(maxs)) or pstone < int(float(mins)):
        e = f"Stone to reduce should be between {mins} and {maxs}"  
        send(e, to="game1")  
    else:
        match pnum:
            case 1:
                pile1 = int(float(pile1)) - pstone
            case 2:
                pile2 = int(float(pile2)) - pstone
            case 3:
                pile3 = int(float(pile3)) - pstone
            
        e = f"Pile 1:{pile1}\nPile 2: {pile2}\nPile 3:{pile3}{request.sid}"
        msg = f"{pname} removed {pstone} stones from Pile {pnum}"
        socketio.emit('score1', e)
        send(msg, to="game1")

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', to=room)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('home.html')

@app.route("/task", methods=["GET", "POST"])
def task():
    return render_template('task.html')

@app.route("/runtask", methods=["GET", "POST"])
def runtask():
    global pile1, pile2, pile3, maxs, mins
    pile1 = int(float(request.form["pile1"]))
    pile2 = int(float(request.form["pile2"]))
    pile3 = int(float(request.form["pile3"]))
    maxs = int(float(request.form["maxs"]))
    mins = int(float(request.form["mins"]))
    e = f"Pile 1:{pile1}\nPile 2: {pile2}\nPile 3:{pile3}"
    socketio.emit('score1', e)
    return render_template('task.html')

@app.route("/player1", methods=["GET", "POST"])
def player1():
    return render_template('player1.html', pile1=pile1, pile2=pile2, pile3=pile3, maxs=maxs, mins=mins)

@app.route("/setplayer1", methods=["GET", "POST"])
def setplayer1():
    return render_template('player1.html')

@app.route("/player2", methods=["GET", "POST"])
def player2():
    return render_template('player2.html')

if __name__ == '__main__':
    socketio.run(app)
