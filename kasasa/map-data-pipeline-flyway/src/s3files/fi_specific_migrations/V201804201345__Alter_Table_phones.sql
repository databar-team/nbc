-- Data already exists in this table.  Add a column with not null is going fail.  So Truncate the table first and then do the alter.  Truncate is ok, because the data is Transient.
TRUNCATE TABLE phones;

ALTER TABLE phones
ADD COLUMN key_type varchar(25) NOT NULL FIRST,
ADD COLUMN kasasakey varchar(100) NOT NULL AFTER key_type,
DROP COLUMN customer_kasasa_key;

ALTER TABLE phones ADD PRIMARY KEY (kasasakey, key_type);