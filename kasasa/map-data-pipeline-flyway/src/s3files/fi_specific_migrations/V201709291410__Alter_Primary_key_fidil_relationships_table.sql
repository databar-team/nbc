ALTER TABLE fidil_relationships DROP PRIMARY KEY;

ALTER TABLE fidil_relationships ADD PRIMARY KEY (account_kasasakey, customer_kasasakey, kasasa_relationship_code);
