CREATE TABLE `surrogates` (
    `surrogate_id` BIGINT NOT NULL,
    `key_type` VARCHAR(25) NOT NULL,
    `record_key` VARCHAR(100) NOT NULL,
    PRIMARY KEY (surrogate_id),
    UNIQUE KEY `unique_record_type_and_key` (`key_type`, `record_key`),
    INDEX (`key_type`, `record_key`)
);
