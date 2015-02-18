import psycopg2, requests, json
from flask.ext.github import GitHub
from flask import Flask, render_template, request, redirect, url_for, flash, session


conn = psycopg2.connect(database="name", user="username", password="pw", host="hostString", port="portnumber")
cur = conn.cursor()
cur2 = conn.cursor()

voteArray =[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

app = Flask(__name__)
app.config['GITHUB_CLIENT_ID'] = 'INSERT YOUR CLIENT ID HERE'
app.config['GITHUB_CLIENT_SECRET'] = 'INSERT YOUR CLIENT SECRET HERE'
app.secret_key = 'AAA0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

github = GitHub(app)

@app.route('/', methods = ['GET', 'POST'])
def home():
	cur.execute("SELECT * FROM project2 ORDER BY rating DESC;")
	rows = cur.fetchall()
	return render_template("welcome.html", rows=rows, cur2=cur2, conn=conn)

# LOGIN ROUTES
@app.route('/login')
def login():
    return github.authorize()
	

	
@app.route('/welcome', methods = ['GET', 'POST'])
@github.authorized_handler
def authorized(oauth_token): 
	cur2.execute("SELECT usertoken FROM users WHERE usertoken= %(oauth)s;", {'oauth': oauth_token})
	user = cur2.fetchone()

	if user is None:
		cur2.execute("INSERT into users VALUES (%(oauth)s)", {'oauth': oauth_token})
		conn.commit()	
	
	# short script for parsing out the User Name from GitHub request
	j = requests.get('https://api.github.com/user?access_token=' + oauth_token)
	j = j.text

	i = 0
	text = ""
	quoteCount = 0
	beginning = 0
	end = 0
	userName = ""

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
		userName = userName + (j[beginning+1])
		beginning = beginning + 1
	
	cur2.execute("UPDATE users SET githubname =  %(gitname)s WHERE usertoken = %(oauth)s;", {'gitname': userName, 'oauth': oauth_token})
	conn.commit()
		
	return render_template("GitHubTest.html", userName=userName)
	
	
	
	
	
	
	
	
	
	
# ROUTES FOR RATING SYSTEM. can be improved in the future
	
@app.route('/upvote1', methods = ['POST'])	
def upvote():
	#if array value is 0 then user has not voted. we add 1 for UPVOTE and set to 1
	if voteArray[0] == 0:
		cur2.execute("update project2 set rating = rating + 1 where id = 1")
		conn.commit()
		voteArray[0] = 1
	#if array value is -1 then user DOWNVOTED first. we add 2 for UPVOTE and set to 1
	elif voteArray[0] == -1:
		cur2.execute("update project2 set rating = rating + 2 where id = 1")
		conn.commit()
		voteArray[0] = 1
	return redirect('/')
	
@app.route('/downvote1', methods = ['POST'])	
def downvote():
	#if array value is 0 then user has not voted. we subtract 1 for DOWNVOTE and set to -1
	if voteArray[0] == 0:
		cur2.execute("update project2 set rating = rating - 1 where id = 1")
		conn.commit()
		voteArray[0] = -1
	#if array value is 0 then user UPVOTED first. we subtract 2 for DOWNVOTE and set to -1
	if voteArray[0] == 1:
		cur2.execute("update project2 set rating = rating - 2 where id = 1")
		conn.commit()
		voteArray[0] = -1
	return redirect('/')
	
@app.route('/upvote2', methods = ['POST'])	
def upvote2():
	#if array value is 0 then user has not voted. we add 1 for UPVOTE and set to 1
	if voteArray[1] == 0:
		cur2.execute("update project2 set rating = rating + 1 where id = 2")
		conn.commit()
		voteArray[1] = 1
	#if array value is -1 then user DOWNVOTED first. we add 2 for UPVOTE and set to 1
	elif voteArray[1] == -1:
		cur2.execute("update project2 set rating = rating + 2 where id = 2")
		conn.commit()
		voteArray[1] = 1
	return redirect('/')
	
@app.route('/downvote2', methods = ['POST'])	
def downvote2():
	#if array value is 0 then user has not voted. we subtract 1 for DOWNVOTE and set to -1
	if voteArray[1] == 0:
		cur2.execute("update project2 set rating = rating - 1 where id = 2")
		conn.commit()
		voteArray[1] = -1
	#if array value is 0 then user UPVOTED first. we subtract 2 for DOWNVOTE and set to -1
	if voteArray[1] == 1:
		cur2.execute("update project2 set rating = rating - 2 where id = 2")
		conn.commit()
		voteArray[1] = -1
	return redirect('/')
	
@app.route('/upvote3', methods = ['POST'])	
def upvote3():
	#if array value is 0 then user has not voted. we add 1 for UPVOTE and set to 1
	if voteArray[2] == 0:
		cur2.execute("update project2 set rating = rating + 1 where id = 3")
		conn.commit()
		voteArray[2] = 1
	#if array value is -1 then user DOWNVOTED first. we add 2 for UPVOTE and set to 1
	elif voteArray[2] == -1:
		cur2.execute("update project2 set rating = rating + 2 where id = 3")
		conn.commit()
		voteArray[2] = 1
	return redirect('/')
	
@app.route('/downvote3', methods = ['POST'])	
def downvote3():
	#if array value is 0 then user has not voted. we subtract 1 for DOWNVOTE and set to -1
	if voteArray[2] == 0:
		cur2.execute("update project2 set rating = rating - 1 where id = 3")
		conn.commit()
		voteArray[2] = -1
	#if array value is 0 then user UPVOTED first. we subtract 2 for DOWNVOTE and set to -1
	if voteArray[2] == 1:
		cur2.execute("update project2 set rating = rating - 2 where id = 3")
		conn.commit()
		voteArray[2] = -1
	return redirect('/')
	
@app.route('/upvote4', methods = ['POST'])	
def upvote4():
	#if array value is 0 then user has not voted. we add 1 for UPVOTE and set to 1
	if voteArray[3] == 0:
		cur2.execute("update project2 set rating = rating + 1 where id = 4")
		conn.commit()
		voteArray[3] = 1
	#if array value is -1 then user DOWNVOTED first. we add 2 for UPVOTE and set to 1
	elif voteArray[3] == -1:
		cur2.execute("update project2 set rating = rating + 2 where id = 4")
		conn.commit()
		voteArray[3] = 1
	return redirect('/')
	
@app.route('/downvote4', methods = ['POST'])	
def downvote4():
	#if array value is 0 then user has not voted. we subtract 1 for DOWNVOTE and set to -1
	if voteArray[3] == 0:
		cur2.execute("update project2 set rating = rating - 1 where id = 4")
		conn.commit()
		voteArray[3] = -1
	#if array value is 0 then user UPVOTED first. we subtract 2 for DOWNVOTE and set to -1
	if voteArray[3] == 1:
		cur2.execute("update project2 set rating = rating - 2 where id = 4")
		conn.commit()
		voteArray[3] = -1
	return redirect('/')	
	
if __name__ == '__main__':
	app.run(debug=True)
	
