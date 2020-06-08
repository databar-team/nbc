ALTER TABLE `map_config`.`campaign_details`
DROP PRIMARY KEY,
ADD PRIMARY KEY (customer_kasasakey, product_guid, campaign_name)
;