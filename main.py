from flask import Flask, jsonify, request, render_template


class ShoppingRow:
    def __init__(self, product_name: str = "Nom du produit", price: float = 1, quantity: int = 1):
        self.name = product_name
        self.price = price
        self.quantity = quantity

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity
        }


shopping_list : list[ShoppingRow] = list()
shopping_list.append(ShoppingRow(price=1))
shopping_list.append(ShoppingRow("Lait", 3, 1))


app = Flask(__name__)


def get_product():
    dictionnary = list()
    for row in shopping_list:
        dictionnary.append(row.to_dict())
    return jsonify(dictionnary)

@app.route("/")
def all_product():
    return render_template("index.html", shopping_list=shopping_list)

@app.route("/new", methods=["POST"])
def new_product():
    if "name" in request.form and "price" in request.form and "quantity" in request.form:
        shopping_list.append(ShoppingRow(request.form['name'], int(request.form['price']), int(request.form["quantity"])))
        return render_template("index.html", shopping_list=shopping_list)
    else:
        return "Il manque des données dans le json", 400


@app.route("/delete/<int:identifier>", methods=["GET"])
def get_by_id(identifier : int):
    if identifier < len(shopping_list) and identifier >= 0:
        del shopping_list[identifier]
        return render_template("index.html", shopping_list=shopping_list)



