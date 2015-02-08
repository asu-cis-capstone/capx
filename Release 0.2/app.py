import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash, session

conn = psycopg2.connect(database="MODIFY", user="MODIFY", password="MODIFY", host="MODIFY", port="MODIFY")
cur = conn.cursor()
cur2 = conn.cursor()

voteArray =[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/', methods = ['GET', 'POST'])
def home():
	cur.execute("SELECT * FROM project2 ORDER BY rating DESC;")
	rows = cur.fetchall()
	return render_template("welcome.html", rows=rows, cur2=cur2, conn=conn)

# LOGIN ROUTES
@app.route('/login.html', methods = ['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if (request.form['username'] != 'admin') \
				or request.form['password'] != 'admin':
			error = 'Invalid Credentials. Please try again.'
		else:
			session['logged_in'] = True
			error = 'Admin'
			return render_template('login.html', error=error)
		return render_template('login.html', error=error)
	
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
	
