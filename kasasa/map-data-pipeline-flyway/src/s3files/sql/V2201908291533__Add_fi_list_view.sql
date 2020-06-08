CREATE VIEW map_config.onboard_fi_ids AS
SELECT DISTINCT financial_institution_id
	FROM map_config.feature_signup
	WHERE feature_name IN ('prospecting', 'lifecycle')
		AND active_end_date > UTC_TIMESTAMP();