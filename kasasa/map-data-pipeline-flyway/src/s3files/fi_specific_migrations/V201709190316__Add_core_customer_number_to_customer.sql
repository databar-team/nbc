ALTER TABLE customer
ADD COLUMN core_customer_number VARCHAR(25) DEFAULT NULL AFTER date_of_birth;