import pymongo
import configparser
confs = configparser.ConfigParser()


confs.read("app.conf")


db_url = confs.get("general","connect")


client = pymongo.MongoClient(db_url)
db = client.test
