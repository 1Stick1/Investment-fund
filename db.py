import sqlite3

DB_PATH = 'db/rambad_invest.db'

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def add_user(email, username, password):
    conn = get_connection()
    conn.execute('INSERT INTO users (username, email, password, created_time) VALUES (?, ?, ?, CURRENT_DATE)', (username, email, password))
    conn.commit()
    conn.close()
    
def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return dict(user) if user else None

# def get_all_users():
#     conn = get_connection()
#     users = conn.execute('SELECT * FROM users').fetchall()
#     conn.close()
#     return [dict(u) for u in users]



# def update_user(user_id, username, email, password):
#     conn = get_connection()
#     conn.execute('UPDATE users SET username = ?, email = ?, password = ? WHERE id = ?', (name, email, password, user_id))
#     conn.commit()
#     conn.close()