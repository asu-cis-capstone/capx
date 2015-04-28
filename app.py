import psycopg2, requests, json, markdown, os
from flask.ext.github import GitHub
from flask import Flask, render_template, request, redirect, url_for, flash, session, g, send_from_directory, Response
import datetime
from flaskext.markdown import Markdown
from werkzeug import secure_filename
from hashlib import sha1
import time, base64, hmac, urllib
import boto
from boto.s3.key import Key


def connect_db():
	g.conn = psycopg2.connect(database="MODIFY", user="MODIFY", password="MODIFY", host="MODIFY", port="MODIFY")
	g.cur = g.conn.cursor()
	
def close_db():
	g.conn.close()
	g.cur.close()
	
	
#setup for GitHub login using Client ID and Client Secret
app = Flask(__name__)
app.config['GITHUB_CLIENT_ID'] = 'MODIFY'
app.config['GITHUB_CLIENT_SECRET'] = 'MODIFY'
app.secret_key = 'MODIFY'
app.config['AWS_ACCESS_KEY_ID'] = 'MODIFY'
app.config['AWS_SECRET_ACCESS_KEY'] = 'MODIFY'

Markdown(app)
github = GitHub(app)

# Variables

# These indicate which page has focus
showroomStatus = ''
aboutStatus = ''
projectStatus = ''
homeStatus = ''
addprojectStatus = ''
adminStatus = ''

# This variable is passed to every child template to determine which Navigation bar they should extend (logged in or not logged in)
logincheck = ''

# ROUTES START HERE
# Each route first checks if the user is currently logged in
# Then it passed the active tab name, username and login status to the template

# Index route
@app.route('/')
def index():
	connect_db()
	# Sets the current users GitHub name
	if 'userName' in session:
		print('User already in session...')
	else:
		session['userName'] = ''
		session['adminCheck'] = ''
		# Tracks if a user is logged in or not
		session['blnLoggedIn'] = ''
		#Tracks the user's oauth code provided through GitHub login
		session['oauth'] = ''		
	
	homeStatus = 'active1'
	if session['blnLoggedIn'] == "yes":
		logincheck = '_loggedin'
	else:
		logincheck = ''
	

	# pull all blog posts, show the most recent
	g.cur.execute("select * from Blog where active = 'yes' order by datecreated desc, timecreated desc;")
	blogs = g.cur.fetchall()

	close_db()

	return render_template("index.html", homeStatus=homeStatus, logincheck=logincheck, admin=session['adminCheck'], userName=session['userName'], blogs=blogs)

# Projects route
@app.route('/projects', methods = ['GET', 'POST'])
def project():
	connect_db()
	# select all projects from the project2 table and order them (highest rating first)
	# pass SQL result to project page
	g.cur.execute("SELECT * FROM project2 where active = 'yes' ORDER BY rating DESC;")
	rows = g.cur.fetchall()
	projectStatus = 'active1'
	if session['blnLoggedIn'] == "yes":
		logincheck = '_loggedin'
	else:
		logincheck = ''
	close_db()
	return render_template("project.html", rows=rows, projectStatus=projectStatus, logincheck=logincheck, userName=session['userName'], admin=session['adminCheck'])

# Showroom route	
@app.route('/showroom')
def showroom():
	showroomStatus = 'active1'
	if session['blnLoggedIn'] == "yes":
		logincheck = '_loggedin'
	else:
		logincheck = ''
	return render_template("showroom.html", showroomStatus=showroomStatus, logincheck=logincheck, userName=session['userName'], admin=session['adminCheck'])

# About route
@app.route('/about')
def about():
	aboutStatus = 'active1'
	if session['blnLoggedIn'] == "yes":
		logincheck = '_loggedin'
	else:
		logincheck = ''
	return render_template("about.html", aboutStatus=aboutStatus, logincheck=logincheck, userName=session['userName'], admin=session['adminCheck'])
	
# Add Project route
@app.route('/addproject')
def addproject():
	addprojectStatus = 'active1'
	if session['blnLoggedIn'] == "yes":
		logincheck = '_loggedin'
	else:
		logincheck = ''
	return render_template("addproject.html", addprojectStatus=addprojectStatus, logincheck=logincheck, userName=session['userName'], admin=session['adminCheck'])
	
# Login route - calls the GitHub authorize function
@app.route('/login')
def login():
    return github.authorize()

# Logout route
@app.route('/logout')
def logout():
	session.pop('userName', None)
	session.clear()
	flash('You successfully logged out!')
	return redirect(url_for('index', _external=True))
	
# Admin route
@app.route('/adminpanel')
def adminpanel():
	if session['adminCheck'] != 'yes':
		#return redirect(url_for('index', _external=True, _scheme='https'))
		return redirect(url_for('index', _external=True))
	adminStatus = 'active1'
	if session['blnLoggedIn'] == "yes":
		logincheck = '_loggedin'
	else:
		logincheck = ''
	return render_template("adminpanel.html", adminStatus=adminStatus, logincheck=logincheck, userName=session['userName'], admin=session['adminCheck'])


# Welcome route 
# This route is executed once users log in with GitHub
@app.route('/welcome', methods = ['GET', 'POST'])
@github.authorized_handler
def authorized(oauth_token): 
	connect_db()
	session['oauth'] = oauth_token
	j = requests.get('https://api.github.com/user?access_token=' + session['oauth'])
	j = json.loads(j.content.decode('utf-8'))
	session['userName'] = j['login']
		
	# check if current user is already in database with the corresponding githubname
	g.cur.execute("SELECT githubname FROM users WHERE githubname= %(user)s;", {'user': session['userName']})
	user = g.cur.fetchone()

	# create new user record if user was not found
	if user is None:
		g.cur.execute("INSERT into users (usertoken, githubname) VALUES (%(oauth)s, %(user)s)", {'oauth': session['oauth'], 'user': session['userName']})
		g.conn.commit()	
	else:
		g.cur.execute("UPDATE users SET usertoken =  %(oauth)s  WHERE githubname = %(user)s;", {'oauth': session['oauth'], 'user': session['userName']})
		g.conn.commit()	
		
	currentDate = datetime.date.today()
	g.cur.execute("UPDATE users SET lastlogindate = %(date)s WHERE githubname = %(user)s;", {'date': currentDate, 'user': session['userName']})
	g.conn.commit()
	
	# Set logged in status to yes
	session['blnLoggedIn'] = 'yes'
	
	# temporary solution to check if the user is an admin. Should be switched to DB conn line
	g.cur.execute("SELECT accountType FROM users WHERE githubname = %(user)s", {'user': session['userName']})
	result = g.cur.fetchone()
	
	if result[0] == 'admin':
		session['adminCheck'] = 'yes'
	
	close_db()
	return redirect(url_for('index', _external=True))
	
# Upvote route
# This route is executed whenever a user upvotes a project on the Project page
@app.route('/upvote', methods = ['POST', 'GET'])	
def upvote():
	#check if user is logged in. If not, send them to special log in page
	if session['blnLoggedIn'] == '':
		return render_template("pleaselogin.html")
	else:	
		connect_db()
		# The corresponding HTML form posts the ID number for the project that was upvoted
		projectId = request.form.get('upvote', None)
		projectId = int(projectId)
		projectId = projectId - 1
		oauthvote = session['userName']
		# Get the votingArray from the user table for the currently logged in user
		g.cur.execute("SELECT votingArray[%(indexof)s] FROM users WHERE githubname = %(oauth)s;", {'oauth': oauthvote, 'indexof': projectId})
		voteArray = g.cur.fetchone()
		
		# If the array is already set to 1, then the user has already voted for this specific project
		if voteArray[0] == 1:
			flash('You already upvoted this project!')
		elif voteArray[0] == -1:
			g.cur.execute("UPDATE users SET votingArray[%(indexof)s] = 0 WHERE githubname = %(oauth)s;", {'oauth': oauthvote, 'indexof': projectId})
			g.conn.commit()
			projectId = projectId + 1
			g.cur.execute("update project2 set rating = rating + 1 where id = %(id)s;", {'id': projectId})
			g.conn.commit()
			flash('You now have a neutral vote for this project!')
		# If array is not set to 1, it means the user is allowed to vote for this project
		else:
			# Set the votingArray element to 1 and increment the rating for the appropriate project by 1
			g.cur.execute("UPDATE users SET votingArray[%(indexof)s] = 1 WHERE githubname = %(oauth)s;", {'oauth': oauthvote, 'indexof': projectId})
			g.conn.commit()
			projectId = projectId + 1
			g.cur.execute("update project2 set rating = rating + 1 where id = %(id)s;", {'id': projectId})
			g.conn.commit()
			flash('You successfully voted for this project!')
		close_db()
		return redirect('/projects')

# Downvote route
# Similar logic as the upvote route, just adapted for downvoting
@app.route('/downvote', methods = ['POST', 'GET'])		
def downvote():	
	
	if session['blnLoggedIn'] == '':
		return render_template("pleaselogin.html")
	else:	
		connect_db()
		projectId = request.form.get('downvote', None)
		projectId = int(projectId)
		projectId = projectId - 1
		oauthvote = session['userName']
		g.cur.execute("SELECT votingArray[%(indexof)s] FROM users WHERE githubname = %(oauth)s;", {'oauth': oauthvote, 'indexof': projectId})
		voteArray = g.cur.fetchone()
		
		if voteArray[0] == -1:
			flash('You already downvoted this project!')
		elif voteArray[0] == 1:
			g.cur.execute("UPDATE users SET votingArray[%(indexof)s] = 0 WHERE githubname = %(oauth)s;", {'oauth': oauthvote, 'indexof': projectId})
			g.conn.commit()
			projectId = projectId + 1
			g.cur.execute("update project2 set rating = rating - 1 where id = %(id)s;", {'id': projectId})
			g.conn.commit()
			flash('You now have a neutral vote for this project!')
		else:
			g.cur.execute("UPDATE users SET votingArray[%(indexof)s] = -1 WHERE githubname = %(oauth)s;", {'oauth': oauthvote, 'indexof': projectId})
			g.conn.commit()
			projectId = projectId + 1
			g.cur.execute("update project2 set rating = rating - 1 where id = %(id)s;", {'id': projectId})
			g.conn.commit()
			flash('You successfully voted for this project!')
		close_db()
		return redirect('/projects')
		
# Propose project route		
@app.route('/proposeproject', methods = ['POST', 'GET'])
def proposeproject():
	connect_db()
	# Find the highest project Id, cast to int
	g.cur.execute("select id from project2 order by id desc limit 1;")
	maxid = g.cur.fetchone()
	print (maxid)
	maxid = int(maxid[0])
	# Add 1 to max id 
	maxid = maxid + 1
	maxid = str(maxid)

	# Connect to Amazon S3
	s3 = boto.connect_s3(app.config['AWS_ACCESS_KEY_ID'], app.config['AWS_SECRET_ACCESS_KEY'])
	
	# Get a handle to the S3 bucket
	bucket_name = 'cis440images'
	print (bucket_name)
	bucket = s3.get_bucket(bucket_name)
	k = Key(bucket)

	# Loop over the list of files from the HTML input control
	data_files = request.files.getlist('file')
	print(data_files[0])
	

	for data_file in data_files:
		if data_file.filename == '':
			uploadUrl = "../static/capx.jpeg"
		else:
			# Read the contents of the file
			file_contents = data_file.read()

			# Use Boto to upload the file to the S3 bucket
			originalFileName = data_file.filename
			print('Original name: ' + originalFileName)
			# Create a unique file name based on the current project ID and the original upload name
			newFileName = maxid + originalFileName
			k.key = newFileName
			k.content_type ='image/jpeg'
			print ("Uploading some data to " + bucket_name + " with key: " + k.key)
			uploadUrl = "https://cis440images.s3.amazonaws.com/" + newFileName
			print(uploadUrl)
			k.set_contents_from_string(file_contents)	

	firstName = request.form.get('firstname', None)
	lastName = request.form.get('lastname', None)
	email = request.form.get('email', None)
	phone = request.form.get('phone', None)
	company = request.form.get('company', None)
	projectTitle = request.form.get('project', None)
	description = request.form.get('comment', None)
	
	
	currentDate = date = datetime.date.today()
	semester = 'Spring2015'
	contact = firstName + ' ' + lastName
	
	print (firstName)
	print (lastName)
	print (email)
	print (phone)
	print (company)
	print (projectTitle)
	print (description)
	
	
	g.cur.execute("INSERT INTO PROJECT2 (company, description, rating, dateCreated, semester, contact, email, phone, active, title, uploadlink) VALUES (%(company)s, %(description)s, 0, %(date)s, %(semester)s, %(contact)s, %(email)s, %(phone)s, 'no', %(title)s, %(link)s);", {'company': company, 'description': description, 'date': currentDate, 'semester': semester, 'contact': contact, 'email': email, 'phone': phone, 'title':projectTitle, 'link': uploadUrl})
	g.conn.commit()
	
	close_db()
	flash('You successfully submitted a project!')
	
	return redirect(url_for('index', _external=True))

# Express interest in project route
@app.route('/expressInterest', methods = ['POST', 'GET'])
def expressInterest():
	if session['blnLoggedIn'] == '':
		return render_template("pleaselogin.html")
	
	projectId = request.form.get('expressInterest', None)
	projectId = int(projectId)
	print (projectId)
	connect_db()	

	g.cur.execute("SELECT interested from PROJECT2 WHERE id = %(id)s;", {'id': projectId})
	result = g.cur.fetchall()
	
	newInterest = [session['userName']]
	print(result[0][0])
	
	if result[0][0] is None:
		print("Nobody has expressed interest yet, first record is being added...")
		newResult = newInterest
	else:
		if session['userName'] in result[0][0]:
			flash('You already expressed interest to work on this project!')
			return redirect('/projects')
		else: 
			flash('You successfully expressed interest to work on this project!')
			newResult = result[0][0] + newInterest

	g.cur.execute("UPDATE project2 set interested = %s WHERE id = %s;", (newResult, projectId))
	g.conn.commit()
	close_db()
	return redirect('/projects')
	
# Admin Feature: Blog Main Page
@app.route('/adminBlog')
def adminBlog():
	if session['adminCheck'] != 'yes':
		return redirect(url_for('index', _external=True))
	adminStatus = 'active1'
	if session['blnLoggedIn'] == "yes":
		logincheck = '_loggedin'
	else:
		logincheck = ''
	return render_template("adminBlog.html", adminStatus=adminStatus, logincheck=logincheck, userName=session['userName'], admin=session['adminCheck'])	
	
# Admin Feature: Blog Edit Post
@app.route('/adminBlogEdit')
def adminBlogEdit():
	if session['adminCheck'] != 'yes':
		return redirect(url_for('index', _external=True))
	adminStatus = 'active1'
	if session['blnLoggedIn'] == "yes":
		logincheck = '_loggedin'
	else:
		logincheck = ''
	
	connect_db()
	g.cur.execute("SELECT * from blog where active = 'yes' order by datecreated desc;")
	blogs = g.cur.fetchall()
	close_db()
		
	return render_template("adminBlogEdit.html", adminStatus=adminStatus, logincheck=logincheck, userName=session['userName'], admin=session['adminCheck'], blogs=blogs)	
	
# Admin Feature: Blog edit methods
@app.route('/blogedit', methods = ['POST', 'GET'])
def blogedit():
	if session['adminCheck'] != 'yes':
		return redirect(url_for('index', _external=True))
	
	currentDate = datetime.date.today()
	time = datetime.datetime.now()
	hour = time.hour
	minute = time.minute
	timeCreated = str(hour) + ':' + str(minute)
	
	blogwriter = ''
	blogwriter = session['userName']
	
	blogtitle = request.form.get('blogtitle', None)
	blogpost = request.form.get('blogpost', None)
	id = request.form.get('blogid', None)
	
	active = ''
	if blogpost == '':
		active = 'no'
	else:
		active = 'yes'
	
	connect_db()
	g.cur.execute("UPDATE BLOG set blogwriter = %s, blogtitle = %s, blogentry = %s, dateCreated = %s, timeCreated = %s, editstatus = 'yes', active = %s WHERE id = %s;", (blogwriter, blogtitle, blogpost, currentDate, timeCreated, active, id))
	g.conn.commit()
	close_db()
	
	flash('You successfully edited a blog post!')
	return redirect('/adminBlogEdit')
	

# Admin Feature: Blog entry
@app.route('/blogentry', methods = ['POST', 'GET'])		
def blogentry():	
	if session['adminCheck'] != 'yes':
		return redirect(url_for('index', _external=True))
	blogtitle = request.form.get('blogtitle', None)
	blogpost = request.form.get('blogpost', None)
	
	currentDate = datetime.date.today()
	time = datetime.datetime.now()
	hour = time.hour
	minute = time.minute
	timeCreated = str(hour) + ':' + str(minute)
	
	blogwriter = ''
	blogwriter = session['userName']
	
	connect_db()
	g.cur.execute("INSERT INTO BLOG (blogtitle, blogentry, blogwriter, dateCreated, timeCreated) VALUES (%s, %s, %s, %s, %s);", (blogtitle, blogpost, blogwriter, currentDate, timeCreated))
	g.conn.commit()
	close_db()
	flash('You successfully submitted a blog entry!')
	return redirect('/adminBlog')
	
# Admin Feature: Project approval Main Page
@app.route('/adminProject')
def adminProject():
	if session['adminCheck'] != 'yes':
		return redirect(url_for('index', _external=True))
	connect_db()
	adminStatus = 'active1'
	if session['blnLoggedIn'] == "yes":
		logincheck = '_loggedin'
	else:
		logincheck = ''
	
	g.cur.execute("SELECT * from project2 WHERE active = 'no' ORDER BY dateCreated desc;")
	pending = g.cur.fetchall()
	close_db()
	return render_template("adminProject.html", adminStatus=adminStatus, logincheck=logincheck, userName=session['userName'], admin=session['adminCheck'], pending=pending)
	
# Admin Feature: Approve and Add Comment toProject
@app.route('/addcomment', methods = ['POST', 'GET'])		
def addcomment():	
	if session['adminCheck'] != 'yes':
		return redirect(url_for('index', _external=True))
	projectid = request.form.get('commentid', None)
	comment = request.form.get('addedcomment', None)
	comment = str(comment)
	
	
	newdescription = request.form.get('addeddescription', None)
	newdescription = str(newdescription)
	
	connect_db()
	g.cur.execute("SELECT description FROM project2 WHERE id = %(id)s;",{'id':projectid})
	olddescription = g.cur.fetchone()
	olddescription = olddescription[0]
	print(olddescription)
	close_db()
	
	print(newdescription)
	
	editStatus = ''
	if newdescription == olddescription:
		editStatus = 'no'
	else:
		editStatus = 'yes'
		
	print(editStatus)
	
	tags = request.form.get('addedtags', None)
	tags = str(tags)
	print (tags)
	tags = "{" + tags + "}"
	print(tags)
	
	print (comment)
	print (projectid)
	
	connect_db()
	if editStatus == 'yes':
		g.cur.execute("UPDATE project2 SET active = 'yes', comments = %s, tags = %s, description = %s, editstatus = %s WHERE id = %s;", (comment, tags, newdescription, editStatus, projectid))
		g.conn.commit()
	else:
		g.cur.execute("UPDATE project2 SET active = 'yes', comments = %s, tags = %s, editstatus = %s WHERE id = %s;", (comment, tags, editStatus, projectid))
		g.conn.commit()
	close_db()
	flash('You successfully approved a project!')
	return redirect('/adminProject')
	
# Admin Feature: Promote Admin Main Page
@app.route('/adminPromote', methods = ['POST', 'GET'])
def adminPromote():
	if session['adminCheck'] != 'yes':
		return redirect(url_for('index', _external=True))
	connect_db()
	adminStatus = 'active1'
	if session['blnLoggedIn'] == "yes":
		logincheck = '_loggedin'
	else:
		logincheck = ''
	g.cur.execute("SELECT githubname from users WHERE accountType = 'normal';")
	normUser = g.cur.fetchall()
	close_db()	
	
	return render_template("adminPromote.html", adminStatus=adminStatus, logincheck=logincheck, userName=session['userName'], admin=session['adminCheck'], normUser=normUser)
		
# Admin Feature: Promote Account to Admin
@app.route('/createAdmin', methods = ['POST', 'GET'])
def createAdmin():
	if session['adminCheck'] != 'yes':
		return redirect(url_for('index', _external=True))
	githubname = request.form.get('createAdmin', None)
	print ('Trying to promote...' + githubname)
	
	connect_db()
	g.cur.execute("SELECT githubname from users where accountType = 'normal';")
	normUser = g.cur.fetchall()

	nameExists = 0
	for row in normUser:
		if githubname == row[0]:
			nameExists = 1
	if nameExists == 1:
		g.cur.execute("UPDATE users SET accountType = 'admin' WHERE githubname = %(name)s;", {'name':githubname})
		g.conn.commit()
		close_db()
		print('Successfully promoted ' + githubname)
		flash('Successfully promoted ' + githubname + ' to admin!')
	else:
		flash('No record with this GitHub name exists. Please try again.')
		close_db()
		
	return redirect('/adminPromote')

# Admin Feature: Promote Admin Main Page
@app.route('/adminRoster', methods = ['POST', 'GET'])
def adminRoster():
	if session['adminCheck'] != 'yes':
		return redirect(url_for('index', _external=True))
	connect_db()
	adminStatus = 'active1'
	if session['blnLoggedIn'] == "yes":
		logincheck = '_loggedin'
	else:
		logincheck = ''
	g.cur.execute("SELECT githubname, lastlogindate, accountType from users order by githubname")
	roster = g.cur.fetchall()
	close_db()	
	
	return render_template("adminRoster.html", adminStatus=adminStatus, logincheck=logincheck, userName=session['userName'], admin=session['adminCheck'], roster=roster)
	
# Admin Feature: Set Project Inactive
@app.route('/adminInactive', methods = ['POST', 'GET'])
def adminInactive():
	if session['adminCheck'] != 'yes':
		return redirect(url_for('index', _external=True))
	connect_db()
	adminStatus = 'active1'
	if session['blnLoggedIn'] == "yes":
		logincheck = '_loggedin'
	else:
		logincheck = ''
	
	g.cur.execute("SELECT * FROM PROJECT2 WHERE active = 'yes'")
	inactiveProjects = g.cur.fetchall()
	
	close_db()
	
	return render_template("adminInactive.html", adminStatus=adminStatus, logincheck=logincheck, userName=session['userName'], admin=session['adminCheck'], inactiveProjects=inactiveProjects)

# Admin Feature: Project Inactive
@app.route('/inactivateProject', methods = ['POST', 'GET'])
def inactivateProject():
	if session['adminCheck'] != 'yes':
		return redirect(url_for('index', _external=True))
	
	projectId = request.form.get('projectId', None)
	projectId = int(projectId)
	
	connect_db()
	g.cur.execute("UPDATE project2 SET active = 'no' WHERE id = %(id)s;", {'id':projectId})
	g.conn.commit()
	
	close_db()
	
	flash('Successfully set project inactive!')
	
	return redirect('/adminInactive')

# Admin Feature: Printer friendly projects
@app.route('/adminPrint')
def adminPrint():
	if session['adminCheck'] != 'yes':
		return redirect(url_for('index', _external=True))
	connect_db()
	adminStatus = 'active1'
	if session['blnLoggedIn'] == "yes":
		logincheck = '_loggedin'
	else:
		logincheck = ''
		
	connect_db()
	g.cur.execute("SELECT id, company, title, description, contact, email, phone, rating FROM project2 WHERE active = 'yes' ORDER BY rating desc;")
	result = g.cur.fetchall()
	
	close_db()
	
	return render_template('adminPrintProjects.html', adminStatus=adminStatus, logincheck=logincheck, userName=session['userName'], admin=session['adminCheck'], result = result)
		
	
if __name__ == '__main__':
	app.run(debug=True)
	
	
	
	
	
	
	
	
	
	
	
	
	