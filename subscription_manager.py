# === subscription_manager.py ===

import sqlite3
from datetime import datetime, timedelta

DB_FILE = 'users.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            telegram_id INTEGER PRIMARY KEY,
            free_attempts INTEGER DEFAULT 5,
            plan TEXT DEFAULT 'free',
            plan_expiry TEXT,
            remaining INTEGER DEFAULT 5
        )
    ''')
    conn.commit()
    conn.close()

def get_user(telegram_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
    user = c.fetchone()
    conn.close()
    return user

def register_user(telegram_id):
    if not get_user(telegram_id):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''
            INSERT INTO users (telegram_id, free_attempts, plan, plan_expiry, remaining)
            VALUES (?, 5, 'free', NULL, 5)
        ''', (telegram_id,))
        conn.commit()
        conn.close()

def can_use_bot(telegram_id):
    user = get_user(telegram_id)
    if user:
        telegram_id, free_attempts, plan, plan_expiry, remaining = user

        # Check if user has a paid plan and if it has expired
        if plan != 'free' and plan_expiry:
            if datetime.strptime(plan_expiry, "%Y-%m-%d") < datetime.now():
                # Plan expired - downgrade to free
                update_plan(telegram_id, 'free', None)
                update_remaining(telegram_id, free_attempts)
                return free_attempts > 0

            return remaining > 0  # Plan still active
        else:
            return remaining > 0  # Free plan with remaining attempts

    return False  # User doesn't exist

def decrement_attempt(telegram_id):
    user = get_user(telegram_id)
    if user:
        remaining = user[4]
        if remaining > 0:
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute('UPDATE users SET remaining = ? WHERE telegram_id = ?', (remaining - 1, telegram_id))
            conn.commit()
            conn.close()

def update_remaining(telegram_id, value):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('UPDATE users SET remaining = ? WHERE telegram_id = ?', (value, telegram_id))
    conn.commit()
    conn.close()

def update_plan(telegram_id, plan, expiry):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('UPDATE users SET plan = ?, plan_expiry = ? WHERE telegram_id = ?', (plan, expiry, telegram_id))
    conn.commit()
    conn.close()

def activate_plan(telegram_id, plan_type):
    duration_map = {
        "daily": 1,
        "monthly": 30,
        "yearly": 365
    }

    if plan_type not in duration_map:
        return False

    days = duration_map[plan_type]
    expiry_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

    update_plan(telegram_id, plan_type, expiry_date)
    update_remaining(telegram_id, 999)  # Effectively unlimited usage for paid plans

    return True
