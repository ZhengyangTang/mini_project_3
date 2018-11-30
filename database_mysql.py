  
import tweepy  
import requests
import urllib
import sys
import pymysql
from google.cloud import vision_v1


#input keys and secret keys  
consumer_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
consumer_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
access_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
access_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
  
# upload keys and secret keys
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  
auth.set_access_token(access_key, access_secret)  
  
api = tweepy.API(auth)  


#get user's first 10 images from first 200 tweets 


def get_tweets(screen_name,username):
	count = 0;
	public_tweets = api.user_timeline(screen_name = screen_name,count = 200)
	db = pymysql.connect("localhost","root","BRANDnew821","mini_project3")
	cursor = db.cursor()
	string = repr(screen_name)
	for tweet in public_tweets:
		if 'media' in tweet.entities.keys():
			urllib.request.urlretrieve(tweet.entities['media'][0]['media_url'],'C:/EC601/EC601_IMAGES/0%d.jpg'%count)





			tag = tags(count)
			for j in tag:
				if j != '':
					url = tweet.entities["media"][0]["media_url"]
					cursor.execute("insert into %s values( %s, %s, %s)" % (username,string,repr(url),repr(j)) ) #% \
					db.commit()
			count = count + 1
			if count == 10:
				break

		  #(screen_name,20))

	db.close()
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
	db = pymysql.connect("localhost","root","BRANDnew821","mini_project3")
	cursor = db.cursor()
	cursor.execute("select username from users where username = %s" % (repr(username)))
	username_db = cursor.fetchone()


	#username_db1 = username_db[0]
	#print(username_db1)
	if username_db!= None:
		cursor.execute("select password from users where username = %s" % (repr(username)))
		password_db = cursor.fetchone()

		password_db1 = password_db[0]

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
					cursor.execute('''create table %s(
									search_content varchar(255),
									image_url varchar(255),
									tag varchar(255))''' % username_new)
					cursor.execute('insert into users values( %s, %s)'% (repr(username_new),repr(password_new)))
					db.commit()
					print('user successfully created')
				else:
					print('''the password you just entered is different from the password you entered first time.
please check your password.''')
	db.close()
def search_tags(tag):
    db = pymysql.connect("localhost","root","BRANDnew821","mini_project3")
    cursor = db.cursor()
    cursor.execute('show tables')
    users = cursor.fetchall()
    dict = {}
    count = 0
    for user in users:
        results = []
        user_db = user[0]
        if user_db != 'users':
            cursor.execute('select * from %s'%user_db)
            user_info = cursor.fetchall()

            for tags in user_info:
                if tags != () and tags[2] == tag:
                    for i in results:
                        if tags[0] == i:
                            count = count+1
                    if count == 0:
                        #print(tags[0])
                        results.append(tags[0])
                    count = 0
            dict[user_db] = results

    return dict
def hottest_tags():
    db = pymysql.connect("localhost","root","BRANDnew821","mini_project3")
    cursor = db.cursor()
    tag_dict = {}
    cursor.execute("show tables")
    tables=cursor.fetchall()

    for table in tables:
        if table[0]!='users':
            cursor.execute("select tag from %s"%table[0])
            tags=cursor.fetchall()
            count = 0
            #print(tags)
            for tag in tags:

                keys = tag_dict.keys()


                for key in keys:
                    if(key == tag[0]):
                        tag_dict[key] = tag_dict[key]+1
                        count = 1
                if count == 0:
                    tag_dict[tag[0]] = 0
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



