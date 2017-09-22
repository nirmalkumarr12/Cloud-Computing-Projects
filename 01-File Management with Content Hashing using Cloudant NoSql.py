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
import glob
import base64



client=Cloudant()
client.connect()
my_database = client['my_database']
#app = Flask(__name__)
#port = int(os.getenv('PORT', 8080))







def upload_post():
	root=Tkinter.Tk()
	filez = tkFileDialog.askopenfilenames(parent=root,title='Choose a file')#opens the file dialog
	root.withdraw()
	for fil in filez:
		fh=open(fil)
		name,ext=os.path.splitext(fil)
		content=base64.b64encode(fh.read())
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
		
		#conn.put_object('passmt1_cont',os.path.basename(name)+'_'+str(version_num)+ext,contents=str(hash(content)),content_type=ext)
		print "File stored!"

def upload_post():
	root=Tkinter.Tk()
	filez = tkFileDialog.askopenfilenames(parent=root,title='Choose a file')#opens the file dialog
	root.withdraw()
	e=""

	for fil in filez:
		fh=open(fil)
		name,ext=os.path.splitext(fil)
		e=ext
		content=base64.b64encode(fh.read())
		version_num=0
		for doc in text_database:
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

		if(e=='.txt'):
			my_doc=text_database.create_document(data)
		else:
			my_doc=other_database.create_document(data)
		
		#conn.put_object('passmt1_cont',os.path.basename(name)+'_'+str(version_num)+ext,contents=str(hash(content)),content_type=ext)
		print "File stored!"


def list_folder():
	print "1.Text"
	print "2.Other types"
	input=raw_input()
	if(input=='1'):
		for d in text_database:
			print d['name']
	elif(input=='2'):
		for d in other_database:
			print d['name']

def retrieve_post():
	print "Enter keyword"
	name=raw_input()
	
	found=0
	cont=""
	for doc in text_database:
		if doc['content'].find(name):
			found=1
			cont=doc['content']
			break
	if found==0:
		print "File not found"
	#name,ext=name.split('.')
	fh=open(name,'w+')
	fh.write(cont)
	fh.close()
	print "File retrieved!!!"
def upload_post():
	root=Tkinter.Tk()
	filez = tkFileDialog.askopenfilenames(parent=root,title='Choose a file')#opens the file dialog
	root.withdraw()
	e=""

	for fil in filez:
		fh=open(fil)
		name,ext=os.path.splitext(fil)
		e=ext
		content=base64.b64encode(fh.read())
		version_num=0
		for doc in text_database:
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

		if(e=='.txt'):
			my_doc=text_database.create_document(data)
		else:
			my_doc=other_database.create_document(data)
		
		#conn.put_object('passmt1_cont',os.path.basename(name)+'_'+str(version_num)+ext,contents=str(hash(content)),content_type=ext)
		print "File stored!"

def list_folder():
	print "1.Text"
	print "2.Other types"
	input=raw_input()
	if(input=='1'):
		for d in text_database:
			print d['name']
	elif(input=='2'):
		for d in other_database:
			print d['name']

def move_file():
	print "Enter keyword"
	input=raw_input()
	for doc in text_database:
		if doc['content'].find(input):
			other_database.create_document(doc)
			doc.delete()
	print "File moved"




def display_files(input):
	save_path=tkFileDialog.askdirectory()
	os.chdir(save_path)
	for file in glob.glob("*."+input):
		print file
while(True):
	print "1.List"
	print "2.Upload"
	ch=int(raw_input())
	if(ch==1):
		print "Enter file type"
		input=raw_input()
		display_files(input)
	elif(ch==2):
		upload_post()
	else:
		break


















#app.run(host='127.0.0.1', port=5000)