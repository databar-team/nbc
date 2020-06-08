-- This table is being used in MAP Adpotion campaign
CREATE TABLE IF NOT EXISTS config_cycles
(
	financial_institution_id  bigint      NOT NULL,
	cycle_set_id              bigint      NOT NULL,
	cycle_id_config           bigint      NOT NULL,
	drop_date                 date        NOT NULL,
	second_drop_date          date        NOT NULL,
	statement_date_start      date        NOT NULL,
	statement_date_end        date        NOT NULL,
	qualification_date_start  date        NOT NULL,
	qualification_date_end    date        NOT NULL,
	earnings_date_start       date        NOT NULL,
	earnings_date_end         date        NOT NULL,
	file_creation_date_time   timestamp   NOT NULL
	,PRIMARY KEY (financial_institution_id, cycle_set_id, cycle_id_config)
)ENGINE=InnoDB DEFAULT CHARSET=utf8
;
