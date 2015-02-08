/* SQL QUERIES */
CREATE TABLE PROJECTTEMP (
	id			serial		NOT NULL	PRIMARY KEY,
	company		varchar(50),
	description	varchar(300),
	comments 	varchar(300))
	

INSERT INTO PROJECT VALUES (1, 'Spark Open Research, LLC', 'Develop student user analytics...', 'Project 1. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse enim justo, molestie in justo sed, malesuada euismod erat. Nam suscipit sed turpis convallis pulvinar. Cras gravida elit nisl, sit amet sodales erat molestie lacinia. Donec accumsan congue dolor, ut ullamcorper ligula ullamcorper eu. Vivamus mattis turpis id vestibulum lacinia. Pellentesque sit amet placerat orci. Quisque');
INSERT INTO PROJECT VALUES (2, 'Aspen Systems, Inc.', 'The project presented by Aspen Systems is a native Android...', 'Project 2. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse enim justo, molestie in justo sed, malesuada euismod erat. Nam suscipit sed turpis convallis pulvinar. Cras gravida elit nisl, sit amet sodales erat molestie lacinia. Donec accumsan congue dolor, ut ullamcorper ligula ullamcorper eu. Vivamus mattis turpis id vestibulum lacinia. Pellentesque sit amet placerat orci. Quisque');
INSERT INTO PROJECT VALUES (3, 'ABC Company, LLC', 'Develop a website for an online retailer...', 'Project 3. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse enim justo, molestie in justo sed, malesuada euismod erat. Nam suscipit sed turpis convallis pulvinar. Cras gravida elit nisl, sit amet sodales erat molestie lacinia. Donec accumsan congue dolor, ut ullamcorper ligula ullamcorper eu. Vivamus mattis turpis id vestibulum lacinia. Pellentesque sit amet placerat orci. Quisque');
INSERT INTO PROJECT VALUES (4, 'XYZ Clothin, Inc', 'Design a sales platform for a leading clothing business...', 'Project 4. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse enim justo, molestie in justo sed, malesuada euismod erat. Nam suscipit sed turpis convallis pulvinar. Cras gravida elit nisl, sit amet sodales erat molestie lacinia. Donec accumsan congue dolor, ut ullamcorper ligula ullamcorper eu. Vivamus mattis turpis id vestibulum lacinia. Pellentesque sit amet placerat orci. Quisque');

INSERT INTO PROJECTTEMP VALUES (1, 'Spark Open Research, LLC', 'Develop student user analytics...', 'Project 1. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse enim justo, molestie in justo sed, malesuada euismod erat. Nam suscipit sed turpis convallis pulvinar. Cras gravida elit nisl, sit amet sodales erat molestie lacinia.');
INSERT INTO PROJECTTEMP VALUES (2, 'Aspen Systems, Inc.', 'The project presented by Aspen Systems is a native Android...', 'Project 2. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse enim justo, molestie in justo sed, malesuada euismod erat. Nam suscipit sed turpis convallis pulvinar. Cras gravida elit nisl, sit amet sodales erat molestie lacinia.');
INSERT INTO PROJECTTEMP VALUES (3, 'ABC Company, LLC', 'Develop a website for an online retailer...', 'Project 3. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse enim justo, molestie in justo sed, malesuada euismod erat. Nam suscipit sed turpis convallis pulvinar. Cras gravida elit nisl, sit amet sodales erat molestie lacinia.');
INSERT INTO PROJECTTEMP VALUES (4, 'XYZ Clothin, Inc', 'Design a sales platform for a leading clothing business...', 'Project 4. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse enim justo, molestie in justo sed, malesuada euismod erat. Nam suscipit sed turpis convallis pulvinar. Cras gravida elit nisl, sit amet sodales erat molestie lacinia.');

DROP TABLE IF EXISTS PROJECT2 CASCADE;

CREATE TABLE PROJECT2 (
	id			serial		NOT NULL	PRIMARY KEY,
	company		varchar(50),
	description	varchar(300),
	comments 	varchar(300),
	rating 		smallint)
	
INSERT INTO PROJECT2 VALUES (1, 'Spark Open Research, LLC', 'Develop student user analytics...', 'Project 1. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse enim justo, molestie in justo sed, malesuada euismod erat. Nam suscipit sed turpis convallis pulvinar. Cras gravida elit nisl, sit amet sodales erat molestie lacinia.', 5);
INSERT INTO PROJECT2 VALUES (2, 'Aspen Systems, Inc.', 'The project presented by Aspen Systems is a native Android...', 'Project 2. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse enim justo, molestie in justo sed, malesuada euismod erat. Nam suscipit sed turpis convallis pulvinar. Cras gravida elit nisl, sit amet sodales erat molestie lacinia.', 6);
INSERT INTO PROJECT2 VALUES (3, 'ABC Company, LLC', 'Develop a website for an online retailer...', 'Project 3. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse enim justo, molestie in justo sed, malesuada euismod erat. Nam suscipit sed turpis convallis pulvinar. Cras gravida elit nisl, sit amet sodales erat molestie lacinia.', 2);
INSERT INTO PROJECT2 VALUES (4, 'XYZ Clothin, Inc', 'Design a sales platform for a leading clothing business...', 'Project 4. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse enim justo, molestie in justo sed, malesuada euismod erat. Nam suscipit sed turpis convallis pulvinar. Cras gravida elit nisl, sit amet sodales erat molestie lacinia.', 0);

INSERT INTO PROJECT2 VALUES (5, 'Test, Inc', 'Design a test...', 'Project 5. Lorem ipsum', 10);
