from decouple import config
from bson import ObjectId
from pymongo import MongoClient
import pandas as pd


MONGO_DETAILS = config('MONGO_DETAILS')
port = 8000
client = MongoClient(MONGO_DETAILS, port)
db = client["DataTerminal"]

user_collection = db.get_collection('User')
economic = db.get_collection('Economic Dashboard')
business = db.get_collection('Business Dashboard')
industry = db.get_collection('Industry Dashboard')

economic_collection = economic.find()
economic_collection = pd.DataFrame(economic_collection)
economic_collection.drop('_id', inplace=True, axis=1)

business_collection = business.find()
business_collection = pd.DataFrame(business_collection)
business_collection.drop('_id', inplace=True, axis=1)

industry_collection = industry.find()
industry_collection = pd.DataFrame(industry_collection)
industry_collection.drop('_id', inplace=True, axis=1)