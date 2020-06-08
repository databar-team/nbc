-- This table is being used in MAP Adpotion campaign
CREATE TABLE IF NOT EXISTS config_product_mappings
(
	financial_institution_id            bigint         NOT NULL,
	core_product_code                   varchar(50)    NOT NULL,
	core_account_type                   varchar(10)    NOT NULL,
	kasasa_account_type                 varchar(40)    NOT NULL,
	product_type                        varchar(50),
	is_kasasa_powered_product           boolean        NOT NULL,
	is_kasasa_branded_product           boolean        NOT NULL,
	is_active_reward_processing         boolean        NOT NULL,
	financial_institution_product_name  varchar(100),
	product_classification_id           bigint         NOT NULL,
	product_id_config                   bigint,
	reward_processing_launch_date       date,
	file_creation_date_time             timestamp      NOT NULL
	,PRIMARY KEY (financial_institution_id, core_product_code, core_account_type)
)ENGINE=InnoDB DEFAULT CHARSET=utf8
;