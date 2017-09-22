#Nirmal Kumar Ravichandran
#10.182.26.181






from flask import Flask,request,make_response,session
import MySQLdb
import random
from datetime import datetime
import redis

	

app = Flask(__name__)
app.secret_key = 'any random string'
db = MySQLdb.connect()
cursor = db.cursor()
query_list=["SELECT Domain FROM table_name where TldRank=100",
"SELECT Domain FROM table_name where TldRank=1",
"SELECT Domain FROM table_name where TldRank=3",
"SELECT Domain FROM table_name where GlobalRank=3"
]
redis_db = redis.StrictRedis()


user_content='''
<form action='/random' method='POST'>
<input type='submit' value='Random queries without memcache'/><br>
</form>
<form action='/randomcache' method='POST'>
<input type='submit' value='Random queries with memcache'/><br>
</form>
<form action='/specific' method='POST'>
<input type='submit' value='Specific queries without memcache'/><br>
</form>
<form action='/specificcache' method='POST'>
<input type='submit' value='Specific queries with memcache'/><br>
</form>

'''

@app.route('/')
def hello_world():
	return user_content

@app.route('/random',methods=['POST'])
def random_query_without_cache():
	startTime = datetime.now()
	for x in range(0,100):
		cursor.execute(query_list[random.randint(0,3)])

	return str((datetime.now()-startTime).microseconds)

@app.route('/randomcache',methods=['POST'])
def random_query_with_cache():
	startTime = datetime.now()
	for x in range(0,100):
		query=query_list[random.randint(0,3)]
		if not redis_db.get(query):
			cursor.execute(query)
			redis_db.set(query,cursor.fetchall())
		else:
			rows=redis_db.get(query)
	return str((datetime.now()-startTime).microseconds)

@app.route('/specific',methods=['POST'])
def specific_query_without_cache():
	startTime = datetime.now()
	query='SELECT Domain from table_name where GlobalRank='
	for x in range(0,5):
		cursor.execute(query+str(x))

	return str((datetime.now()-startTime).microseconds)

@app.route('/specificcache',methods=['POST'])
def specific_query_with_cache():
	startTime = datetime.now()
	query='SELECT Domain from table_name where GlobalRank='
	for x in range(0,5):
		query_str=query+str(x)
		#print query_str
		if not redis_db.get(query_str):
			cursor.execute(query_str)
			rows=cursor.fetchall()
			redis_db.set(query,rows)
			print rows
		else:
			rows=redis_db.get(query)

	return str((datetime.now()-startTime).microseconds)



#app.run()