-- This table is being used in MAP Adpotion campaign
CREATE TABLE IF NOT EXISTS krp_overall_qualifications
(
 	account_kasasakey 			VARCHAR(100) NOT NULL,
	financial_institution_id 	BIGINT NOT NULL,
	cycle_id_config 			BIGINT NOT NULL,
	product_id_config 			BIGINT NOT NULL,
	highest_qualifying_level 	BIGINT NOT NULL,
	met_quals 					BOOLEAN NOT NULL,
	auto_qual 					BOOLEAN NOT NULL,
	qual_override 				VARCHAR(50) NOT NULL,
	final_qualification 		BOOLEAN NOT NULL,
	file_creation_date_time 	TIMESTAMP NOT NULL
	,PRIMARY KEY (account_kasasakey,financial_institution_id,cycle_id_config,product_id_config)
)ENGINE=InnoDB DEFAULT CHARSET=utf8
;