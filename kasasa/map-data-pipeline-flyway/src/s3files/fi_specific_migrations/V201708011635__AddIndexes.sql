ALTER TABLE `customer`
ADD INDEX `kasasa_master_person_id` (`kasasa_master_person_id` ASC);

ALTER TABLE `customer`
ADD INDEX `fico_individual_id` (`fico_individual_id` ASC);

ALTER TABLE `customer_address`
ADD INDEX `customer_kasasa_key` (`customer_kasasa_key` ASC);

ALTER TABLE `customer_email`
ADD INDEX `customer_kasasa_key` (`customer_kasasa_key` ASC);

ALTER TABLE `customer_phone`
ADD INDEX `customer_kasasa_key` (`customer_kasasa_key` ASC);

ALTER TABLE `accounts`
ADD INDEX `customer_kasasa_key` (`customer_kasasa_key` ASC);

ALTER TABLE `fico_sourced_customers`
ADD INDEX `customer_kasasa_key` (`customer_kasasa_key` ASC);

ALTER TABLE `fico_sourced_customers`
ADD INDEX `fico_individual_id` (`fico_individual_id` ASC);

ALTER TABLE `fico_sourced_prospects`
ADD INDEX `fico_individual_id` (`fico_individual_id` ASC);

ALTER TABLE `fico_sourced_prospects`
ADD INDEX `kasasa_master_person_id` (`kasasa_master_person_id` ASC);

ALTER TABLE `branch`
ADD INDEX `financial_institution_id` (`financiaL_institution_id` ASC);

ALTER TABLE `branch_address`
ADD INDEX `branch_id` (`branch_id` ASC);
