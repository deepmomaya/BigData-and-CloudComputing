from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecureSecretKey'

inventory = []
purchases = {}

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/gs", methods=["GET", "POST"])
def grocery_store_admin():
    global purchases
    if request.method == "GET":
        return render_template('gs.html', inventory=inventory, purchases=purchases)
    elif request.method == "POST":
        if "add_item" in request.form:
            item_name = request.form["item_name"]
            if item_name not in inventory:
                inventory.append(item_name)
        elif "remove_item" in request.form:
            item_name = request.form["remove_item"]
            if item_name in inventory:
                inventory.remove(item_name)
        return redirect(url_for("grocery_store_admin"))

@app.route("/shopper1", methods=["GET", "POST"])
def shopper1():
    global purchases
    if request.method == "GET":
        return render_template('shopper1.html', inventory=inventory)
    elif request.method == "POST":
        shopper_name = "Shopper 1"
        selected_item = request.form["selected_item"]
        if selected_item in inventory:
            inventory.remove(selected_item)
            purchases[selected_item] = shopper_name
            purchase_success_message = f"You have successfully purchased {selected_item}."
            return render_template('shopper1.html', inventory=inventory, purchase_success=purchase_success_message)
    return redirect(url_for("shopper1"))

@app.route("/shopper2", methods=["GET", "POST"])
def shopper2():
    global purchases
    if request.method == "GET":
        return render_template('shopper2.html', inventory=inventory)
    elif request.method == "POST":
        shopper_name = "Shopper 2"
        selected_item = request.form["selected_item"]
        if selected_item in inventory:
            inventory.remove(selected_item)
            purchases[selected_item] = shopper_name
            purchase_success_message = f"You have successfully purchased {selected_item}."
            return render_template('shopper2.html', inventory=inventory, purchase_success=purchase_success_message)
    return redirect(url_for("shopper2"))

if __name__ == "__main__":
    app.run(debug=True)
