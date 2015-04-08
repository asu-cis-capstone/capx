import requests, os

response = requests.get('http://www.cis440.com')
if str(response.status_code) == '200':
	print("CIS440.com responded with code: " + str(response.status_code) + ' - okay')
else:
	print("Something went wrong - error code: " + str(response.status_code))
	
myPages = ['projects', 'addproject', 'showroom', 'about', 'adminBlog']

for i in range(0,5):
	response = requests.get('http://www.cis440.com/' + myPages[i])
	if str(response.status_code) == '500':
		print("The " + myPages[i] + " page responded with code: " + str(response.status_code) + ' - Okay: page was found, empty response')
	else:
		print("Something went wrong on the " + myPages[i] + " page - error code: " + str(response.status_code))

os.system("start cmd /k ping cis440.com")