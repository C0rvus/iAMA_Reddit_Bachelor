from pymongo import MongoClient
import unicodedata                                      # necessary for converting unicode datatypes to string


client                              =               MongoClient('localhost', 27017)                                                     # the mongo client, necessary to connect to mongoDB
mongo_DB_Reddit                     =               client.iAMA_Reddit
mongo_DB_Collections                =               mongo_DB_Reddit.collection_names()

# Source: https://stackoverflow.com/questions/7571635/fastest-way-to-check-if-a-value-exist-in-a-list


#if ("43gy5n") in mongo_DB_Collections:
#print ("schnell bin i drin !!!")
#print (mongo_DB_Collections.index("43gy5n"))


# TODO: Dieser Befehl ginge sicherlich schneller....

# Iterate overy every single object within the mongo_DB_Collections
for j in range (0, len(mongo_DB_Collections)):

	#collection_Name_Converted_To_String = unicodedata.normalize('NFKD', mongo_DB_Collections[j])
	collection_Name_Converted_To_String = "43gy5n"

	if collection_Name_Converted_To_String in mongo_DB_Collections:
		print("ich existiere schon !")
		print("pruefe ob ich mich geaendert habe - zwischenzeitlich")

		collection = mongo_DB_Reddit[collection_Name_Converted_To_String]
		cursor = collection.find()

		print (cursor[0].get("author"))
		# print (cursor[0].get("downs")) << not getting calculated here, because this costs lots of performance
		print (cursor[0].get("num_Comments"))
		print (cursor[0].get("selftext"))
		print (cursor[0].get("title"))
		print (cursor[0].get("total_Votes"))
		print (cursor[0].get("ups"))
		print (cursor[0].get("url"))
		mongo_DB_Reddit.drop_collection(collection_Name_Converted_To_String)

		#for document in cursor:
			#print (document)

	else:
		print ("BIN NEU HIER")





		#TODO: Dann checke die einzelnen Columns

