# xuser
# b9kgZC2zJB8iyBk
from logger import logging
from flask import Flask
import pymongo
from faker import Faker
import configparser
from bson.json_util import dumps
import random




app = Flask(__name__)
confs = configparser.ConfigParser()
fake = Faker()


confs.read("app.conf")



db_url = confs.get("general","connect")
db_str = confs.get("dbdetails","dbname")
table_name = confs.get('dbdetails','collection')
logging.info(f"\nconnection:{db_url}\ndatabase:{db_str}\ntable:{table_name}")

try:
    client = pymongo.MongoClient(db_url)
    db = client[db_str]
    usersTable = db[table_name]
    logging.info(client.server_info()) 
    logging.info("connected to mongo") 
except pymongo.errors.ServerSelectionTimeoutError as err:
    logging.error(err)
    print(err)


@app.route("/", methods=["POST","GET"])
def home():
    return "Hello!"

@app.route("/read/<string:name>", methods=["POST","GET"])
def read_data(name: str):
    user = usersTable.find_one({'name':name})
    logging.info(f"data from mongo:{user}")
    return dumps(user)

@app.route("/write", methods=["POST","GET"], defaults={"name": fake.name(), 'age': random.randint(12,90)})
@app.route("/write/<string:name>/<int:age>", methods=["POST","GET"], defaults={"name": fake.name(), 'age': random.randint(12,90)})
def write_data(name, age):
    data = {
        'name':name,
        'age':age,
    }
    try:
        usersTable.insert_one(data)
        logging.info(f"inserted {name}:{age} to mongo.")
        return f"inserted {name}:{age} to mongo."
    except: 
        logging.info(f"data '{name}:{age}' can't be written to mongo.")
        return f"data '{name}:{age}' can't be written to mongo."


if __name__ == "__main__":
    app.run(debug=True)


# MySql -> Mongo
# Database -> Database
# Table -> Collection
# Row -> Document
# Index -> Index
