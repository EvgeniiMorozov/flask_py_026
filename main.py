from sqlite3 import connect

from flask import Flask, render_template, request


app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/users", methods=["GET", "POST"])
def add_user():
    conn = connect("shop.sqlite")
    cursor = conn.cursor()

    if request.method == "POST":
        data = {
            "name": str(request.form.get("name")),
            "email": str(request.form.get("email")),
            "phone": str(request.form.get("phone")),
        }

        # print(
        #     f"INSERT INTO customer (name, phone, email) "
        #     f"VALUES (\"{data['name']}\", \"{data['phone']}\", \"{data['email']}\")"
        # )

        cursor.execute(
            f"INSERT INTO customer (name, phone, email) VALUES (\"{data['name']}\", \"{data['phone']}\", \"{data['email']}\")"
        )
        conn.commit()

        return render_template("users.html", **data)

    return render_template("users.html")


if __name__ == "__main__":
    app.run(debug=True)
