CREATE TABLE fidil_relationships (
  account_kasasakey VARCHAR(100),
  customer_kasasakey VARCHAR(100),
  kasasa_relationship_code VARCHAR(25),
  financial_institution_id int(11),
  core_processing_date date,
  PRIMARY KEY (account_kasasakey));

CREATE TABLE account_events (
  account_kasasakey VARCHAR(100),
  core_processing_date date,
  event_type VARCHAR(100),
  core_product_code VARCHAR(50),
  core_account_type VARCHAR(50),
  kasasa_product_type VARCHAR(50),
  kasasa_account_type VARCHAR(75),
  kasasa_product_id int(11),
  event_effective_date date,
  is_kasasa_powered bool,
  current_account_status VARCHAR(50),
  financial_institution_id int(11),
  PRIMARY KEY (account_kasasakey));

CREATE TABLE deposits (
  account_kasasakey VARCHAR(100),
  financial_institution_id int(11),
  core_processing_date date,
  core_account_type VARCHAR(50),
  open_date date,
  close_date date,
  branch VARCHAR(10),
  PRIMARY KEY (account_kasasakey));
