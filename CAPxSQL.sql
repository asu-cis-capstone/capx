/* SQL QUERIES */

DROP TABLE IF EXISTS PROJECT2 CASCADE;

CREATE TABLE PROJECT2 (
	id		serial		NOT NULL		PRIMARY KEY,
	company				varchar(50),
	description			varchar(300),
	comments 			varchar(300),
	rating 				smallint,
	tags 				varchar[20],
	dateCreated			date,
	semester			varchar(20),
	contact				varchar(60),
	email				varchar(100),
	phone				varchar(20),
	active				varchar(3))
	
	
INSERT INTO PROJECT2 (id, company, description, comments, rating) 
VALUES (1, 'Spark Open Research, LLC', 'Develop student user analytics and reporting on the Open edX platform. In this project, students will have the opportunity to develop open-source tools for educators and education researchers to allow them to better understand how students learn.', 'Project 1. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse enim justo, molestie in justo sed, malesuada euismod erat. Nam suscipit sed turpis convallis pulvinar. Cras gravida elit nisl, sit amet sodales erat molestie lacinia.', 5);
INSERT INTO PROJECT2 (id, company, description, comments, rating) 
VALUES (2, 'Aspen Systems, Inc.', 'The project presented by Aspen Systems is a native Android application used to help delivery truck drivers view customer information, view route information, allow customers to sign off on deliveries and other related actions.', 'Project 2. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse enim justo, molestie in justo sed, malesuada euismod erat. Nam suscipit sed turpis convallis pulvinar. Cras gravida elit nisl, sit amet sodales erat molestie lacinia.', 6);
INSERT INTO PROJECT2 (id, company, description, comments, rating) 
VALUES (3, 'ABC Company, LLC', 'Develop a website for an online retailer. Students will be expected to create an Android and iOS mobile app in order to let customers purchase products from their phone. A shopping cart will be required.', 'Project 3. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse enim justo, molestie in justo sed, malesuada euismod erat. Nam suscipit sed turpis convallis pulvinar. Cras gravida elit nisl, sit amet sodales erat molestie lacinia.', 2);
INSERT INTO PROJECT2 (id, company, description, comments, rating) 
VALUES (4, 'XYZ Clothin, Inc', 'Design a sales platform for a leading clothing business. Students will have the opportunity to visit our local factory and the project will require extensive front-end design to make our new website express our company style.', 'Project 4. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse enim justo, molestie in justo sed, malesuada euismod erat. Nam suscipit sed turpis convallis pulvinar. Cras gravida elit nisl, sit amet sodales erat molestie lacinia.', 0);

DROP TABLE IF EXISTS USERS CASCADE;

CREATE TABLE USERS (
	usertoken		varchar(100)		NOT NULL		PRIMARY KEY,
	votingArray		integer[300],
	githubname 		varchar(50),
	lastlogindate	date,
	lastlogintime	time,
	accountType		varchar(15)		default 'normal',
	placeholder2 	varchar(50),
	placeholder3 	smallint)
	
	
Drop TABLE IF EXISTS BLOG CASCADE;
	
CREATE TABLE BLOG (
	id		serial		NOT NULL		PRIMARY KEY,
	blogtitle		varchar(100),
	blogentry		varchar(1000),
	blogwriter		varchar(50),
	dateCreated		date,
	timeCreated		time)
	