-- This table is being used in MAP Adpotion campaign
-- for the purpose of persisting the touch count.
CREATE TABLE IF NOT EXISTS `map_config`.`campaign_details` 
(
	customer_kasasakey VARCHAR(100) NOT NULL,
	financial_institution_id BIGINT NOT NULL,
	campaign_name varchar(100) NOT NULL,
	touch_count SMALLINT NOT NULL DEFAULT 0,
	date_last_run DATE NULL,
	PRIMARY KEY (customer_kasasakey)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;