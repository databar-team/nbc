CREATE TABLE `last_successful_lt_pipeline_run` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `last_run` timestamp,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
