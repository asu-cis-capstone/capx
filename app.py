import psycopg2, requests, json
from flask.ext.github import GitHub
from flask import Flask, render_template, request, redirect, url_for, flash, session

#setup the database connection and create 3 cursor objects to execute SQL statements
conn = psycopg2.connect(database="db", user="user", password="pw", host="host", port="port")
cur = conn.cursor()
cur2 = conn.cursor()
cur3 = conn.cursor()

#setup for GitHub login using Client ID and Client Secret
app = Flask(__name__)
app.config['GITHUB_CLIENT_ID'] = 'clientId'
app.config['GITHUB_CLIENT_SECRET'] = 'ClientSecret'
app.secret_key = 'yourSecretKey'

github = GitHub(app)

# Variables

# These indicate which page has focus
showroomStatus = ''
aboutStatus = ''
projectStatus = ''
homeStatus = ''

# This variable is passed to every child template to determine which Navigation bar they should extend (logged in or not logged in)
logincheck = ''

# ROUTES START HERE
# Each route first checks if the user is currently logged in
# Then it passed the active tab name, username and login status to the template

# Index route
@app.route('/')
def index():
	# Sets the current users GitHub name
	if 'userName' in session:
		print('Do nothing')
	else:
		session['userName'] = ''
		# Tracks if a user is logged in or not
		session['blnLoggedIn'] = ''
		#Tracks the user's oauth code provided through GitHub login
		session['oauth'] = ''
	homeStatus = 'active1'
	if session['blnLoggedIn'] == "yes":
		logincheck = '_loggedin'
	else:
		logincheck = ''
	return render_template("index.html", homeStatus=homeStatus, logincheck=logincheck, userName=session['userName'])

# Projects route
@app.route('/projects', methods = ['GET', 'POST'])
def project():
	# select all projects from the project2 table and order them (highest rating first)
	# pass SQL result to project page
	cur.execute("SELECT * FROM project2 ORDER BY rating DESC;")
	rows = cur.fetchall()
	projectStatus = 'active1'
	if session['blnLoggedIn'] == "yes":
		logincheck = '_loggedin'
	else:
		logincheck = ''
	return render_template("project.html", rows=rows, cur2=cur2, conn=conn, projectStatus=projectStatus, logincheck=logincheck, userName=session['userName'])

# Showroom route	
@app.route('/showroom')
def showroom():
	showroomStatus = 'active1'
	if session['blnLoggedIn'] == "yes":
		logincheck = '_loggedin'
	else:
		logincheck = ''
	return render_template("showroom.html", showroomStatus=showroomStatus, logincheck=logincheck, userName=session['userName'])

# About route
@app.route('/about')
def about():
	aboutStatus = 'active1'
	if session['blnLoggedIn'] == "yes":
		logincheck = '_loggedin'
	else:
		logincheck = ''
	return render_template("about.html", aboutStatus=aboutStatus, logincheck=logincheck, userName=session['userName'])
	
# Login route - calls the GitHub authorize function
@app.route('/login')
def login():
    return github.authorize()

# Logout route
@app.route('/logout')
def logout():
	session['blnLoggedIn'] = ''
	session['userName'] = ''
	return render_template("logout.html")
	
# Welcome route 
# This route is executed once users log in with GitHub
@app.route('/welcome', methods = ['GET', 'POST'])
@github.authorized_handler
def authorized(oauth_token): 
	session['oauth'] = oauth_token
	# check if current user is already in database with the corresponding token
	cur2.execute("SELECT usertoken FROM users WHERE usertoken= %(oauth)s;", {'oauth': session['oauth']})
	user = cur2.fetchone()

	# create new user record if user was not found
	if user is None:
		cur2.execute("INSERT into users VALUES (%(oauth)s)", {'oauth': session['oauth']})
		conn.commit()	
	
	# Following code is used for parsing out the GitHub username from the returned JSON object
	j = requests.get('https://api.github.com/user?access_token=' + session['oauth'])
	j = j.text

	i = 0
	text = ""
	quoteCount = 0
	beginning = 0
	end = 0

	while quoteCount < 4:
		text = text + j[i]
		if j[i] == '"':
			quoteCount = quoteCount + 1
		if quoteCount == 3 and j[i] == '"':
			beginning = i
		if quoteCount == 4:
			end = i
		i = i + 1

	while beginning < end - 1:
		session['userName'] = session['userName'] + (j[beginning+1])
		beginning = beginning + 1
	
	# Add the GitHub name to the record matching the oauth token
	cur2.execute("UPDATE users SET githubname =  %(gitname)s WHERE usertoken = %(oauth)s;", {'gitname': session['userName'], 'oauth': session['oauth']})
	conn.commit()
	
	# Set logged in status to yes
	session['blnLoggedIn'] = 'yes'
	
	return render_template("welcome.html", userName=session['userName'])
	
# Upvote route
# This route is executed whenever a user upvotes a project on the Project page
@app.route('/upvote', methods = ['POST', 'GET'])	
def upvote():
	#check if user is logged in. If not, send them to special log in page
	if session['blnLoggedIn'] == '':
		return render_template("pleaselogin.html")
	else:	
		# The corresponding HTML form posts the ID number for the project that was upvoted
		projectId = request.form.get('upvote', None)
		projectId = int(projectId)
		projectId = projectId - 1
		oauthvote = session['oauth']
		# Get the votingArray from the user table for the currently logged in user
		cur.execute("SELECT votingArray[%(indexof)s] FROM users WHERE usertoken = %(oauth)s;", {'oauth': oauthvote, 'indexof': projectId})
		voteArray = cur.fetchone()
		
		# If the array is already set to 1, then the user has already voted for this specific project
		if voteArray[0] == 1:
			flash('You already voted for this project!')
		# If array is not set to 1, it means the user is allowed to vote for this project
		else:
			# Set the votingArray element to 1 and increment the rating for the appropriate project by 1
			cur3.execute("UPDATE users SET votingArray[%(indexof)s] = 1 WHERE usertoken = %(oauth)s;", {'oauth': oauthvote, 'indexof': projectId})
			conn.commit()
			projectId = projectId + 1
			cur2.execute("update project2 set rating = rating + 1 where id = %(id)s;", {'id': projectId})
			conn.commit()
			flash('You successfully voted for this project!')
		return redirect('/projects')

# Downvote route
# Similar logic as the upvote route, just adapted for downvoting
@app.route('/downvote', methods = ['POST', 'GET'])		
def downvote():	
	
	if session['blnLoggedIn'] == '':
		return render_template("pleaselogin.html")
	else:	
		projectId = request.form.get('downvote', None)
		projectId = int(projectId)
		projectId = projectId - 1
		oauthvote = session['oauth']
		cur.execute("SELECT votingArray[%(indexof)s] FROM users WHERE usertoken = %(oauth)s;", {'oauth': oauthvote, 'indexof': projectId})
		voteArray = cur.fetchone()
		
		if voteArray[0] == 1:
			flash('You already voted for this project!')
		else:
			cur3.execute("UPDATE users SET votingArray[%(indexof)s] = 1 WHERE usertoken = %(oauth)s;", {'oauth': oauthvote, 'indexof': projectId})
			conn.commit()
			projectId = projectId + 1
			cur2.execute("update project2 set rating = rating - 1 where id = %(id)s;", {'id': projectId})
			conn.commit()
			flash('You successfully voted for this project!')

		return redirect('/projects')
	
	
if __name__ == '__main__':
	app.run(debug=True)
	
