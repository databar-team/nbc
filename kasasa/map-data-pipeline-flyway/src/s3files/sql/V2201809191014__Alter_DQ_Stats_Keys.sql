ALTER TABLE `data_quality`.`stats`
DROP PRIMARY KEY;

ALTER TABLE `data_quality`.`stats`
ADD COLUMN `sequence_id` INT AUTO_INCREMENT PRIMARY KEY FIRST,
ADD COLUMN `time_inserted` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;
