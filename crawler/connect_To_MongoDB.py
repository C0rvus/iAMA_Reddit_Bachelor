from pymongo import MongoClient                         # necessary to interact with MongoDB
# TODO: Connect PRAW with this DB connection script
# TODO: Comment all that stuff in a better way
# TODO: Create HTTP-Server containing test site with refresh button to start PRAW-Gathering
# TODO: Create REST-Server with FLASK for that stuf

client = MongoClient                                # will be modified by connect_To_MongoDB()
mongo_DB_Reddit = MongoClient                       # will be modified by get_DB_Instance()
mongo_DB_Collections = ""                           # will be modified by get_DB_Collections()
mongo_DataSet_Row = {}                              # will be modified by generate_DataSet_To_Be_Written_To_DB()



# <editor-fold desc="Connects to MongoDB-Server">
# Connects to the specified MongoDB-Server
# We can replace localhost with an IP-Adress, whenever the database runs somewhere else
# Alternative connect method: client = MongoClient('mongodb://localhost:27017/')
# Source: http://api.mongodb.org/python/current/tutorial.html                   @ 28.01.2016 ~ 20:15
#
# </editor-fold>
def connect_To_MongoDB():
	global client                                   # references the global variable to make use of it locally

	client = MongoClient('localhost', 27017)        # filles the global variable with corrrect values, according to the mongoDB we want to connect to

# <editor-fold desc="Retrieves the data base instance "iAMA_Reddit">
# The method below retrieves the correct database instace here "iAMA_Reddit"
# </editor-fold>
def get_DB_Instance():
	global mongo_DB_Reddit                          # references the global variable to make use of it locally

	mongo_DB_Reddit = client.iAMA_Reddit            # refers to the local iAMA_Reddit database and creates it if non existent

# <editor-fold desc="Retrieves all collections / tables">
# Stores all mongoDB collections (tables) into mongo_DB_Collections
# </editor-fold>
def get_DB_Collections():
	global mongo_DB_Reddit                             # references the global variable to make use of it locally
	global mongo_DB_Collections                        # references the global variable to make use of it locally

	mongo_DB_Collections = mongo_DB_Reddit.collection_names()          # stores all collections / tables into that array. Necessary for crawler -> mongoDB writing checking

# <editor-fold desc="Writes test data into the database iAMA_Reddit">
# Writes generated data into all tables
# </editor-fold>
def write_DB_Test_Data():
	global mongo_DataSet_Row                        # references the global variable to make use of it locally
	global mongo_DB_Reddit                          # references the global variable to make use of it locally
	# noinspection PyTypeChecker

	mongo_DataSet_Row = dict({
		"sepp"  :   "Hans_1",
		"sepp2" :   "Hans_2"
	})

	mongo_Collection_To_Be_Written_Into = mongo_DB_Reddit["example_Table"]
	mongo_Collection_To_Be_Written_Into.insert_one(mongo_DataSet_Row)

	print('Test data has been successfully written into example_Table')



connect_To_MongoDB()                                    # Connects to the mongoDB
get_DB_Instance()                                       # Gets and declares the mongoDB-Instance
get_DB_Collections()                                    # Gets all existent collections (necessary to skip unnecessary / redundant writes into mongoDB)
write_DB_Test_Data()                                    # Writes test data into the database, to check whether the connection is working or not