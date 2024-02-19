import click
from flask import Flask, jsonify, request, render_template
import peewee
from flask.cli import with_appcontext

db = peewee.SqliteDatabase('people.db')
@click.command("init-db")
@with_appcontext
def init_db_command():
    database = peewee.SqliteDatabase('people.db')
    database.create_tables([ShoppingRow])
    print("Initialized the database.")

class ShoppingRow(peewee.Model):
    name = peewee.CharField()
    price = peewee.FloatField()
    quantity = peewee.IntegerField()

    class Meta:
        database = db


app = Flask(__name__)
app.cli.add_command(init_db_command)

@app.route("/")
def all_product():
    return render_template("index.html", shopping_list=ShoppingRow.select())


@app.route("/new", methods=["POST"])
def new_product():
    if "name" in request.form and "price" in request.form and "quantity" in request.form:
        ShoppingRow.create(name=request.form['name'], price=int(request.form['price']),
                                          quantity=int(request.form["quantity"]))
        return render_template("index.html", shopping_list=ShoppingRow.select())
    else:
        return "Il manque des données dans le json", 400


@app.route("/delete/<int:identifier>", methods=["GET"])
def get_by_id(identifier: int):
    shopping_row = ShoppingRow.get_or_none(ShoppingRow.id == identifier)
    if not shopping_row:
        return "Il n'existe pas"
    shopping_row.delete_instance()
    return render_template("index.html", shopping_list=ShoppingRow.select())






