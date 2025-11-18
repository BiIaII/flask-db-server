from flask import Flask, request, render_template_string
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


@app.route("/add_user_form", methods=["POST"])
def add_user_form():
    username = request.form.get("username")

    if not username:
        return "No username provided.", 400

    add_user_to_db(username)
    return "User added from form! <br><a href='/'>Back</a>"

@app.route("/show_users", methods=["GET"])
def show_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users")
    rows = cursor.fetchall()
    conn.close()

    html = "<h1>Users</h1><ul>"
    for row in rows:
        html += f"<li>{row[0]} - {row[1]}</li>"
    html += "</ul><a href='/'>Back</a>"

    return html



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

@app.route("/", methods=["GET"])
def index():
    html = """
    <html>
        <head>
            <title>User Database</title>
        </head>
        <body>
            <h1>User Database</h1>

            <h2>Add a user</h2>
            <form action="/add_user_form" method="post">
                <input type="text" name="username" placeholder="Enter username" required>
                <button type="submit">Add user</button>
            </form>

            <h2>Show all users</h2>
            <form action="/show_users" method="get">
                <button type="submit">Show users</button>
            </form>
        </body>
    </html>
    """
    return render_template_string(html)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
