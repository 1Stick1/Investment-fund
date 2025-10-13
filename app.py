from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
import db
from werkzeug.security import generate_password_hash, check_password_hash
 
import sqlite3
 
from threading import Lock
update_lock = Lock()
 
 
import yfinance as yf
import datetime

from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.secret_key = 'supersecretkey'


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/logout")
def logout():
    session.clear()
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
            return redirect(url_for('customer_panel'))
        else:
            flash('Złe hasło lub login', 'error')
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
            
            flash('Konto zostało pomyślnie stworzone', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError as e:
            if 'UNIQUE constraint failed: users.email' in str(e):
                flash("Ten adres e-mail jest zajęty.", 'error')
            return redirect(url_for('register'))
        except Exception as e:            
            flash("Wystąpił problem. Proszę spróbować ponownie.", 'error')
            return redirect(url_for('register'))
        
    return render_template("register.html")

@app.route('/update_email', methods=['GET', 'POST'])
def update_email():    
    user_id = session['user_id']

    if request.method == 'POST':
        new_email = request.form.get('email').strip()
        
        if not new_email:
            flash("Email nie może być pusty", 'error')
            return redirect(url_for('customer_panel'))

        db.update_user_email(user_id, new_email)
        flash("Adres e-mail został pomyślnie zaktualizowany", 'success')
        session['email'] = new_email
        return redirect(url_for('customer_panel'))

@app.route('/update_username', methods=['GET', 'POST'])
def update_username():
    user_id = session['user_id']

    if request.method == 'POST':
        new_username = request.form.get('username').strip()
        if not new_username:
            flash("Imię nie może być puste", 'error')
            return redirect(url_for('customer_panel'))

        db.update_user_username(user_id, new_username)
        flash("Imię zostało pomyślnie zaktualizowane", 'success')
        session['username'] = new_username
        return redirect(url_for('customer_panel'))


@app.route("/about_us")
def about_us():
    return render_template("about_us.html")

@app.route("/invwestment")
def inwestment():
    return render_template("inwestment.html")



@app.route("/calculator")
def calculator():
    return render_template("calculator.html")



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


















def calculate_portfolio_growth(sp500_change, bund_change):
    return (0.6 * sp500_change) + (0.4 * bund_change)


def update_all_portfolios():
    if not update_lock.acquire(blocking=False):
        return

    try:
        sp500 = yf.Ticker("^GSPC")
        bund = yf.Ticker("^STOXX50E")
        
        sp500_hist = sp500.history(period="1d", interval="1m")
        bund_hist = bund.history(period="1d", interval="1m")
        
        if len(sp500_hist) < 2 or len(bund_hist) < 2:
            return
        
        sp500_change = (sp500_hist['Close'].iloc[-1] / sp500_hist['Close'].iloc[-2]) - 1
        bund_change = (bund_hist['Close'].iloc[-1] / bund_hist['Close'].iloc[-2]) - 1
        
        portfolio_change = calculate_portfolio_growth(sp500_change, bund_change)
        
        if abs(portfolio_change) < 0.000001:
            print("No significant change")
            return
        
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, current_balance FROM investment WHERE current_balance > 0")
        investments = cursor.fetchall()
        
        for inv in investments:
            user_id = inv['user_id']
            old_balance = inv['current_balance']
            new_balance = old_balance * (1 + portfolio_change)
            db.update_investment_balance(user_id, new_balance)
        
        conn.close()
        print(f"Portfolios updated. Change: {portfolio_change*100:.4f}%")
        
    except Exception as e:
        print(f"Error updating portfolios: {e}")
    finally:
        update_lock.release()


@app.route('/invest', methods=['POST'])
def invest():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        amount = float(request.form.get('amount', 0))
        if amount <= 0:
            flash('Сумма должна быть положительной', 'error')
            return redirect(url_for('customer_panel'))
        
        new_balance = db.invest_money(session['user_id'], amount)
        flash(f'Инвестировано ${amount:.2f}. Новый баланс: ${new_balance:.2f}', 'success')
        
    except Exception as e:
        flash(f'Ошибка: {str(e)}', 'error')
    
    return redirect(url_for('customer_panel'))


@app.route('/withdraw', methods=['POST'])
def withdraw():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        amount = float(request.form.get('amount', 0))
        if amount <= 0:
            flash('Сумма должна быть положительной', 'error')
            return redirect(url_for('customer_panel'))
        
        new_balance = db.withdraw_money(session['user_id'], amount)
        flash(f'Выведено ${amount:.2f}. Новый баланс: ${new_balance:.2f}', 'success')
        
    except ValueError as e:
        flash(str(e), 'error')
    except Exception as e:
        flash(f'Ошибка: {str(e)}', 'error')
    
    return redirect(url_for('customer_panel'))




# Обновленный customer_panel
@app.route("/customer_panel")
def customer_panel():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    investment = db.get_or_create_investment(session['user_id'])
    transactions = db.get_user_transactions(session['user_id'])
    
    return render_template(
        "customer-panel.html", 
        username=username,
        investment=investment,
        transactions=transactions
    )



scheduler = BackgroundScheduler()
scheduler.add_job(func=update_all_portfolios, trigger="interval", seconds=10)  # Каждый час
scheduler.start()




if __name__ == "__main__":
    app.run(debug=True)














