/* SQL QUERIES */

DROP TABLE IF EXISTS PROJECT2 CASCADE;

CREATE TABLE PROJECT2 (
	id		serial		NOT NULL		PRIMARY KEY,
	company		varchar(50),
	description	varchar(300),
	comments varchar(300),
	rating smallint)
	
INSERT INTO PROJECT2 VALUES (1, 'Spark Open Research, LLC', 'Develop student user analytics...', 'Project 1. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse enim justo, molestie in justo sed, malesuada euismod erat. Nam suscipit sed turpis convallis pulvinar. Cras gravida elit nisl, sit amet sodales erat molestie lacinia.', 5);
INSERT INTO PROJECT2 VALUES (2, 'Aspen Systems, Inc.', 'The project presented by Aspen Systems is a native Android...', 'Project 2. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse enim justo, molestie in justo sed, malesuada euismod erat. Nam suscipit sed turpis convallis pulvinar. Cras gravida elit nisl, sit amet sodales erat molestie lacinia.', 6);
INSERT INTO PROJECT2 VALUES (3, 'ABC Company, LLC', 'Develop a website for an online retailer...', 'Project 3. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse enim justo, molestie in justo sed, malesuada euismod erat. Nam suscipit sed turpis convallis pulvinar. Cras gravida elit nisl, sit amet sodales erat molestie lacinia.', 2);
INSERT INTO PROJECT2 VALUES (4, 'XYZ Clothin, Inc', 'Design a sales platform for a leading clothing business...', 'Project 4. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse enim justo, molestie in justo sed, malesuada euismod erat. Nam suscipit sed turpis convallis pulvinar. Cras gravida elit nisl, sit amet sodales erat molestie lacinia.', 0);



CREATE TABLE USERS (
	usertoken		varchar(100)		NOT NULL		PRIMARY KEY,
	votingArray		integer[300],
	githubname 		varchar(50),
	placeholder1	varchar(50),
	placeholder2 	varchar(50),
	placeholder3 	smallint)
	
