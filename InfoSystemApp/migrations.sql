--
-- Create model Device
--
CREATE TABLE `Devices` (`device_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `device_name` varchar(254) COLLATE `utf8mb3_general_ci` NOT NULL, `authentication_token` varchar(128) COLLATE `utf8mb3_general_ci` NULL, `creation_date` datetime(6) NOT NULL, `status` varchar(15) COLLATE `utf8mb3_general_ci` NOT NULL, `last_activity_time` datetime(6) NOT NULL, `location_name` varchar(254) COLLATE `utf8mb3_general_ci` NOT NULL, `location_latitude` numeric(10, 0) NULL, `location_longtitude` numeric(10, 0) NULL, `location_timestamp` datetime(6) NULL, `description` varchar(254) COLLATE `utf8mb3_general_ci` NULL);
--
-- Create model Parameter
--
CREATE TABLE `Parameters` (`parameter_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `parameter_name` varchar(254) COLLATE `utf8mb3_general_ci` NOT NULL, `parameter_symbol` varchar(25) COLLATE `utf8mb3_general_ci` NOT NULL, `device_id` integer NOT NULL);
--
-- Create model User
--
CREATE TABLE `Users` (`last_login` datetime(6) NULL, `user_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `username` varchar(254) COLLATE `utf8mb3_general_ci` NOT NULL UNIQUE, `password` varchar(254) COLLATE `utf8mb3_general_ci` NOT NULL, `salt` varchar(128) COLLATE `utf8mb3_general_ci` NOT NULL, `email` varchar(254) COLLATE `utf8mb3_general_ci` NOT NULL, `info` varchar(254) COLLATE `utf8mb3_general_ci` NULL, `is_staff` bool NOT NULL, `is_superuser` bool NOT NULL);
--
-- Create model SentData
--
CREATE TABLE `SentData` (`sent_data_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `timestamp` datetime(6) NOT NULL, `value` varchar(254) COLLATE `utf8mb3_general_ci` NOT NULL, `description` varchar(254) COLLATE `utf8mb3_general_ci` NULL, `parameter_id` integer NOT NULL);
--
-- Create model DeviceGroup
--
CREATE TABLE `DeviceGroups` (`device_group_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `device_group_name` varchar(50) COLLATE `utf8mb3_general_ci` NOT NULL, `status` varchar(15) COLLATE `utf8mb3_general_ci` NOT NULL, `creation_date` datetime(6) NOT NULL, `description` varchar(254) COLLATE `utf8mb3_general_ci` NULL, `user_id` integer NOT NULL);
--
-- Add field device_group to device
--
ALTER TABLE `Devices` ADD COLUMN `device_group_id` integer NOT NULL , ADD CONSTRAINT `Devices_device_group_id_f6941cc9_fk_DeviceGroups_device_group_id` FOREIGN KEY (`device_group_id`) REFERENCES `DeviceGroups`(`device_group_id`);
--
-- Create model DataFrame
--
CREATE TABLE `DataFrames` (`data_frame_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `timestamp` datetime(6) NOT NULL, `result` varchar(254) COLLATE `utf8mb3_general_ci` NOT NULL, `description` varchar(254) COLLATE `utf8mb3_general_ci` NULL, `parameter_id` integer NOT NULL);
ALTER TABLE `Parameters` ADD CONSTRAINT `Parameters_device_id_251abdb1_fk_Devices_device_id` FOREIGN KEY (`device_id`) REFERENCES `Devices` (`device_id`);
ALTER TABLE `DeviceGroups` ADD CONSTRAINT `DeviceGroups_user_id_2aec8c26_fk_Users_user_id` FOREIGN KEY (`user_id`) REFERENCES `Users` (`user_id`);
ALTER TABLE `SentData` ADD CONSTRAINT `SentData_parameter_id_d5cd6642_fk_Parameters_parameter_id` FOREIGN KEY (`parameter_id`) REFERENCES `Parameters` (`parameter_id`);
ALTER TABLE `DataFrames` ADD CONSTRAINT `DataFrames_parameter_id_c1073ca3_fk_Parameters_parameter_id` FOREIGN KEY (`parameter_id`) REFERENCES `Parameters` (`parameter_id`);
