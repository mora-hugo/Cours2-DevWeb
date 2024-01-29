from flask import Flask, jsonify, request


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

@app.route("/", methods=["GET", "PUT"])
def hello_world():
    if request.method == "GET":
        return get_product()
    else:
        if request.is_json == False:
            return "Erreur dans le json", 422
        else:
            data = request.get_json()
            if "name" in data and "price" in data and "quantity" in data:
                shopping_list.append(ShoppingRow(data['name'], int(data['price']), int(data["quantity"])))
                return get_product()
            else:
                return "Il manque des données dans le json", 400


@app.route("/<int:identifier>", methods=["PATCH", "DELETE"])
def get_by_id(identifier : int):
    if request.method == "DELETE":
        if identifier < len(shopping_list) and identifier >= 0:
            del shopping_list[identifier]
            return get_product()
    elif request.method == "PATCH":
        if request.is_json == False:
            return "Erreur dans le json", 422
        if identifier >= len(shopping_list) or identifier < 0:
            return "Existe pas", 404
        data = request.get_json()
        shopping_row : ShoppingRow = shopping_list[identifier]
        if "name" in data:
            shopping_row.name = data["name"]
        if "price" in data:
            shopping_row.price = data["price"]
        if "quantity" in data:
            shopping_row.quantity = data["quantity"]
        return get_product()



