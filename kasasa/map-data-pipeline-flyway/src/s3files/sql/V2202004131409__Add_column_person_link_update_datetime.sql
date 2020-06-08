ALTER TABLE `map_global_data`.`surrogate_person_link_mappings`
    ADD COLUMN `person_link_update_datetime` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
;