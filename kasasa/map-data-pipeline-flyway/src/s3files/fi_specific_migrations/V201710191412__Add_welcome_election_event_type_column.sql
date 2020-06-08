ALTER TABLE customer_attribute
ADD COLUMN welcome_election_event_type VARCHAR(100) GENERATED ALWAYS AS (attribute_object->'$.welcome_election_event_type') STORED AFTER welcome_election_product_record_id
;
