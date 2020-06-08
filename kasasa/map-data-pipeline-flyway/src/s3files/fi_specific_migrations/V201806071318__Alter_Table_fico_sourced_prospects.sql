ALTER TABLE fico_sourced_prospects
add COLUMN `email_append_flag` char(1) DEFAULT NULL AFTER email,
add COLUMN `score` char(1) DEFAULT NULL AFTER distance_to_branch,
add COLUMN `phone_number` varchar(10) DEFAULT NULL AFTER decile
;