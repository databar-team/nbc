ALTER TABLE customer_attribute
ADD COLUMN date_of_birth VARCHAR(45)
GENERATED ALWAYS AS (attribute_object->'$.date_of_birth') STORED AFTER delete_date,
ADD INDEX date_of_birth (date_of_birth ASC);