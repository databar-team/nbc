-- due to previous primary key, records were being dropped (case ignorant string compares in core_product_code).
-- product_classification_id appears to be the FK from KRP for this table, making it the key
ALTER TABLE config_product_mappings DROP PRIMARY KEY;

ALTER TABLE config_product_mappings ADD PRIMARY KEY (product_classification_id)