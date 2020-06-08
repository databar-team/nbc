ALTER TABLE `map_config`.`campaign_details`
DROP PRIMARY KEY,
add COLUMN product_guid varchar(36) NOT NULL AFTER campaign_name,
ADD PRIMARY KEY (customer_kasasakey, product_guid)
;