CREATE DATABASE IF NOT EXISTS livetech;

CREATE TABLE IF NOT EXISTS livetech.events_login_success (
  `message_id` int(11) NOT NULL AUTO_INCREMENT,
  `entity_id` int(11) DEFAULT NULL,
  `entity_name` varchar(250) DEFAULT NULL,
  `user_id` varchar(250) DEFAULT NULL,
  `host` varchar(250) NOT NULL,
  `url` varchar(250) DEFAULT NULL,
  `system_id` int(11) DEFAULT NULL,
  `system_name` varchar(250) DEFAULT NULL,
  `timestamp` timestamp NOT NULL,
  PRIMARY KEY (`message_id`),
  UNIQUE KEY `message_id_UNIQUE` (`message_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE DATABASE IF NOT EXISTS map_config;

CREATE TABLE IF NOT EXISTS map_config.feature_signup (
  `financial_institution_id` int(11) NOT NULL,
  `feature_name` varchar(45) DEFAULT NULL,
  `active_start_date` date DEFAULT NULL,
  `active_end_date` date DEFAULT NULL,
  `created_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_by` varchar(45) DEFAULT 'SELECT  CURRENT_USER()',
  `modified_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `feature_signupcol` varchar(45) NOT NULL,
  `deleted_by` varchar(45) DEFAULT NULL,
  `deleted_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`financial_institution_id`),
  KEY `fi_feature` (`financial_institution_id`,`feature_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

