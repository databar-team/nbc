CREATE TABLE primary_relationships
(
    account_kasasakey varchar(100) NOT NULL,
    customer_kasasakey varchar(100) NOT NULL,
    PRIMARY KEY (account_kasasakey, customer_kasasakey)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;