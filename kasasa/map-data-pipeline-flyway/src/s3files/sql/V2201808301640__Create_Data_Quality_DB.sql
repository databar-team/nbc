-- Create new database to house campaign data from vendors
CREATE DATABASE IF NOT EXISTS data_quality
;

-- create sources
CREATE TABLE IF NOT EXISTS `data_quality`.`sources`
(
    `source_id` BIGINT NOT NULL AUTO_INCREMENT,
    `source` VARCHAR(100) NOT NULL,
    PRIMARY KEY (source_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

-- seed sources
INSERT INTO `data_quality`.`sources` (source)
VALUES ('extract'),
    ('transform'),
    ('load'),
    ('vendor_in'),
    ('vendor_out'),
    ('processing_attributes'),
    ('processing_campaigns')
;

-- input stats
CREATE TABLE IF NOT EXISTS `data_quality`.`stats` 
(
    `source` VARCHAR(100) NOT NULL,
    `source_id` BIGINT NOT NULL,
    `fi_id` BIGINT NOT NULL,
    `file_type` VARCHAR(100) NOT NULL,
    `count` INT NOT NULL,
    `stats_object` JSON NULL,
    `date_loaded` DATE NOT NULL,
    PRIMARY KEY (source, source_id, fi_id, file_type, date_loaded)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;