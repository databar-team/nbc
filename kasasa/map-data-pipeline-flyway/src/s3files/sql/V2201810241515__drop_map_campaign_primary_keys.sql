ALTER TABLE `map_campaign`.`livetech_mailing_list`
DROP PRIMARY KEY;

ALTER TABLE `map_campaign`.`livetech_prospects`
DROP PRIMARY KEY;

ALTER TABLE `map_campaign`.`livetech_mailing_list`
CHANGE COLUMN `list_id` `list_id` VARCHAR(100) NULL ,
CHANGE COLUMN `customer_kasasakey` `customer_kasasakey` VARCHAR(100) NULL ,
CHANGE COLUMN `list_name` `list_name` VARCHAR(100) NULL ,
CHANGE COLUMN `financial_institution_id` `financial_institution_id` BIGINT(20) NULL ;

ALTER TABLE `map_campaign`.`livetech_prospects`
DROP COLUMN `customer_kasasakey`,
CHANGE COLUMN `prospect_kasasa_key` `prospect_kasasa_key` VARCHAR(100) NOT NULL ,
ADD PRIMARY KEY (`prospect_kasasa_key`, `load_date_time`);