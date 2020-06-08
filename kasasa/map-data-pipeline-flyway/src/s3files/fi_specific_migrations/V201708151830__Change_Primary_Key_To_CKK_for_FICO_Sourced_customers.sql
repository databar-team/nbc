ALTER TABLE fico_sourced_customers DROP PRIMARY KEY;
ALTER TABLE fico_sourced_customers ADD PRIMARY KEY (customer_kasasa_key);
