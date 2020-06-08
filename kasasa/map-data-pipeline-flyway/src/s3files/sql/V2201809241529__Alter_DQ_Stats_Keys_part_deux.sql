-- Sequence number is going to be turned into a batch number by fi_id by date_loaded by file_type by source_id
-- First instance of file type will be 1, second of the same file type on the same day for the same fi woud be 2 and so on for each stat loaded

-- truncate the table, we're not going to worry about historical items
TRUNCATE TABLE `data_quality`.`stats`;

-- alter sequence id column (no longer auto inc) and drop keys, then reset keys
ALTER TABLE `data_quality`.`stats` MODIFY COLUMN sequence_id INT AFTER file_type,
DROP PRIMARY KEY,
ADD PRIMARY KEY (fi_id, source_id, date_loaded, file_type, sequence_id);