-- Data already exists in this table.  Add a column with not null is going fail.  So Truncate the table first and then do the alter.  Truncate is ok, because the data is Transient.
TRUNCATE TABLE addresses;

ALTER TABLE addresses
ADD COLUMN key_type varchar(25) NOT NULL FIRST,
ADD COLUMN kasasakey varchar(100) NOT NULL AFTER key_type,
DROP COLUMN customer_kasasa_key,
DROP COLUMN delivery_point_bar_code,
DROP COLUMN carrier_route_code,
DROP COLUMN line_of_travel,
DROP COLUMN national_change_of_address_move_flag,
DROP COLUMN national_change_of_address_move_date,
DROP COLUMN national_change_of_address_drop_flag,
DROP COLUMN advantage_target_narrow_band_income,
DROP COLUMN advantage_target_income_indicator,
DROP COLUMN house_hold_type_code,
DROP COLUMN geo_code_census_tract_block_number_area,
DROP COLUMN geo_code_block_group,
DROP COLUMN geo_code_census_state_code,
DROP COLUMN geo_code_census_county_code,
DROP COLUMN geo_code_neilsen_county_size_code,
DROP COLUMN geo_code_dma_code,
DROP COLUMN advantage_dwelling_type,
DROP COLUMN advantage_dwelling_type_indicator,
DROP COLUMN individual_age_ccyymm,
DROP COLUMN distance_to_branch,
DROP COLUMN time_zone,
DROP COLUMN wireless_flag,
DROP COLUMN start_date
;
ALTER TABLE addresses ADD PRIMARY KEY (kasasakey, key_type);