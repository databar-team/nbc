-- Adding index to livetech tables for performance
ALTER TABLE `map_campaign`.`livetech_customers` ADD INDEX `index_fi_id` (`financial_institution_id`);

ALTER TABLE `map_campaign`.`livetech_mailing_list` ADD INDEX `index_fi_id` (`financial_institution_id`);
ALTER TABLE `map_campaign`.`livetech_mailing_list` ADD INDEX `index_load_date_time` (`load_date_time`);
ALTER TABLE `map_campaign`.`livetech_mailing_list` ADD INDEX `index_customer_kasasakey` (`customer_kasasakey`);


ALTER TABLE `map_campaign`.`livetech_prospects` ADD INDEX `index_fi_id` (`financial_institution_id`);
