	from flask import Flask,request,make_response,session
import boto
import boto.s3
from boto.s3.key import Key
import os
import imghdr
import ConfigParser
import tempfile

	

app = Flask(__name__)
app.secret_key = 'any random string'

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
upload_content='''<html lang="en">
<head>
<title>Nirmal Kumar Ravichandran-%s</title>
</head>
<body><h2>Upload File :</h2><form action='/upload' method='POST' enctype = 'multipart/form-data'>
<input type = "file" multiple="" name = "file" />
<input type='submit' value='Upload'/>
</form>
<hr>
<h2>Delete File :</h2><br>
<form action='/delete' method='POST'>
Filename:<input type='text' name='filename'/>
<input type='submit' value='Delete'/><br>
</form>
<hr>
<h2>Download File :</h2><br>
<form action='/download' method='POST'>
Filename:<input type='text' name='filename'/>
<input type='submit' value='Download'/><br>
</form>
<form action='/move' method='POST'>
Filename:<input type='text' name='filename'/>
Bucket1:<input type='text' name='buck1'/>
Bucket2:<input type='text' name='buck2'/>
<input type='submit' value='Move'/><br>
</form>
<hr>

<br>
<a href='/display'>Display</a>
<hr>

</body>
</html>
'''
user_content='''
<h2>User Access</h2><br>
<form action='/' method='POST'>
Username:<input type='text' name='username'/>
<input type='submit' value='Login'/><br>
</form>

'''
extension_list=[
   "txt"
]

conn1 =boto.connect_s3()
bucket1 = conn1.get_bucket()


@app.route('/')
def hello_world():
	return user_content


@app.route('/move')
def mover():
	buck1=request.forms.get('buck1')
	buck2=request.forms.get('buck2')
	conn1 =boto.connect_s3()
	bucket1=conn.get_bucket(buck1)
	bucket2=conn.get_bucket(buck2)
	filename=request.forms.get('fname')
	k=Key(bucket1)
	k.key=filename
	s=k.get_contents_as_string()
	k=Key(bucket2)
	k.key=filename
	k.set_contents_from_string(s)
	return "File moved!!"


@app.route('/',methods = ['POST'])
def hello_world_po():
	cont=check_user()
	user=request.form.get('username')
	if user in cont:
		conn=get_connection(user)
		#bucket=conn.get_bucket(config.get(user, 'db'))
		if not conn:
			return "Access denied for "+user
		session['user']=user
		return upload_content%session['user']
	else:
		return "Access denied for "+user

def check_user():
	k=Key(bucket1)
	k.key='access.txt'
	return k.get_contents_as_string()

	
@app.route('/download',methods = ['POST'])
def download():
	name=request.form.get('filename')
	conn=get_connection(session['user'])
	bucket=conn.get_bucket(session['db'])
	key=bucket.get_key(name)
	if not key:
		return "File not found"

	cont=key.get_contents_as_string()
	response = make_response(cont)
	response.headers["Content-Disposition"] = "attachment; filename="+name+";"
	return response
def get_connection(user):
	temporary_file = tempfile.NamedTemporaryFile()
	k=Key(bucket1)
	k.key='access.txt'
	cont=k.get_contents_as_string()
	fw=open(temporary_file.name,'w+')
	fw.write(cont)
	fw.close()
	fr=open(temporary_file.name,'r')
	config = ConfigParser.ConfigParser()
	config.readfp(fr)
	conn=boto.connect_s3(config.get(user, 'aws_access_key_id'),config.get(user, 'aws_secret_access_key'))
	session['db']=config.get(user, 'db')
	return conn

@app.route('/upload',methods = ['POST'])
def upload():
	try:
		flist = request.files.getlist('file')
		for f in flist:
			name=f.filename

			if not any([name.lower().endswith(e) for e in extension_list]):
				continue
			
			content=f.read()
			conn=get_connection(session['user'])
			if not conn:
				return "No Connection"
			
			bucket=conn.get_bucket(session['db'])
			result=""
			for fl in bucket:
				if fl.key==name:
					result="File overwrite"
			k= Key(bucket)
			
			k.key=name
			f.seek(0,0)
			k.set_contents_from_file(f)
			if result!="":
				return result
		#s3.Bucket('nirmal1234').put_object(Key=name, Body=content)
		return "file uploaded "
	except Exception as e:
		return str(e)

@app.route('/display')
def display():
	conn=get_connection(session['user'])
	bucket=conn.get_bucket(session['db'])
	result='<ol>'
	list1=''
	for key in bucket.list():
		if any([key.name.encode('utf-8').lower().endswith(e) for e in extension_list]):
			result+='<li>'+key.name.encode('utf-8')+'</li>'
	return result+'</ol>'

@app.route('/delete',methods = ['POST'])
def delete():
	conn=get_connection(session['user'])
	bucket=conn.get_bucket(session['db'])
	name=request.form.get('filename')
	k=Key(bucket)
	k.key=name
	bucket.delete_key(k)
	return "Deleted file!!!"





#app.run()