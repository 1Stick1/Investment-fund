import sqlite3

DB_PATH = 'db/rambad_invest.db'

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def add_user(email, username, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, email, password, created_time) VALUES (?, ?, ?, CURRENT_DATE)', (username, email, password))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
    
def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return dict(user) if user else None


def update_user_email(user_id, email):
    conn = get_connection()
    print(email)
    print(user_id)
    conn.execute('UPDATE users SET email = ? WHERE id = ?', (email, user_id))
    conn.commit()
    conn.close()
    
def update_user_username(user_id, username):
    conn = get_connection()
    conn.execute('UPDATE users SET username = ? WHERE id = ?', (username, user_id))
    conn.commit()
    conn.close()  
def get_or_create_investment(user_id):
    """Получить или создать инвестиционный аккаунт"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM investment WHERE user_id = ?", (user_id,))
    inv = cursor.fetchone()
    
    if not inv:
        cursor.execute(
            "INSERT INTO investment (user_id, total_invested, current_balance) VALUES (?, 0, 0)",
            (user_id,)
        )
        conn.commit()
        cursor.execute("SELECT * FROM investment WHERE user_id = ?", (user_id,))
        inv = cursor.fetchone()
    
    conn.close()
    return dict(inv) if inv else None


def add_transaction(user_id, trans_type, amount, balance_after):
    """Добавить транзакцию"""
    conn = get_connection()
    conn.execute(
        "INSERT INTO transactions(user_id, type, amount, balance_after) VALUES (?, ?, ?, ?)",
        (user_id, trans_type, amount, balance_after)
    )
    conn.commit()
    conn.close()


def update_investment_balance(user_id, new_balance):
    """Обновить баланс портфеля"""
    conn = get_connection()
    conn.execute(
        "UPDATE investment SET current_balance = ?, last_update = CURRENT_TIMESTAMP WHERE user_id = ?",
        (new_balance, user_id)
    )
    conn.commit()
    conn.close()


def invest_money(user_id, amount):
    """Инвестировать деньги"""
    inv = get_or_create_investment(user_id)
    new_balance = inv['current_balance'] + amount
    new_total = inv['total_invested'] + amount
    
    conn = get_connection()
    conn.execute(
        "UPDATE investment SET current_balance = ?, total_invested = ?, last_update = CURRENT_TIMESTAMP WHERE user_id = ?",
        (new_balance, new_total, user_id)
    )
    conn.commit()
    conn.close()
    
    add_transaction(user_id, 'invest', amount, new_balance)
    return new_balance


def withdraw_money(user_id, amount):
    """Вывести деньги"""
    inv = get_or_create_investment(user_id)
    
    if inv['current_balance'] < amount:
        raise ValueError("Niewystarczające środki")
    
    new_balance = inv['current_balance'] - amount
    new_total = inv['total_invested'] - amount 
    
    conn = get_connection()
    conn.execute(
        "UPDATE investment SET current_balance = ?, total_invested = ?, last_update = CURRENT_TIMESTAMP WHERE user_id = ?",
        (new_balance, new_total, user_id)  
    )
    conn.commit()
    conn.close()
    
    add_transaction(user_id, 'withdraw', amount, new_balance)
    return new_balance

def get_user_transactions(user_id, limit=20):
    """Получить историю транзакций"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM transactions WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
        (user_id, limit)
    )
    transactions = cursor.fetchall()
    conn.close()
    return [dict(t) for t in transactions]