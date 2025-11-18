from flask import Flask, request
import sqlite3

app = Flask(__name__)

# Function to insert a user into the database
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

@app.route("/")
def index():
    return "Server is running! Use /add_user?name=YourName"

if __name__ == "__main__":
    app.run(debug=True)
