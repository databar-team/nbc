CREATE TABLE kasasa_product_min_akk_start_dates
(
    account_kasasakey varchar(100) NOT NULL,
    kasasa_product_type varchar(50) NULL,
    kasasa_product_id int(11) NULL,
    event_effective_date date NOT NULL,
    UNIQUE (account_kasasakey, kasasa_product_type, event_effective_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;