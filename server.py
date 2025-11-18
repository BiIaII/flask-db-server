from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

def add_user_to_db(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
    conn.commit()
    conn.close()

@app.route("/add_user")
def add_user():
    username = request.args.get("name")

    if not username:
        return "Error: no name provided. Use /add_user?name=Bilal"

    add_user_to_db(username)
    return f"User '{username}' added successfully!"

@app.route("/get_users")
def get_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users")
    rows = cursor.fetchall()
    conn.close()

    result = ""
    for row in rows:
        result += f"{row[0]} - {row[1]}\n"

    return f"Users:\n{result}"

@app.route("/")
def index():
    return "Server is running online! Use /add_user?name=YourName"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
