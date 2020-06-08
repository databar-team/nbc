CREATE TABLE IF NOT EXISTS map_global_data.surrogate_person_link_mappings (
    `surrogate_id` BIGINT NOT NULL,
    `person_link_context_id` INT NOT NULL,
    `person_link_id` VARCHAR(32) NOT NULL,
    `financial_institution_id` INT(11),
    PRIMARY KEY(`surrogate_id`,`person_link_context_id`)
);