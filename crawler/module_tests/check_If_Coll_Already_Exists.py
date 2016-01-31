from pymongo import MongoClient

client                              =               MongoClient('localhost', 27017)                                                     # the mongo client, necessary to connect to mongoDB
mongo_DB_Reddit                     =               client.iAMA_Reddit
mongo_DB_Collections                =               mongo_DB_Reddit.collection_names()


