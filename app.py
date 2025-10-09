from flask import Flask, render_template, jsonify
import yfinance as yf
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/registration")
def registration():
    return render_template("registration.html")

@app.route("/about_us")
def about_us():
    return render_template("about_us.html")


@app.route("/customer_panel")
def customer_panel():
    return render_template("customer-panel.html")


@app.route("/data")
def data():
    # Добавляем новую точку
    now = datetime.datetime.now().strftime("%H:%M:%S")
    value = random.randint(1000, 5000)
    data_points.append({"time": now, "value": value})
    
    # Оставляем только последние 10 точек
    if len(data_points) > 10:
        data_points.pop(0)
    
    return jsonify(data_points)


if __name__ == "__main__":
    app.run(debug=True)
