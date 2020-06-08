-- Adding index to email suppression table for performance
ALTER TABLE `map_config`.`email_permanent_suppression` ADD INDEX `index_email_id` (`email_id`);
