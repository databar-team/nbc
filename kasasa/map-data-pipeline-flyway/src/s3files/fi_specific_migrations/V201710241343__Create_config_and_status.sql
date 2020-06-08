-- A table of key value pairs that store FI level configuration and status.
CREATE TABLE `config_and_status` (
    attribute_name VARCHAR(144) NOT NULL,
    attribute_value VARCHAR(144) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
