CREATE TABLE `customer_attribute_hashes` (
    `customer_kasasa_key` VARCHAR(100) NOT NULL,
    `hash` VARCHAR(255) NOT NULL,
    `date_last_updated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (customer_kasasa_key)
);
