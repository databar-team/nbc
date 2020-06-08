-- One of the prospects needs a different PKK
UPDATE acxiom_sourced_prospects
SET
    `prospect_kasasa_key` = CONCAT(`prospect_kasasa_key`, '_a'),
    `kasasa_master_person_id` = CONCAT(`kasasa_master_person_id`, '_a'),
    `data_load_date` = NOW()
WHERE `prospect_kasasa_key` LIKE '%dummy_prospect_kasasa_key%'
;