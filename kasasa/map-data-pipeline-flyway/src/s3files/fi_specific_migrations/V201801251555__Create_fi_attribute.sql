-- This table is currently being used in Adoption campaign.  Intent is to calculate fi level attributes.
-- For now it is transient.  Could not find a reason why it need to move to map_config schema.

DROP TABLE IF EXISTS fi_attribute;
CREATE TABLE fi_attribute (
	financial_institution_id 	integer		NOT NULL,
	cycle_id_config				bigint 		NOT NULL,
	product_id_config			varchar(50)	NOT NULL,
	qual_percentage				TINYINT 	NOT NULL,
	ind_qualify 				TINYINT 	DEFAULT 0,
	PRIMARY KEY (financial_institution_id, cycle_id_config, product_id_config)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;
