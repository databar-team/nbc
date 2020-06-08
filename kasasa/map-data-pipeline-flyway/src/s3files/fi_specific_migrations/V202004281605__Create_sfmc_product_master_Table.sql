
CREATE TABLE sfmc_product_master (

    salesforce_product_id       varchar (50),
    fi_crm_record_id            varchar (40),
    product_name                varchar (18),
    krp_base_product_id         int (11),
    market_this_product         varchar (255),
    product_priority            varchar (255),
    opt_in_status               varchar (255),
    product_type                varchar (50),
    PRIMARY KEY (salesforce_product_id)
        
) ENGINE=InnoDB DEFAULT CHARSET=utf8;   


