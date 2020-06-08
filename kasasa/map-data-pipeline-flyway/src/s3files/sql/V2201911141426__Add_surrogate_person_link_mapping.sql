CREATE TABLE IF NOT EXISTS map_config.person_link_context (
    `person_link_context_id` INT NOT NULL,
    `context_description` VARCHAR(4000) NOT NULL,
    PRIMARY KEY (`person_link_context_id`),
    INDEX `person_link_context_id_idx` (`person_link_context_id` ASC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

CREATE TABLE IF NOT EXISTS map_config.surrogate_to_person_link (
    `surrogate_id` BIGINT NOT NULL,
    `person_link_id` VARCHAR(40) NOT NULL,
    `person_link_context_id` INT NOT NULL,
    PRIMARY KEY (`surrogate_id`, `person_link_id`),
    CONSTRAINT `person_link_context_id`
        FOREIGN KEY (`person_link_context_id`)
        REFERENCES `map_config`.`person_link_context` (`person_link_context_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;