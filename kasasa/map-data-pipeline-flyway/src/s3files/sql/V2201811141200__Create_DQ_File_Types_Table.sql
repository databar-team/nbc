-- Create table for listing valid file types to be used in tandem with sources and stats tables
CREATE TABLE IF NOT EXISTS `data_quality`.`file_types`
(
    file_type_id INT NOT NULL AUTO_INCREMENT,
    file_type VARCHAR(100) NOT NULL,
    PRIMARY KEY (file_type_id),
    UNIQUE uk_file_type(file_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

-- Populate new file_types table with first run of known file types
INSERT INTO `data_quality`.`file_types` (file_type)
VALUES ('account_events'),
    ('addresses'),
    ('calculate_attribute_postprocess'),
    ('calculate_attribute_preprocess'),
    ('config_cycles'),
    ('config_product_mappings'),
    ('crm_product_master'),
    ('customer'),
    ('deposits'),
    ('direct_marketing'),
    ('emails'),
    ('email_permanent_suppression'),
    ('fico_sourced_customers'),
    ('fico_sourced_prospects'),
    ('fidil_relationships'),
    ('krp_overall_qualifications'),
    ('krp_qualifications_details'),
    ('loans'),
    ('phones')
;

-- Create mapping table between sources and their file_types
CREATE TABLE IF NOT EXISTS `data_quality`.`source_file_types`
(
    source_file_type_id INT NOT NULL AUTO_INCREMENT,
    source_id INT NOT NULL,
    file_type_id INT NOT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 0,
    PRIMARY KEY (source_file_type_id),
    UNIQUE uk_source_id_file_type_id(source_id, file_type_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

-- Populate mapping table with sources and their file_types
INSERT INTO `data_quality`.`source_file_types` (source_id, file_type_id, is_active)
SELECT s.source_id, ft.file_type_id, 1
FROM `data_quality`.`sources` s
    INNER JOIN `data_quality`.`file_types` ft
        ON ft.file_type IN ('account_events', 'addresses', 'config_cycles', 'config_product_mappings',
        'crm_product_master', 'customer', 'deposits', 'emails', 'fidil_relationships',
        'krp_overall_qualifications', 'krp_qualifications_details', 'loans', 'phones')
WHERE s.source IN ('extract', 'transform', 'load')

UNION

SELECT s.source_id, ft.file_type_id, 1
FROM `data_quality`.`sources` s
    INNER JOIN `data_quality`.`file_types` ft
        ON ft.file_type IN ('email_permanent_suppression')
WHERE s.source IN ('vendor_in')

UNION

SELECT s.source_id, ft.file_type_id, 1
FROM `data_quality`.`sources` s
    INNER JOIN `data_quality`.`file_types` ft
        ON ft.file_type IN ('calculate_attribute_preprocess')
WHERE s.source IN ('calculate_attribute_preprocess')

UNION

SELECT s.source_id, ft.file_type_id, 1
FROM `data_quality`.`sources` s
    INNER JOIN `data_quality`.`file_types` ft
        ON ft.file_type IN ('calculate_attribute_postprocess')
WHERE s.source IN ('calculate_attribute_postprocess')

UNION

SELECT s.source_id, ft.file_type_id, 1
FROM `data_quality`.`sources` s
    INNER JOIN `data_quality`.`file_types` ft
        ON ft.file_type IN ('calculate_attribute')
WHERE s.source IN ('calculate_attribute')

ORDER BY 1, 2
;