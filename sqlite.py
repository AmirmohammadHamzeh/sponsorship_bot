import sqlite3

def init_db():
    conn = sqlite3.connect('customer.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer (
            user_id INTEGER PRIMARY KEY,
            is_member_of_channels BOOLEAN DEFAULT FALSE
        )
    ''')
    conn.commit()
    return conn, cursor

def add_user(user_id):
    conn, cursor = init_db()
    cursor.execute('SELECT * FROM customer WHERE user_id = ?', (user_id,))
    existing_user = cursor.fetchone()

    if not existing_user:
        cursor.execute('INSERT INTO customer (user_id) VALUES (?)', (user_id,))
        conn.commit()
        new_user_added = True
    else:
        new_user_added = False

    conn.close()
    return new_user_added

def update_membership_status(user_id, is_member):
    conn, cursor = init_db()
    cursor.execute('UPDATE customer SET is_member_of_channels = ? WHERE user_id = ?', (is_member, user_id))
    conn.commit()
    conn.close()