-- This table is being used in MAP Email Hygiene project
-- for the purpose of capturing rules from the following S3 files:
-- domain.csv
-- business.csv
-- explicit.csv
-- mailbox.csv
-- And potentially others in the future - such as SparkPost Suppression List(s)

CREATE TABLE IF NOT EXISTS `map_config`.`email_hygiene_rules` 
(
	src_file_id SMALLINT NOT NULL,
	rule varchar(256) NOT NULL,
	dt_upload DATETIME NULL default CURRENT_TIMESTAMP,
	PRIMARY KEY (src_file_id, rule)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;
