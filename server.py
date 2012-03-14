# Christopher Triolo
# Princeton University
#
# server.py

from flask import Flask, request, abort, redirect, url_for, jsonify
import pymongo
from pymongo import Connection
from pymongo.objectid import ObjectId
from bson.errors import InvalidId

connection = Connection('localhost', 27017)
db = connection.getmehere

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/product", methods=['GET', 'POST', 'PUT', 'DELETE'])
def product():
    if request.method == 'GET':
        if 'id' in request.args:
            try: product = db.products.find_one({"_id":ObjectId(request.args['id'])})
            except InvalidId: return jsonify(response=[])
            if (product is None): return jsonify(response=[])
            product['_id'] = str(product['_id'])
            return jsonify(response=[product])
        elif 'name' in request.args:
            product = db.products.find_one({"name":request.args['name']})
            if (product is None): return jsonify(response=[])
            product['_id'] = str(product['_id'])
            return jsonify(response=[product])
        elif 'prefix' in request.args:
            products = []
            for product in db.products.find({"name":{"$regex":"^" + request.args['prefix'] + ".*"}}):
                product['_id'] = str(product['_id'])
                products.append(product);
            return jsonify(response=products)
        else:
            products = []
            for product in db.products.find():
                product['_id'] = str(product['_id'])
                products.append(product);
            return jsonify(response=products)
    elif request.method == 'POST':
        if (request.json is None): return jsonify(error="POST data is not JSON.")
        db.products.insert(request.json, manipulate=True)
        request.json['_id'] = str(request.json['_id'])
        return jsonify(request.json)
    elif request.method == 'PUT':
        if (request.json is None): return jsonify(error="PUT data is not JSON.")
        request.json['_id'] = ObjectId(request.json['_id'])
        db.products.save(request.json, manipulate=True)
        request.json['_id'] = str(request.json['_id'])
        return jsonify(request.json)
    elif request.method == 'DELETE':
        if 'id' in request.args:
            try: db.products.remove({"_id":ObjectId(request.args['id'])})
            except InvalidId: return jsonify(response=[])
            return jsonify(response="ok")
        elif 'name' in request.args:
            db.products.remove({"name":request.args['name']})
            return jsonify(response="ok")
        return jsonify(error="No parameters.");
    return jsonify(error="This should never happen.")

if __name__ == "__main__":
    app.run(debug=True)
