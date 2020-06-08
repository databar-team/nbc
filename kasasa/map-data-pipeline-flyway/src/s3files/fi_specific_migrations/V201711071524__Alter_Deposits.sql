ALTER TABLE deposits
add COLUMN available_balance NUMERIC(19, 2) NOT NULL 
AFTER branch;


