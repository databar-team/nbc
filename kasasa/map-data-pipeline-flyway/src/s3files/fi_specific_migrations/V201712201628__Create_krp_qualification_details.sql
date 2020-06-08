-- This table is being used in MAP Adpotion campaign
CREATE TABLE IF NOT EXISTS krp_qualifications_details
(
	financial_institution_id  bigint         NOT NULL,
	cycle_id_config           bigint         NOT NULL,
	account_kasasakey         varchar(100)   NOT NULL,
	product_id_config         bigint         NOT NULL,
	qualifying_level          bigint         NOT NULL,
	qualifier_type            varchar(100)   NOT NULL,
	qualifier_target          varchar(100)   NOT NULL,
	qualifier_actual          varchar(100)   NOT NULL,
	met_qualifier             boolean        NOT NULL,
	file_creation_date_time   timestamp      NOT NULL
	,PRIMARY KEY (financial_institution_id, cycle_id_config, account_kasasakey, product_id_config, qualifying_level, qualifier_type)
)ENGINE=InnoDB DEFAULT CHARSET=utf8
;
