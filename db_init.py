# Christopher Triolo
# Princeton University
#
# db_init.py

import pymongo
from pymongo import Connection

connection = Connection('localhost', 27017)
db = connection.getmehere

init_product_names = ["apples",
                      "bananas",
                      "berries",
                      "grapes",
                      "lemons",
                      "limes",
                      "melons",
                      "nectarines",
                      "oranges",
                      "peaches",
                      "peanuts",
                      "pears",
                      "peas",
                      "plums",
                      "strawberries",
                      "watermelon"]

init_products = []
for product_name in init_product_names:
    init_products.append({"name": product_name})
db.products.insert(init_products)
