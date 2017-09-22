from flask import Flask,request,make_response,session,request
import boto
import boto.s3
from boto.s3.key import Key
import os
import MySQLdb


app = Flask(__name__)
app.secret_key = 'any random string'
conn1 =boto.connect_s3()
bucket1 = conn1.get_bucket()


db = MySQLdb.connect()
cursor = db.cursor()

index_cont='''
<form method='POST' action='/login'>
<input type='text' name='username'/>
<input type='submit' value='Login'/>
</form><br>
+2
'''


@app.route('/upload',methods=['POST'])
def upload_pic():
	flist = request.files.getlist('file')
	#return str(flist)
	for f in flist:
		f.seek(0,0)
		k=Key(bucket1)
		k.key=f.filename
		#return f.filename
		k.set_contents_from_file(f)
		link=""+f.filename
		insert_query="insert into photo_user(username,photo_name,photo_link) values('{0}','{1}','{2}')".format(session['username'],f.filename,link)
		cursor.execute(insert_query)
		db.commit()
		
		
	return "File uploaded!!"

@app.route('/')
def index():
	return index_cont


@app.route('/login',methods=['POST'])
def login():
	login_content='''
<form method='POST' action='/upload' enctype = 'multipart/form-data'>
<input type = "file" multiple="" name = "file" />
<input type='submit' value='Upload'/>
</form><br><br>
'''
	session['username']=request.form.get('username')
	sql="SELECT * from photo_user" 
	cursor.execute(sql)
	rows=cursor.fetchall()
	content='''
	'''
	for row in rows:
		login_content=login_content+"<img src='{0}' alt='Pic here!' height=40 width=40><br>".format(row[3])
		if row[1]==session['username']:
			login_content=login_content+"<br><form method='GET' action='/remove'><input type='hidden' name='photo_id' value='{0}'/><input type='submit' value='Remove'/></form>".format(row[0])
		login_content=login_content+"<br><form method='GET' action='/insert_comment'><input type='hidden' name='photo_id' value='{0}'/><input type='hidden' name='username' value='{1}'/><input type='text' name='comment'/><input type='submit' value='Comment'/></form>".format(row[0],session['username'])
		query2="SELECT * from photo_comment where photo_id={0}".format(row[0])
		cursor.execute(query2)
		rows2=cursor.fetchall()
		for r in rows2:
			login_content=login_content+"<br><p>{0}:{1}".format(r[1],r[2])

	login_content=login_content+'<hr>'

	return login_content
@app.route('/insert_comment',methods=['GET'])
def insert_comm():
	idphoto=request.args.get('photo_id')
	user=request.args.get('username')
	cmnt=request.args.get('comment')
	sql="insert into photo_comment values({0},'{1}','{2}')".format(idphoto,user,cmnt)
	cursor.execute(sql)
	db.commit()
	return "Comment Inserted!"

@app.route('/remove',methods=['GET'])
def remove():
	try:
		idrem=request.args.get('photo_id')
		sql="delete from photo_user where photoid={0}".format(idrem)
		cursor.execute(sql)
		db.commit()
		return "Removed "+idrem
	except Exception as e:
		return str(e)










