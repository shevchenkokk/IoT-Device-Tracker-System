SET GLOBAL general_log = 1;
SET GLOBAL general_log_file = 'Users/kirill/Documents/course_work_db/logfile.log';
SET GLOBAL general_log = 'ON';

SET SESSION character_set_server = 'utf8mb4';
DROP DATABASE IF EXISTS INFORMATION_SYSTEM_DB;

CREATE DATABASE INFORMATION_SYSTEM_DB
CHARACTER SET utf8mb4
COLLATE utf8mb4_bin;

USE INFORMATION_SYSTEM_DB;

DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS DeviceGroups;
DROP TABLE IF EXISTS Locations;
DROP TABLE IF EXISTS Devices;
DROP TABLE IF EXISTS Parameters;
DROP TABLE IF EXISTS DataFrames;

CREATE TABLE Users (
	user_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    username NVARCHAR(254) NOT NULL,
    password NVARCHAR(254) NOT NULL,
    salt NVARCHAR(128) NOT NULL,
    email NVARCHAR(254) NOT NULL,
    last_login DATETIME NULL,
    is_superuser BOOL NULL DEFAULT FALSE,
    is_staff BOOL NULL DEFAULT FALSE,
    info NVARCHAR(254) NULL DEFAULT 'Not specified'
);

CREATE TABLE DeviceGroups (
	device_group_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    device_group_name NVARCHAR(254) NOT NULL,
    user_id INT NOT NULL,
    CONSTRAINT FK_DeviceGroups_Users FOREIGN KEY (user_id)
    REFERENCES Users(user_id)
    ON DELETE CASCADE
    ON UPDATE RESTRICT,
    status NVARCHAR(15) NOT NULL,
    creation_date DATETIME NOT NULL,
    description NVARCHAR(254) NULL DEFAULT 'Not specified'
);

CREATE TABLE Devices (
	device_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	device_name NVARCHAR(254) NOT NULL,
    device_group_id INT NOT NULL,
	CONSTRAINT FK_Devices_DeviceGroups FOREIGN KEY (device_group_id)
    REFERENCES DeviceGroups(device_group_id)
    ON DELETE CASCADE
    ON UPDATE RESTRICT,
	creation_date DATETIME NOT NULL,
    authentication_token NVARCHAR(128) NULL,
    status NVARCHAR(15) NOT NULL,
    last_activity_time DATETIME NULL,
    location_name NVARCHAR(254) NOT NULL,
	location_latitude DECIMAL NULL,
    location_longtitude DECIMAL NULL,
    location_timestamp DATETIME NULL,
    description NVARCHAR(255) NULL DEFAULT 'Not specified'
);

CREATE TABLE Parameters (
	parameter_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    parameter_name NVARCHAR(254) NOT NULL,
    parameter_symbol NVARCHAR(25) NOT NULL,
    device_id INT NOT NULL,
    CONSTRAINT FK_Parameters_Devices FOREIGN KEY (device_id)
    REFERENCES Devices(device_id)
    ON DELETE CASCADE
    ON UPDATE RESTRICT
);

CREATE TABLE DataFrames (
	data_frame_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    parameter_id INT NOT NULL,
    CONSTRAINT FK_DataFrames_Parameters FOREIGN KEY (parameter_id)
    REFERENCES Parameters(parameter_id)
    ON DELETE CASCADE
    ON UPDATE RESTRICT,
    timestamp DATETIME NOT NULL,
    result NVARCHAR(254) NOT NULL,
    description NVARCHAR(254) NULL DEFAULT 'Not specified'
);

CREATE TABLE SentData (
	sent_data_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	parameter_id INT NOT NULL,
    CONSTRAINT FK_SentData_Parameters FOREIGN KEY (parameter_id)
    REFERENCES Parameters(parameter_id)
	ON DELETE CASCADE
    ON UPDATE RESTRICT,
	timestamp DATETIME NOT NULL,
	value NVARCHAR(254) NOT NULL,
	description NVARCHAR(254) NULL DEFAULT 'Not specified'
);

SELECT * FROM Users;
SELECT * FROM DeviceGroups;
SELECT * FROM Devices;
SELECT * FROM Parameters;
SELECT * FROM DataFrames;

