CREATE TABLE `crm_product_master` (
    product_record_id VARCHAR(144) NOT NULL,
    fi_crm_record_id VARCHAR(144) NOT NULL,
    product_class VARCHAR(144) NOT NULL,
    product_name VARCHAR(200),
    krp_base_product_id INT(11)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
