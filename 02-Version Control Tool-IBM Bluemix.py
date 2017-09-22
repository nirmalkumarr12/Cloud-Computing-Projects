import swiftclient
import Tkinter
import tkFileDialog
import cf_deployment_tracker
import os
import requests
from flask import Flask
from flask import request
from flask import render_template
from werkzeug import secure_filename
import sys
from cloudant.client import Cloudant
import datetime





client=Cloudant("","",url='')
client.connect()
my_database = client['my_database']

cf_deployment_tracker.track()

app = Flask(__name__)
port = int(os.getenv('PORT', 8080))
#app.run(host='0.0.0.0', port=port)


conn=swiftclient.Connection(key=password,
authurl=authentication_url,
auth_version='3',
os_options={"project_id":project_id,
"user_id":user_id,
"region_name":region_name})
conn.put_container('passmt1_cont')

upload_content='''<html lang="en">
<body><h2>Upload File :</h2><form action='/upload' method='POST'>
<input type='submit' value='Upload'/>
</form>
<hr>
<h2>Delete File :</h2><br>
<form action='/delete' method='POST'>
Filename:<input type='text' name='filename'/>
Version:<input type='text' name='version'/>
<input type='submit' value='Delete'/><br>
</form>
<hr>
<h2>Retrieve File :</h2><br>
<form action='/retrieve' method='POST'>
Filename:<input type='text' name='filename'/>
Version:<input type='text' name='version'/>
<input type='submit' value='Retrieve'/><br>
<hr>
<br>
<a href='/display'>Display</a>
<hr>

</body>
</html>
''' 
del_content='''<html lang="en">
<body><form action='/delete' method='POST'>
<input type='text' name='filename'/>
<input type='text' name='version'/>
<input type='submit' value='Delete'/>
</form>
</body>
</html>
'''
index_content='''<html lang="en">
<body>
<a href='/upload'>Upload</a>
<a href='/delete'>Delete</a>
<a href='/display'>Display</a>
<a href='/retrieve'>Retrieve</a>
</body>
</html>
'''
retrieve_content='''
<html lang="en">
<body><form action='/retrieve' method='POST'>
<input type='text' name='filename'/>
<input type='text' name='version'/>
<input type='submit' value='Retrieve'/>
</form>
</body>
</html>
'''
@app.route('/')
def index():
    return upload_content
@app.route('/upload')
def upload():
	return upload_content

@app.route('/upload',methods=['POST'])
def upload_post():
	root=Tkinter.Tk()
	filez = tkFileDialog.askopenfilenames(parent=root,title='Choose a file')#opens the file dialog
	root.withdraw()
	for fil in filez:
		fh=open(fil)
		name,ext=os.path.splitext(fil)
		content=fh.read()
		version_num=0
		for doc in my_database:
			if doc['hash']==str(hash(content)) and doc['name']==os.path.basename(name)+ext:
				return "File already exists"
			if int(doc['version'])>version_num and doc['name']==os.path.basename(name)+ext:
				version_num=int(doc['version'])
		version_num+=1

		data={
			'name':os.path.basename(name)+ext,
			'version':str(version_num),
			'date': str(datetime.datetime.utcnow()),
			'hash':str(hash(content)),
			'content':content
		}
		my_doc=my_database.create_document(data)
		
		conn.put_object('passmt1_cont',os.path.basename(name)+'_'+str(version_num)+ext,contents=str(hash(content)),content_type=ext)
		return "File stored!"

@app.route('/delete_lesser')
def delete():
	lis=[d for d in my_database]
	lis.sort(key=getname)
	for doc in lis:
		name=doc['name']
		max_ver=0
		for doc2 in my_database:
			if max_ver<int(doc2['version']) and name==doc2['name']:
				max_ver=int(doc2['version'])
		for doc1 in my_database:
			if(doc1['name']==name and doc1['version']!=str(max_ver)):
				doc1.delete()
	return "Deleted"

@app.route('/delete',methods=['POST'])
def delete_post():
	name=request.form.get('filename')
	ver=request.form.get('version')
	
	flag_del=0
	for doc in my_database:
		if doc['name']==name and ver==doc['version']:
			doc.delete()
			flag_del=1
	if flag_del==0:
		return 'Files doesnt exist'
	name,ext=name.split('.')
	conn.delete_object('passmt1_cont',name+'_'+ver+'.'+ext)
	return "Successfully Deleted!"

def getname(obj):
	return obj['name'].lower()

@app.route('/display')
def display_files():
	display_content='''<html lang="en">
	<body>
	<table border='1'>
	<tr>
	<th>File Name</th>
	<th>Date saved</th>
	<th>version</th>
	</tr>
	'''
	content=''''''
	lis=[d for d in my_database]
	lis.sort(key=getname)
	
	for doc in lis:
		display_content+='<tr>'
		display_content+='<td>'+doc['name']+'</td>'
		display_content+='<td>'+str(doc['date'])+'</td>'
		display_content+='<td>'+doc['version']+'</td>'
		display_content+='</tr>'
	display_content+='</table></body>'
	return str(display_content)

@app.route('/retrieve')
def retrieve_file():
	return retrieve_content
@app.route('/retrieve',methods=['POST'])
def retrieve_post():
	name=request.form.get('filename')
	ver=request.form.get('version')
	found=0
	cont=""
	for doc in my_database:
		if doc['name']==name and doc['version']==ver:
			found=1
			cont=doc['content']
			break
	if found==0:
		return "File not found"
	name,ext=name.split('.')
	fh=open(name+'_'+ver+'.'+ext,'w+')
	fh.write(cont)
	return "File retrieved!!!"




	

#	conn.put_object('passmt1_cont',f.filename,contents=f.stream.read(),content_type=f.content_type)
#	return "File uploaded"
	

app.run(host='127.0.0.1', port=5000)
