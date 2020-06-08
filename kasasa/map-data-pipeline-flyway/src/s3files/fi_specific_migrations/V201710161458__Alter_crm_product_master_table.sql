-- Data already exists in this table.  Add a column with not null is going fail.  So Truncate the table first and then do the alter.  Truncate is ok, because the data is Transient.
TRUNCATE TABLE crm_product_master;

ALTER TABLE crm_product_master
ADD COLUMN `last_modified_datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP;
