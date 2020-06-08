DROP TABLE IF EXISTS product_details;
CREATE TABLE product_details (
   product_kasasa_key varchar(100) NOT  NULL,
   vendor_item_id int(11) NOT NULL,
   financial_institution_id int(11) DEFAULT NULL,
   product_name varchar(50) NOT NULL,
   product_class varchar(50) NOT NULL,
   product_status varchar(50) NOT NULL,
   order_priority smallint(6) DEFAULT NULL,
  marketability_of_product char(1) DEFAULT NULL,
  PRIMARY KEY (product_kasasa_key, product_class, vendor_item_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
