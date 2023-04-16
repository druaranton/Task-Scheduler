DROP DATABASE IF EXISTS `app`;
CREATE DATABASE IF NOT EXISTS `app`;
USE `app`;

--Create Tables
CREATE TABLE IF NOT EXISTS `category` ( 
	`category_id` INT(5) AUTO_INCREMENT, 
	`category_name` VARCHAR(15) NOT NULL, 
	CONSTRAINT category_categoryid_pk PRIMARY KEY (category_id) );

CREATE TABLE IF NOT EXISTS `task` ( 
	`task_id` INT(5) NOT NULL AUTO_INCREMENT, 
	`title` VARCHAR(30) NOT NULL, 
	`description` VARCHAR(100) NOT NULL, 
	`date_created` DATE NOT NULL DEFAULT CURDATE(),
	`deadline_date` DATE,
	`status` TINYINT(1) NOT NULL DEFAULT 0,
	`category_id` INT(5),
	CONSTRAINT task_taskid_pk PRIMARY KEY (task_id),
	CONSTRAINT task_categoryid_fk FOREIGN KEY(category_id) REFERENCES category(category_id) );
