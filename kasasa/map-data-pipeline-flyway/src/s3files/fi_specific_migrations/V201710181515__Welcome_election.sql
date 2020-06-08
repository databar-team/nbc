CREATE TABLE `customer_welcome_elections` (
    `customer_kasasa_key` varchar(100) NOT NULL,
    `product_record_id` VARCHAR(144) NOT NULL,
    `event_type` VARCHAR(100)  NOT NULL,
    `date_sent` date  NOT NULL,
    `status` ENUM('PENDING', 'SENT'	),
    `file_name` VARCHAR(100) NOT NULL,
    `date_modified` timestamp  NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE customer_attribute
ADD COLUMN welcome_election_product_record_id VARCHAR(144) GENERATED ALWAYS AS (attribute_object->'$.welcome_election_product_record_id') STORED AFTER customer_email_address
;