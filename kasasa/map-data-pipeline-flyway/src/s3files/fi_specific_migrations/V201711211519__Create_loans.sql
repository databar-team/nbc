CREATE TABLE IF NOT EXISTS loans
(
	account_kasasakey VARCHAR(100) NOT NULL,
	financial_institution_id BIGINT NOT NULL,
	core_processing_date DATE NOT NULL,
	core_account_number VARCHAR(25) NOT NULL,
	core_account_type VARCHAR(50) NOT NULL,
	ach_account_number VARCHAR(25),
	original_balance NUMERIC(19, 2) NOT NULL ,
	current_balance NUMERIC(19, 2) NOT NULL ,
	available_credit NUMERIC(19, 2) ,
	open_date DATE NULL,
	maturity_date DATE NULL ,
	interest_due NUMERIC(19, 8) ,
	branch VARCHAR(10) ,
	core_account_status VARCHAR(50) NULL,
	term_length VARCHAR(25) NULL ,
	term_type VARCHAR(25) NULL,
	interest_rate NUMERIC(19, 8) NULL ,
	core_product_code VARCHAR(50) NOT NULL ,
	interest_year_to_date NUMERIC(19, 8) NULL,
	business_personal VARCHAR(25) ,
	date_last_payment DATE NULL ,
	date_next_payment DATE NULL,
	escrow_amount NUMERIC(19, 2) NULL ,
	origination_fee NUMERIC(19, 2) NULL,
	file_creation_date_time TIMESTAMP NOT NULL ,
	accounting_group VARCHAR(25) NULL,
	rolled_from_date DATE 
	,PRIMARY KEY (account_kasasakey, core_processing_date)
  )ENGINE=InnoDB DEFAULT CHARSET=utf8
  ;


