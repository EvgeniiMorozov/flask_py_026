from sqlite3 import connect

from flask import Flask, render_template, request


app = Flask(__name__, template_folder="templates")


# conn = connect("shop.sqlite", isolation_level=None)
# cursor = conn.cursor()
# conn.close


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
        conn.close()
        return render_template("users.html", **data)

    return render_template("users.html")


@app.route("/product", methods=["GET", "POST"])
def add_product():
    conn = connect("shop.sqlite")
    cursor = conn.cursor()

    if request.method == "POST":
        data = {
            "name": str(request.form.get("name")),
            "description": str(request.form.get("description")),
            "price": str(request.form.get("price")),
        }
        # create_record(data)
        # print(f"INSERT INTO product (name, description, price) VALUES (\"{data['name']}\", \"{data['description']}\", \"{data['price']}\")")
        cursor.execute(
            f"INSERT INTO product (name, description, price) VALUES (\"{data['name']}\", \"{data['description']}\", \"{data['price']}\")"
        )
        conn.commit()
        conn.close()
        return render_template("add_product.html", **data)

    return render_template("add_product.html")


# def create_record(data, cursor=cursor):
#     """
#     Создаём запись в БД
#     """
#     cursor.execute(
#         f"INSERT INTO product (name, description, price) VALUES (\"{data['name']}\", \"{data['description']}\", \"{data['price']}\")"
#     )


@app.route("/ajax_product", methods=["GET", "POST"])
def ajax_html():
    # request_data = request.args.get("text")
    requested_name = request.args.get("name")
    requested_description = request.args.get("description")
    requested_price = request.args.get("price")
    requested_customer = request.args.get("customer")
    requested_product = request.args.get("product")
    # print(requested_name, requested_description, requested_price)
    print(requested_customer, requested_product)
    # if request_data == "Текст":
    #     request_data += " test"
    #     return {"text": request_data}
    if requested_name and requested_description and requested_price != None:
        conn = connect("shop.sqlite")
        cursor = conn.cursor()
        cursor.execute(
            f'INSERT INTO product (name, description, price) VALUES ("{requested_name}", "{requested_description}", "{requested_price}")'
        )
        conn.commit()
        conn.close()
        return "Success"

    if requested_product and requested_customer != None:
        pass

    return "Not success"


def get_users_from_db():
    conn = connect("shop.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM customer")
    result = cursor.fetchall()
    print(result)
    conn.commit()
    conn.close()
    return result


def get_products_from_db():
    conn = connect("shop.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM product")
    result = cursor.fetchall()
    print(result)
    conn.commit()
    conn.close()
    return result


@app.route("/shop", methods=["GET", "POST"])
def products_and_customers():
    cust = get_users_from_db()
    prod = get_products_from_db()
    data = {"customers": cust, "products": prod}
    return render_template("shop.html", **data)


if __name__ == "__main__":
    get_users_from_db()
    app.run(debug=True)
