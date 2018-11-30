import tweepy

import urllib
import pymongo
from google.cloud import vision_v1


#input keys and secret keys
consumer_key = 'j92G77my4VGAt2te7N763Wm7X'
consumer_secret = 'YHwG5DhEvHkmuHyCfPyBsUGbPR4gowHEsJr8lLp0LKBp07xBRf'
access_key = '1038545947972780032-qcMd7whlMk4ELMp7n9KqvQPF0kixuh'
access_secret = 'gYZYXTcT7e7jCxRFfC4KvXQPNGZw0MrYfzYS9hcMXklAh'

# upload keys and secret keys
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)


#get user's first 10 images from first 200 tweets


def get_tweets(screen_name,username):
	count = 0;
	public_tweets = api.user_timeline(screen_name = screen_name,count = 200)
	myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
	db = myclient["mini_project3"]
	set = db["%s"%username]

	string = repr(screen_name)
	for tweet in public_tweets:
		if 'media' in tweet.entities.keys():
			urllib.request.urlretrieve(tweet.entities['media'][0]['media_url'],'C:/EC601/EC601_IMAGES/0%d.jpg'%count)





			tag = tags(count)
			for j in tag:
				if j != '':
					url = tweet.entities["media"][0]["media_url"]
					search_dict = {"search content":string,"image_url":repr(url),"tag":j}

					set.insert_one(search_dict)
			count = count + 1
			if count == 10:
				break

		  #(screen_name,20))


def tags(count):
	client = vision_v1.ImageAnnotatorClient()
	tags = []
	with open('C:/EC601/EC601_IMAGES/0%d.jpg'%count, 'rb') as image_file:
		content = image_file.read()
	image = vision_v1.types.Image(content = content)
	response = client.web_detection(image = image)
	detection = response.web_detection
	for i in detection.web_entities:
		tags.append(i.description)

	return tags
def login_register():
	username = input('username:')
	password = input('password:')
	myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
	db = myclient["mini_project3"]
	set = db["users"]
	username_db = set.find_one({"username":username})



	#username_db1 = username_db[0]
	#print(username_db1)
	if username_db!= None:
		password_db1 = username_db["password"]

		if str(password) == password_db1:
			return username#get_tweets('success')#next,pass username into get_tweets
		else:
			print('wrong password')
	else:
		create = input('user do not exist, create a new user? Y/N')
		if create == 'Y' or create == 'y':
			username_new = username;
			confirm_create = input('your username is {username}, continue?Y/N'.format(username = username))
			if confirm_create == 'Y' or confirm_create == 'y':

				password_new = input('password:')
				comfirm_password = input('please enter your password again:')
				if password_new == comfirm_password:

					set.insert({"username":username_new,"password":password_new})

					print('user successfully created')
				else:
					print('''the password you just entered is different from the password you entered first time.
please check your password.''')

def search_tags(tag):
	myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
	db = myclient["mini_project3"]
	users = db.list_collection_names()
	dict = {}
	count = 0
	for user in users:
		results = []

		if user != 'users':
			user_info = db["%s"%user]
			user_info = user_info.find()

			for tags in user_info:
				if tags != {} and tags["tag"] == tag:
					for i in results:
						if tags["search content"] == i:
							count = count+1
					if count == 0:
						#print(tags[0])
						results.append(tags["search content"])
					count = 0
			dict[user] = results

	return dict
def hottest_tags():
	myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
	db = myclient["mini_project3"]
	tag_dict = {}
	tables = db.list_collection_names()

	for table in tables:
		if table!='users':
			temp = db["%s"%table]
			count = 0
			tags = temp.find()
			#print(tags)
			for tag in tags:

				keys = tag_dict.keys()


				for key in keys:
					if(key == tag["tag"]):
						tag_dict[key] = tag_dict[key]+1
						count = 1
				if count == 0:
					tag_dict[tag["tag"]] = 0
				count = 0
	#print(tag_dict)
	values = tag_dict.values()
	#print(values)
	value = []
	for i in values:
		value.append(i)
	max1 = value.index(max(value))
	keys = tag_dict.keys()
	count = 0
	for key in keys:
		if count == max1:
			return key
		count = count+1





if __name__ == '__main__':
	username = login_register()

	if username!= None:
		function1 = input('select the function you want: \n a. Download images form twitter \n b. Search for certain words and '
						  'retrieve which user that has this work in it \n c. Search the hottest tags \n')
		if function1 == 'a' or function1 == 'a.' or function1 == 'A':
			screen_name = input('enter the twitter you wanna get:')
			get_tweets(screen_name,username)
		elif function1 == 'b' or function1 == 'b.' or function1 == 'B':
			count = 0
			tag_search = input('enter the tag you wanna search:')
			for i in search_tags(tag_search):
				if search_tags(tag_search)[i]!=[]:
					for j in search_tags(tag_search)[i]:
						print("user %s get this tag while searching %s"%(i,j))
					count = 1
			if count == 0:
				print("no user has this tag in his sessions")
		elif function1 == 'c' or function1 == 'c.' or function1 == 'C':
			print(hottest_tags())
		else:
			print("wrong input.")
