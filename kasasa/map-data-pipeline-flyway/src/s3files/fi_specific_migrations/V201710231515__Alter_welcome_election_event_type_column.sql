-- Data already exists in this table.  Add a column with not null is going fail.  So Truncate the table first and then do the alter.  Truncate is ok, because the data is Transient.
TRUNCATE TABLE customer_attribute;

ALTER TABLE customer_attribute
DROP COLUMN welcome_election_product_record_id,
DROP COLUMN welcome_election_event_type,
ADD COLUMN welcome_election_product_record_id VARCHAR(144) GENERATED ALWAYS AS (JSON_UNQUOTE(attribute_object->'$.welcome_election_product_record_id')) STORED AFTER customer_email_address,
ADD COLUMN welcome_election_event_type VARCHAR(100) GENERATED ALWAYS AS (JSON_UNQUOTE(attribute_object->'$.welcome_election_event_type')) STORED AFTER welcome_election_product_record_id
;