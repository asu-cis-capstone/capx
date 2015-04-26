Test Cases by Title
==============
 
Overview
=========
The CAPx team put together a total of ten different test cases for the testing of CIS440.com. Please view each item below to gain an understanding of each test as well as how to use it. The tests created run on various platforms, ranging anywhere from C# to Python. 

**Test 1: SeleniumProjectFormTest_STEVETRUONG**
<<<<<<< HEAD
- *Please install FireFox to use this test*
=======
- *Please install FireFox & the Selenium web driver to use this test*
>>>>>>> 73bfca18420c67b6048b9a4a6d45c31936e656d8
- The aim of this test is to determine if the fields on the project form process invalid entries (i.e. not an email address for the email address field, etc.) It needs to be run using Visual Studios and you must have access to an Admin Account on CIS440.com. Download the file, unzip it, and open the solution in Visual Studios. Once open, look at the code and find two placeholders and replace them with the necessary information:
  - [ADMIN USER NAME]
  - [ADMIN PASSWORD]
- Once completed, run the solution. You should see a console window open followed by a FireFox browser window. Once the test is complete, the console window will appear and tell you which fields processed invalid input.

**Test 2: SeleniumAccessAdminWORights_STEVETRUONG**
<<<<<<< HEAD
=======
- *Please install FireFox & the Selenium web driver to use this test*
-The aim of this test is to attempt to access admin rights as a user without admin rights. To use the test, you will need visual studios and should have an account on CIS440.com that does not have admin rights.
-If the test fails, a console window will tell you that the user does not have sufficient permissions to use admin rights.

**Test 3: pingTest.py (Python Script)**

- **How to run:** launch the python script as you would any other python script, with the command line -windows: py pingTest.py

- **What it does:** sends request messages to various subpages on CIS440.com and checks their reponse status. At the end it will also launch a separate CMD window that will execute a ping command to CIS440 to see if the site is up and running.

- **Sample output:**


	- CIS440.com responded with code: 200 - okay
	- The addproject page responded with... etc


**Test 4: amazonS3test.py (Python Script)**

- **How to run:** launch the python script as you would any other python script, with the command line -windows: py amazonS3test.py. This script assumes that you have a database set up with a column labeled 'uploadlink' which stores the direct link to an image file hosted on amazon S3.

- **What it does:** Retrieves all direct image links from the CAPx database and sends out status requests to each image file and notes the reponse code. This will allow us to track if any externally hosted files are having issues.

- **Sample output:**

	- Image(id) responded with code: 200 - okay
	- Image40 responded with code: 200 -okay


**Test 5: Voting_Test_Case.html**
- *Please install FireFox & Selenium IDE plugin to use this test*
- This test checks to see if the user is logged in, allowing them to vote on proposed projects. If user is not logged in they should get an error.

**Test 6: Admin_Test_Case_ForModifiedTag.html**
- *Please install FireFox & Selenium IDE plugin to use this test* 
- This test checks to make sure the modified tag appears after an edit has been made to the project description.


**Test: TestCase1.py**
- Test case uses the Selenium IDE with Firefox and Python plugin
- The test is used to determine if a user is directed to a Github login page if they attempt to perform an action on the site that requires the user to be logged in
- Example: user attempts action on the projects page

**Test: TestCase2.py**
- Test case uses the Selenium IDE with Firefox and Python plugin
- The test is used to see if the appropriate error messages are displayed on the site when a logged in user tries to use the voting system on the projects page incorrectly
- The user is only allowed to vote up or down once for a project
- Example: alert messages on top of page indicate if the user already voted for the project


>>>>>>> 73bfca18420c67b6048b9a4a6d45c31936e656d8
