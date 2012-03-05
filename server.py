# Christopher Triolo
# Princeton University
#
# server.py

from flask import Flask
from flask import jsonify
import pymongo
from pymongo import Connection

connection = Connection('localhost', 27017)
db = connection.getmehere

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/product/<query>")
def get_products(query):
    matches = []
    for product in db.products.find({"name":{"$regex":"^" + query + ".*"}}):
        product['_id'] = str(product['_id'])
        matches.append(product); #{'name': str(product[u'name'])})
    products = {"count" : len(matches), "rows" : matches}
    return jsonify(products)

if __name__ == "__main__":
    app.run(debug=True)
