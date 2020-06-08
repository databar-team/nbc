CREATE TABLE IF NOT EXISTS map_config.fico_orders_active (
  `order_id` INT NOT NULL AUTO_INCREMENT,
  `financial_institution_id` INT(11) NOT NULL,
  `order_size` INT(11) NOT NULL,
  `start_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `end_date` timestamp,
  `created_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_by` varchar(45) DEFAULT 'SELECT  CURRENT_USER()',
  `modified_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_by` VARCHAR(45) NULL,
  `deleted_date` TIMESTAMP NULL,
  PRIMARY KEY (`order_id`),
  INDEX `financial_institution_id_idx` (`financial_institution_id` ASC),
  CONSTRAINT `financial_institution_id`
    FOREIGN KEY (`financial_institution_id`)
    REFERENCES `map_config`.`feature_signup` (`financial_institution_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
