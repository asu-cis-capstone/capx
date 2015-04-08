import requests, os, psycopg2


conn = psycopg2.connect(database="MODIFY", user="MODIFY", password="MODIFY", host="MODIFY", port="MODIFY")
cur = conn.cursor()


cur.execute("select id, uploadlink from project2;")
imageURLs = cur.fetchall()

print("Total images in database: " + str(len(imageURLs)))

for row in imageURLs:
	response = requests.get(row[1])
	if str(response.status_code) == '200':
		print("Image"+ str(row[0]) +" responded with code: " + str(response.status_code) + ' - okay')
	else:
		print("Something went wrong - error code: " + str(response.status_code))


