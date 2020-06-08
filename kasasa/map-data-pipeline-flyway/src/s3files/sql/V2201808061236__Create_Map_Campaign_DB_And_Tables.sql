-- Create new database to house campaign data from vendors
CREATE DATABASE IF NOT EXISTS map_campaign
;


-- mailing list data
CREATE TABLE IF NOT EXISTS `map_campaign`.`livetech_mailing_list` 
(
    `list_id` VARCHAR(100) NOT NULL,
    `customer_kasasakey` VARCHAR(100) NOT NULL,
    `list_name` VARCHAR(100) NOT NULL,
    `financial_institution_id` BIGINT NOT NULL,
    `load_date_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (customer_kasasakey, load_date_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;


-- prospects data
CREATE TABLE IF NOT EXISTS `map_campaign`.`livetech_prospects` 
(
    `customer_kasasakey` VARCHAR(100) NOT NULL,
    `prospect_kasasa_key` VARCHAR(100) NOT NULL,
    `kasasa_master_person_id` VARCHAR(100) NOT NULL,
    `full_name` VARCHAR(100) NULL,
    `first_name` VARCHAR(50) NULL,
    `middle_name` VARCHAR(30) NULL,
    `last_name` VARCHAR(50) NULL,
    `suffix` VARCHAR(10) NULL,
    `address_2` VARCHAR(100) NULL,
    `address_1` VARCHAR(100) NULL,
    `city` VARCHAR(50) NULL,
    `state` CHAR(2) NULL,
    `zipcode` VARCHAR(5) NULL,
    `zipcode_extended` VARCHAR(4) NULL,
    `delivery_point_bar_code` INT(11) NULL,
    `carrier_route_code` VARCHAR(10) NULL,
    `line_of_travel` VARCHAR(10) NULL,
    `fico_individual_id` VARCHAR(12) NOT NULL,
    `financial_institution_id` BIGINT NOT NULL,
    `branch_id` VARCHAR(100) NULL,
    `email` VARCHAR(100) NULL,
    `expiration_date` DATE NULL,
    `distance_to_branch` DECIMAL(5,1) NULL,
    `load_date_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (customer_kasasakey, load_date_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;


-- customer data
CREATE TABLE IF NOT EXISTS `map_campaign`.`livetech_customers` 
(
    `customer_kasasakey` VARCHAR(100) NOT NULL,
    `financial_institution_id` BIGINT,
    `kasasa_master_person_id` VARCHAR(100) NOT NULL,
    `full_name` VARCHAR(100) NULL,
    `first_name` VARCHAR(50) NULL,
    `middle_name` VARCHAR(30) NULL,
    `last_name` VARCHAR(50) NULL,
    `suffix` VARCHAR(10) NULL,
    `address_2` VARCHAR(100) NULL,
    `address_1` VARCHAR(100) NULL,
    `city` VARCHAR(50) NULL,
    `state` CHAR(2) NULL,
    `zipcode` VARCHAR(5) NULL,
    `zipcode_extended` VARCHAR(4) NULL,
    `delivery_point_bar_code`INT(11),
    `carrier_route_code` VARCHAR(10) NULL,
    `line_of_travel` VARCHAR(10) NULL,
    `fico_individual_id` VARCHAR(12) NOT NULL,
    `email` VARCHAR(100) NULL,
    `phone_number` VARCHAR(10) NULL,
    `cm_birthday` VARCHAR(100) NULL,
    `cm_anniversary` VARCHAR(100) NULL,
    `cm_welcome` VARCHAR(100) NULL,
    `cm_adoption` VARCHAR(100) NULL,
    `cm_retention` VARCHAR(100) NULL,
    `cm_cross_sell_email` VARCHAR(100) NULL,
    `cm_cross_sell_direct` VARCHAR(100) NULL,
    `load_date_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (customer_kasasakey, load_date_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;