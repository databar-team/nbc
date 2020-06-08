INSERT INTO `data_quality`.`sources` (`source_id`, `source`) VALUES ('9', 'dq_rule_runner');
INSERT INTO `data_quality`.`file_types` (`file_type_id`, `file_type`) VALUES ('20', 'dq_rule_runner');
INSERT INTO `data_quality`.`source_file_types` (`source_file_type_id`, `source_id`, `file_type_id`, `is_active`) VALUES ('41', '9', '20', 1);
