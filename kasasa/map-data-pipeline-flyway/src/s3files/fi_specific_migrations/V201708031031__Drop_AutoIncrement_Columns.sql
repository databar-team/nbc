ALTER TABLE accounts DROP COLUMN customer_account_id;

ALTER TABLE branch_address DROP COLUMN branch_address_id;

ALTER TABLE branch_address ADD PRIMARY KEY (branch_id);

ALTER TABLE customer DROP COLUMN customer_id;

ALTER TABLE customer_address DROP COLUMN address_id;

ALTER TABLE customer_address ADD PRIMARY KEY (customer_kasasa_key);

ALTER TABLE customer_email DROP COLUMN email_id;

ALTER TABLE customer_email ADD PRIMARY KEY (customer_kasasa_key);

ALTER TABLE customer_phone DROP COLUMN phone_id;

ALTER TABLE customer_phone ADD PRIMARY KEY (customer_kasasa_key);

ALTER TABLE customer_score DROP COLUMN score_id;

ALTER TABLE customer_score ADD PRIMARY KEY (customer_kasasa_key);

ALTER TABLE product_details DROP COLUMN product_details_id;

ALTER TABLE prospect_customer_mapping DROP COLUMN prospect_customer_map_id;

ALTER TABLE prospect_customer_mapping ADD PRIMARY KEY (customer_kasasa_key);
