-- This table will contain the email suppression list from shared services and will be joined 
-- to the customer attribute process to determine which emails to scrub from the customer file.
CREATE TABLE IF NOT EXISTS `map_config`.`email_permanent_suppression` (
   ID int NOT NULL AUTO_INCREMENT,
   reason varchar(10),
   fi_id INT DEFAULT 0, -- Zero FiId means global
   email_id varchar(1000) NOT NULL,
   create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY(ID),
   UNIQUE UI_FiId_EmailId(fi_id,email_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;