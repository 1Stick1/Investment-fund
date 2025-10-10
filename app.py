from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
import db
from werkzeug.security import generate_password_hash, check_password_hash

import yfinance as yf
import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/logout")
def logout():
    session.clear()
    flash('Вы вышли из аккаунта', 'success')
    return redirect(url_for('index'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = db.get_user_by_email(email)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            flash('Correct', 'succes')
            return redirect(url_for('customer_panel'))
        else:
            flash('Not Correct', 'error')
            return redirect(url_for("login"))
        
    return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        
        hashed_password = generate_password_hash(password)
        try:
            db.add_user(email, username, hashed_password)
            return redirect(url_for('index'))
        except Exception as e:
            return redirect(url_for('register'))
    
    return render_template("register.html")

@app.route('/update_email', methods=['GET', 'POST'])
def update_email():
    if 'user_id' not in session:
        flash("Пожалуйста, войдите в систему")
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        new_email = request.form.get('email').strip()
        
        if not new_email:
            flash("Email nie może być pusty")
            return redirect(url_for('update_email'))

        db.update_user_email(user_id, new_email)
        flash("Adres e-mail został pomyślnie zaktualizowany")
        return redirect(url_for('customer_panel'))

@app.route('/update_username', methods=['GET', 'POST'])
def update_username():
    user_id = session['user_id']

    if request.method == 'POST':
        new_username = request.form.get('username').strip()
        
        if not new_username:
            flash("Imię nie może być puste")
            return redirect(url_for('update_username'))

        db.update_user_username(user_id, new_username)
        flash("Imię zostało pomyślnie zaktualizowane")
        session['username'] = new_username
        return redirect(url_for('customer_panel'))


@app.route("/about_us")
def about_us():
    return render_template("about_us.html")

@app.route("/invwestment")
def inwestment():
    return render_template("inwestment.html")


@app.route("/customer_panel")
def customer_panel():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    username = session['username']
    return render_template("customer-panel.html", username=username)


# @app.route("/data")
# def data():
#     # Добавляем новую точку
#     now = datetime.datetime.now().strftime("%H:%M:%S")
#     value = random.randint(1000, 5000)
#     data_points.append({"time": now, "value": value})
    
#     # Оставляем только последние 10 точек
#     if len(data_points) > 10:
#         data_points.pop(0)
    
#     return jsonify(data_points)


def load_initial_data():
    usa_stock = yf.Ticker("^GSPC")
    eu_bonds = yf.Ticker("^STOXX50E")

    usa_hist = usa_stock.history(period="70d", interval="1h")
    eu_hist = eu_bonds.history(period="70d", interval="1h")

    if usa_hist.empty or eu_hist.empty:
        return []

    points = []
    for (time, usa_row), (_, eu_row) in zip(usa_hist.iterrows(), eu_hist.iterrows()):
        points.append({
            "time": time.strftime("%d %b %H:%M"),
            "usa": round(float(usa_row["Close"]), 2),
            "eu": round(float(eu_row["Close"]), 2)
        })

    return points

data_points = load_initial_data()


@app.route("/data")
def data():
    usa_stock = yf.Ticker("^GSPC")  
    eu_bonds = yf.Ticker("^STOXX50E")   

    usa_hist = usa_stock.history(period="7d", interval="5m")
    eu_hist = eu_bonds.history(period="7d", interval="5m")

    if usa_hist.empty or eu_hist.empty:
        return jsonify({"error": "No data available"}), 500
    print("USA history:")
    print(usa_hist.tail())
    print("EU history:")
    print(eu_hist.tail())

    usa_price = usa_hist["Close"].iloc[-1]
    eu_price = eu_hist["Close"].iloc[-1]

    now = datetime.datetime.now().strftime("%d %b %H:%M")
    data_points.append({
        "time": now,
        "usa": round(float(usa_price), 2),
        "eu": round(float(eu_price), 2)
    })

    if len(data_points) > 1000:
        data_points.pop(0)

    return jsonify(data_points)

if __name__ == "__main__":
    app.run(debug=True)
