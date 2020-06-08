CREATE TABLE `tasks` (
    `task_id` INT NOT NULL AUTO_INCREMENT,
    `description` VARCHAR(100) NOT NULL,
    PRIMARY KEY (`task_id`),
    UNIQUE KEY `unique_record_type_and_key` (`description`)
);

CREATE TABLE `task_last_run` (
    `run_id` INT NOT NULL AUTO_INCREMENT,
    `task_id` INT NOT NULL,
    `last_run_date_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`run_id`),
    UNIQUE KEY `unique_record_type_and_key` (`task_id`, `last_run_date_time`)
);

INSERT INTO `tasks` (`description`)
    VALUES ("Marketing Cloud Send")
;