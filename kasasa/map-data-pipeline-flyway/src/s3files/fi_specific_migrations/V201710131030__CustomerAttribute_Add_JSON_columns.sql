-- While the purpose of JSON datatype for column attribute_object is to unleash the unstructured feature.  So, that when new attribute is added there is no need to change the table structure.
-- Why are we adding these columns then?  Well, PO's do not need to learn about JSON Query!!! They would rather be comfortable running queries on structure db structure.

-- Data already exists in this table.  Add a column with not null is going fail.  So Truncate the table first and then do the alter.  Truncate is ok, because the data is Transient.
TRUNCATE TABLE customer_attribute;

ALTER TABLE customer_attribute
DROP INDEX date_of_birth,
DROP COLUMN date_of_birth,
ADD COLUMN customer_account_holder int(1) GENERATED ALWAYS AS (attribute_object->'$.customer_account_holder') STORED AFTER attribute_object,
ADD COLUMN customer_kasasa_account_holder int(1) GENERATED ALWAYS AS (attribute_object->'$.customer_kasasa_account_holder') STORED AFTER customer_account_holder,
ADD COLUMN customer_date_of_birth date GENERATED ALWAYS AS (JSON_UNQUOTE(attribute_object->'$.customer_date_of_birth')) STORED AFTER customer_kasasa_account_holder,
ADD COLUMN beta_customer_kasasa_start_date date GENERATED ALWAYS AS (JSON_UNQUOTE(attribute_object->'$.beta_customer_kasasa_start_date')) STORED AFTER customer_date_of_birth,
ADD COLUMN customer_kasasa_start_date date GENERATED ALWAYS AS (JSON_UNQUOTE(attribute_object->'$.customer_kasasa_start_date')) STORED AFTER beta_customer_kasasa_start_date,
ADD COLUMN customer_email_address varchar(100) GENERATED ALWAYS AS (JSON_UNQUOTE(attribute_object->'$.customer_email_address')) STORED AFTER customer_kasasa_start_date,
ADD INDEX customer_attribute_idx (customer_account_holder, customer_kasasa_account_holder, customer_date_of_birth)
;
