CAPx Repository
==============
 
Overview
=========
 
Develop a website specifically for the CIS 440 Capstone class. The site will allow both students and companies to post project opportunities. In addition, there will be an area that shows various past projects. Students will be able to view all available projects and rank them with a up/downvote system. Students will also be able to signup for projects directly on the site. Each project will have information provided by the company as well as Dr. Clark's comments. Additionally, each project will have Tags, giving a quick overview of the desired coding language, required technologies and other characteristics.
 
**Stable Release**
 https://stormy-atoll-5080.herokuapp.com/
 
**Beta Testing**
 https://capxtest.herokuapp.com/
 
 (more info coming soon!)
 
Product Backlog
========
[![Stories in Ready](https://badge.waffle.io/asu-cis-capstone/capx.png?label=ready&title=Ready)](https://waffle.io/asu-cis-capstone/capx) [![Stories In Progress](https://badge.waffle.io/asu-cis-capstone/capx.png?label=In%20Progress&title=In%20Progress)](https://waffle.io/asu-cis-capstone/capx) [![Stories in Testing](https://badge.waffle.io/asu-cis-capstone/capx.png?label=testing&title=Testing)](https://waffle.io/asu-cis-capstone/capx)
 

How to Install (without GitHub Login)
==================
Please note that these instructions assume that you have initally set up Heroku with Python on your machine and are able to run Heroku commands from your Terminal application. Please visit [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#introduction) if this has not been set up. Follow the setup instructions through installing the Heroku ToolBelt, which will allow you to use Heroku commands within your terminal application.*
 
1. Download source from this GitHub repo
2. Create a database on Heroku via your Heroku profile.
3. Using PGAdmin, connect to your Heroku database and modify the following line of code in the app.py, to match your Heroku database variables.
![What to Edit](https://github.com/STruong1/CIS440-ScreenShots/blob/master/Images/Screen%20Shot%202015-02-08%20at%2011.47.45%20AM.png)
4. With PGAdmin, use the CAPxSQL.sql file to create the correct table, with its attributes, and some dummy data on your Heroku database from steps 2-3.  
5. In a new Terminal window, run the following commands: ***git init, git add -A, git commit -m 'some comment here', heroku create, git push heroku master***
6. Now navigate to your *Heroku Dashboard > Personal Apps* and a new app should be available in the *Personal Apps* list.
7. When launching the Heroku App from your dashboard, if you receive an application error and are operating under a free Heroku account, you will need to scale the web dynos to one. In order to do this, use the same terminal/command window from step five, and run the following command: ***heroku ps:scale web=1***

How to Install (with GitHub Login)
==================
1. Follow the same steps listed in the "How to Install (without GitHub Login)" section and while modifying the app.py file in step three, you'll also need to modify the following line of code to match the Client ID and Client Secret to match the ones that you were provided if you've registered your application with Github:
![What to Edit](https://github.com/STruong1/CIS440-ScreenShots/blob/master/Images/Screen%20Shot%202015-02-17%20at%209.09.10%20PM.png)
 
Contributors 
=======================
 
1. Steve Truong
2. Jose Recendez
3. Alex Neumann
4. Sneha Dadhania
5. Tom Rullestad
 
Release Notes
=========
 
**Release 0.1**
 
- Added site mockups
- Added live "Hello World" demo hosted via Heroku
- Created GitHub repo
- Created Waffle.io Task Board
 
**Release 0.2**
 
- Added technology stack diagram
- Added Procfile for Heroku
- Added SQL file for DB table and dummy data creation
- Updated live Heroku test site link (in overview)
  - Site now has HTML, CSS, & some JS
  - Content is read from PostgreSQL DB
- Updated "How to Install" section

**Release 0.3**
 
- Link to Google Form used for User Survey: http://goo.gl/forms/TEXaZuHtb6
- Updated the CAPx Test Site (capxtest.herokuapp.com)
 - Added content to "About & Contact" page
 - Added content to "Home" page
 - Added GitHub Login functionality
 - Fixed the Up/Down Vote issues 
