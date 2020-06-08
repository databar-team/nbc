ALTER TABLE emails
ADD COLUMN key_type varchar(25) NOT NULL FIRST,
ADD COLUMN kasasakey varchar(100) NOT NULL AFTER key_type,
DROP COLUMN customer_kasasa_key