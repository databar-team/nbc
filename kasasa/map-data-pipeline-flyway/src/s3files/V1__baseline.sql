CREATE TABLE `accounts` (
  `customer_account_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_kasasa_key` varchar(100) NOT NULL,
  `account_kasasa_key` varchar(100) NOT NULL,
  `branch_code` varchar(100) NOT NULL,
  `kasasa_product_class` varchar(50) NOT NULL,
  `kasasa_product_status` varchar(50) NOT NULL,
  `product_kasasa_key` varchar(100) NOT NULL,
  `kasasa_account_type` varchar(75) NOT NULL,
  `is_kasasa_powered` char(1) NOT NULL,
  `estatement_flag` char(1) DEFAULT NULL,
  `product_status` varchar(50) NOT NULL,
  `open_date` date DEFAULT NULL,
  `closed_date` date DEFAULT NULL,
  `kasasa_relationship_code` varchar(25) NOT NULL,
  `kasasa_product_launch_date` date DEFAULT NULL,
  `customer_since_date` date DEFAULT NULL,
  `first_start_date_as_this_kasasa_product` date DEFAULT NULL,
  `first_start_date_as_any_kasasa_product` date DEFAULT NULL,
  `core_processing_date` date NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `created_by` varchar(45) DEFAULT NULL,
  `created_datetime` datetime DEFAULT NULL,
  `last_modified_by` varchar(45) DEFAULT NULL,
  `last_modified_datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`customer_kasasa_key`,`account_kasasa_key`,`product_kasasa_key`,`kasasa_relationship_code`,`core_processing_date`),
  UNIQUE KEY `customer_account_id` (`customer_account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `branch` (
  `branch_id` varchar(100) NOT NULL,
  `branch_no` int(11) NOT NULL,
  `financial_institution_id` int(11) NOT NULL,
  `fi_cert_no` int(11) DEFAULT NULL,
  `fi_type` varchar(50) DEFAULT NULL,
  `main_office` bit(1) DEFAULT b'0',
  `branch_name` varchar(45) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date DEFAULT NULL,
  `created_by` varchar(45) DEFAULT NULL,
  `created_datetime` datetime DEFAULT NULL,
  `last_modified_by` varchar(45) DEFAULT NULL,
  `last_modified_datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`branch_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `branch_address` (
  `branch_address_id` int(11) NOT NULL AUTO_INCREMENT,
  `branch_id` varchar(100) NOT NULL,
  `address_1` varchar(100) DEFAULT NULL,
  `address_2` varchar(100) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `state` varchar(45) NOT NULL,
  `zipcode` varchar(5) DEFAULT NULL,
  `zipcode_extended` varchar(4) DEFAULT NULL,
  `county` varchar(3) DEFAULT NULL,
  `distance` varchar(5) DEFAULT NULL,
  `urbanicity` varchar(15) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `created_by` varchar(45) DEFAULT NULL,
  `created_datetime` datetime DEFAULT NULL,
  `last_modified_by` varchar(45) DEFAULT NULL,
  `last_modified_datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`branch_address_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

CREATE TABLE `campaign` (
  `campaign_id` int(11) NOT NULL AUTO_INCREMENT,
  `campaign_name` varchar(100) NOT NULL,
  `financial_institution_id` int(11) NOT NULL,
  `campaign_begin_date` date DEFAULT NULL,
  `campaign_end_date` date DEFAULT NULL,
  `campaign_unique_details` varchar(200) NOT NULL,
  `created_by` varchar(45) DEFAULT NULL,
  `created_datetime` datetime DEFAULT NULL,
  `last_modified_by` varchar(45) DEFAULT NULL,
  `last_modified_datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`campaign_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `customer` (
  `customer_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_kasasa_key` varchar(100) NOT NULL,
  `kasasa_master_person_id` varchar(100) NOT NULL,
  `fico_individual_id` varchar(12) NOT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `middle_name` varchar(30) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `suffix` varchar(10) DEFAULT NULL,
  `created_by` varchar(45) DEFAULT NULL,
  `created_datetime` datetime DEFAULT NULL,
  `last_modified_by` varchar(45) DEFAULT NULL,
  `last_modified_datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `deleted_by` varchar(45) DEFAULT NULL,
  `deleted_datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`customer_kasasa_key`),
  UNIQUE KEY `customer_id` (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=32705 DEFAULT CHARSET=utf8;

CREATE TABLE `customer_address` (
  `address_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_kasasa_key` varchar(100) NOT NULL,
  `address_1` varchar(100) DEFAULT NULL,
  `address_2` varchar(100) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `state` varchar(25) DEFAULT NULL,
  `zipcode` varchar(5) DEFAULT NULL,
  `zipcode_extended` varchar(4) DEFAULT NULL,
  `delivery_point_bar_code` int(11) DEFAULT NULL,
  `carrier_route_code` varchar(10) DEFAULT NULL,
  `line_of_travel` varchar(10) DEFAULT NULL,
  `national_change_of_address_move_flag` char(1) DEFAULT NULL,
  `national_change_of_address_move_date` date DEFAULT NULL,
  `national_change_of_address_drop_flag` char(1) DEFAULT NULL,
  `advantage_target_narrow_band_income` char(1) DEFAULT NULL,
  `advantage_target_income_indicator` char(1) DEFAULT NULL,
  `house_hold_type_code` smallint(6) DEFAULT NULL,
  `geo_code_census_tract_block_number_area` smallint(6) DEFAULT NULL,
  `geo_code_block_group` smallint(6) DEFAULT NULL,
  `geo_code_census_state_code` smallint(6) DEFAULT NULL,
  `geo_code_census_county_code` smallint(6) DEFAULT NULL,
  `geo_code_neilsen_county_size_code` char(1) DEFAULT NULL,
  `geo_code_dma_code` smallint(6) DEFAULT NULL,
  `advantage_dwelling_type` smallint(6) DEFAULT NULL,
  `advantage_dwelling_type_indicator` char(1) DEFAULT NULL,
  `individual_age_ccyymm` varchar(50) DEFAULT NULL,
  `distance_to_branch` decimal(5,1) DEFAULT NULL,
  `time_zone` char(1) DEFAULT NULL,
  `wireless_flag` char(1) DEFAULT NULL,
  `decile` int(11) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `created_by` varchar(45) DEFAULT NULL,
  `created_datetime` datetime DEFAULT NULL,
  `last_modified_by` varchar(45) DEFAULT NULL,
  `last_modified_datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deleted_by` varchar(45) DEFAULT NULL,
  `deleted_datetime` datetime DEFAULT NULL,
  UNIQUE KEY `address_id` (`address_id`)
) ENGINE=InnoDB AUTO_INCREMENT=32703 DEFAULT CHARSET=utf8;

CREATE TABLE `customer_email` (
  `email_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_kasasa_key` varchar(100) NOT NULL,
  `email_address` varchar(100) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `primary_flag` char(1) DEFAULT NULL,
  `email_address_append_flag` char(1) DEFAULT NULL,
  `created_by` varchar(45) DEFAULT NULL,
  `created_datetime` datetime DEFAULT NULL,
  `last_modified_by` varchar(45) DEFAULT NULL,
  `last_modified_datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `email_id` (`email_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3729 DEFAULT CHARSET=utf8;

CREATE TABLE `customer_phone` (
  `phone_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_kasasa_key` varchar(100) NOT NULL,
  `phone_number` varchar(10) DEFAULT NULL,
  `primary_phone_flag` char(1) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `created_by` varchar(45) DEFAULT NULL,
  `created_datetime` datetime DEFAULT NULL,
  `last_modified_by` varchar(45) DEFAULT NULL,
  `last_modified_datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deleted_by` varchar(45) DEFAULT NULL,
  `deleted_datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`phone_id`),
  UNIQUE KEY `perosn_phone_id` (`phone_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `customer_score` (
  `score_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_kasasa_key` varchar(100) NOT NULL,
  `customer_score` smallint(6) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `created_by` varchar(45) DEFAULT NULL,
  `created_datetime` datetime DEFAULT NULL,
  `last_modified_by` varchar(45) DEFAULT NULL,
  `last_modified_datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deleted_datetime` datetime DEFAULT NULL,
  `deleted_by` varchar(45) DEFAULT NULL,
  UNIQUE KEY `customer_score_id` (`score_id`),
  KEY `customer_kasasa_key` (`customer_kasasa_key`),
  CONSTRAINT `customer_score_ibfk_1` FOREIGN KEY (`customer_kasasa_key`) REFERENCES `customer` (`customer_kasasa_key`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `fico_sourced_customers` (
  `financial_institution_id` int(11) NOT NULL,
  `customer_kasasa_key` varchar(100) NOT NULL,
  `fico_individual_id` varchar(12) NOT NULL,
  `kasasa_master_person_id` varchar(100) NOT NULL,
  `fico_file_name` varchar(100) NOT NULL,
  `data_load_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `fico_sourced_prospects` (
  `prospect_kasasa_key` varchar(100) NOT NULL,
  `financial_institution_id` int(11) NOT NULL,
  `branch_id` varchar(100) NOT NULL,
  `fico_individual_id` varchar(12) NOT NULL,
  `kasasa_master_person_id` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `middle_name` varchar(30) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `suffix` varchar(10) DEFAULT NULL,
  `address_1` varchar(100) DEFAULT NULL,
  `address_2` varchar(100) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `state` char(2) DEFAULT NULL,
  `zipcode` varchar(5) DEFAULT NULL,
  `zipcode_extended` varchar(4) DEFAULT NULL,
  `delivery_point_bar_code` int(11) DEFAULT NULL,
  `carrier_route_code` varchar(10) DEFAULT NULL,
  `line_of_travel` varchar(10) DEFAULT NULL,
  `national_change_of_address_move_flag` char(1) DEFAULT NULL,
  `national_change_of_address_move_date` date DEFAULT NULL,
  `national_change_of_address_drop_flag` char(1) DEFAULT NULL,
  `advantage_target_narrow_band_income` char(1) DEFAULT NULL,
  `advantage_target_income_indicator` char(1) DEFAULT NULL,
  `house_hold_type_code` smallint(6) DEFAULT NULL,
  `geo_code_census_tract_block_number_area` smallint(6) DEFAULT NULL,
  `geo_code_block_group` smallint(6) DEFAULT NULL,
  `geo_code_census_state_code` smallint(6) DEFAULT NULL,
  `geo_code_census_county_code` smallint(6) DEFAULT NULL,
  `geo_code_neilsen_county_size_code` char(1) DEFAULT NULL,
  `geo_code_dma_code` smallint(6) DEFAULT NULL,
  `advantage_dwelling_type` smallint(6) DEFAULT NULL,
  `advantage_dwelling_type_indicator` char(1) DEFAULT NULL,
  `individual_age_ccyymm` varchar(50) DEFAULT NULL,
  `distance_to_branch` decimal(5,1) DEFAULT NULL,
  `time_zone` char(1) DEFAULT NULL,
  `wireless_flag` char(1) DEFAULT NULL,
  `decile` int(11) DEFAULT NULL,
  `fico_file_name` varchar(100) NOT NULL,
  `expiration_date` date DEFAULT NULL,
  `data_load_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `financial_institution` (
  `financial_institution_id` int(11) NOT NULL,
  `financial_institution_long_name` varchar(100) DEFAULT NULL,
  `financial_institution_short_name` varchar(45) DEFAULT NULL,
  `created_by` varchar(45) DEFAULT NULL,
  `created_datetime` datetime DEFAULT NULL,
  `last_modified_by` varchar(45) DEFAULT NULL,
  `last_modified_datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`financial_institution_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `message_details` (
  `message_details_id` int(11) NOT NULL AUTO_INCREMENT,
  `vendor_product_id` int(11) NOT NULL,
  `vendor_item_id` int(11) NOT NULL,
  `vendor_object_id` int(11) NOT NULL,
  `product_class` varchar(50) NOT NULL,
  `short_code` varchar(50) NOT NULL,
  `financial_institution_id` int(11) NOT NULL,
  `marketing_message_name` varchar(100) NOT NULL,
  `used_by_vendor_asset` varchar(100) NOT NULL,
  PRIMARY KEY (`vendor_product_id`,`vendor_item_id`,`vendor_object_id`),
  UNIQUE KEY `message_details_id` (`message_details_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `product_details` (
  `product_details_id` int(11) NOT NULL AUTO_INCREMENT,
  `vendor_item_id` int(11) NOT NULL,
  `kasasa_product_guid` varchar(100) NOT NULL,
  `financial_institution_id` int(11) DEFAULT NULL,
  `product_class` varchar(50) NOT NULL,
  `product_name` varchar(50) NOT NULL,
  `product_status` varchar(50) NOT NULL,
  `order_priority` smallint(6) DEFAULT NULL,
  `marketability_of_product` char(1) DEFAULT NULL,
  PRIMARY KEY (`kasasa_product_guid`,`product_class`,`vendor_item_id`),
  UNIQUE KEY `product_details_id` (`product_details_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `prospect_customer_mapping` (
  `prospect_customer_map_id` int(11) NOT NULL AUTO_INCREMENT,
  `prospect_kasasa_key` varchar(100) NOT NULL,
  `customer_kasasa_key` varchar(100) NOT NULL,
  `financial_institution_id` int(11) NOT NULL,
  `data_load_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `prospect_customer_map_id` (`prospect_customer_map_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
