ALTER TABLE account_events DROP PRIMARY KEY;

ALTER TABLE account_events ADD PRIMARY KEY (account_kasasakey, event_type, event_effective_date, core_processing_date);
