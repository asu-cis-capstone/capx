/* SQL QUERIES */

DROP TABLE IF EXISTS PROJECT2 CASCADE;

CREATE TABLE project2
(
  id serial NOT NULL,
  company character varying(50),
  description character varying(300),
  comments character varying(300),
  rating smallint,
  tags character varying[],
  datecreated date,
  semester character varying(20),
  contact character varying(60),
  email character varying(100),
  phone character varying(20),
  active character varying(3),
  title character varying(100),
  interested character varying[],
  extension character varying(10),
  editstatus character varying(3),
  CONSTRAINT project2_pkey PRIMARY KEY (id)
)

  
DROP TABLE IF EXISTS USERS CASCADE;

CREATE TABLE users
(
  usertoken character varying(100) NOT NULL,
  votingarray integer[],
  githubname character varying(50),
  lastlogindate date,
  lastlogintime time without time zone,
  accounttype character varying(15) DEFAULT 'normal'::character varying,
  placeholder2 character varying(50),
  placeholder3 smallint,
  CONSTRAINT users_pkey PRIMARY KEY (usertoken)
)
	
	
Drop TABLE IF EXISTS BLOG CASCADE;
	
CREATE TABLE blog
(
  id serial NOT NULL,
  blogtitle character varying(100),
  blogentry character varying(1000),
  blogwriter character varying(50),
  datecreated date,
  timecreated time without time zone,
  editstatus character varying(3),
  active character varying(3) DEFAULT 'yes'::character varying,
  CONSTRAINT blog_pkey PRIMARY KEY (id)
)