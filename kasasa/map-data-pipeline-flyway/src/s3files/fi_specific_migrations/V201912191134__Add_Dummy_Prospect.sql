-- Dummy record so that if an FI's entire prospect set is expired, we can send
-- back those changes as we'll still have a 'valid' prospect in their data
INSERT INTO fico_sourced_prospects (
    prospect_kasasa_key,
    financial_institution_id,
    branch_id,
    fico_individual_id,
    kasasa_master_person_id,
    email,
    full_name,
    fico_file_name,
    expiration_date
)
VALUES (
      CONCAT(REPLACE((SELECT DATABASE()), 'fi_', ''), '-', 'dummy_prospect_kasasa_key')
    , REPLACE((SELECT DATABASE()), 'fi_', '')
    , 'dummy_branch_id'
    , CONCAT(REPLACE((SELECT DATABASE()), 'fi_', ''), '-', 'id')
    , CONCAT(REPLACE((SELECT DATABASE()), 'fi_', ''), '-', 'dummy_kasasa_master_person_id')
    , 'noreply@kasasa.com'
    , 'DUMMY RECORD'
    , 'flyway_dummy_record'
    , '9999-12-31'
);

INSERT INTO acxiom_sourced_prospects (
    prospect_kasasa_key,
    financial_institution_id,
    branch_id,
    lac_consumer_link,
    lac_address_link,
    lac_household_link,
    kasasa_master_person_id,
    email,
    full_name,
    acxiom_file_name,
    expiration_date
)
VALUES (
      CONCAT(REPLACE((SELECT DATABASE()), 'fi_', ''), '-', 'dummy_prospect_kasasa_key')
    , REPLACE((SELECT DATABASE()), 'fi_', '')
    , 'dummy_branch_id'
    , CONCAT(REPLACE((SELECT DATABASE()), 'fi_', ''), '-', 'id')
    , 'dummy-id'
    , 'dummy-id'
    , CONCAT(REPLACE((SELECT DATABASE()), 'fi_', ''), '-', 'dummy_kasasa_master_person_id')
    , 'noreply@kasasa.com'
    , 'DUMMY RECORD'
    , 'flyway_dummy_record'
    , '9999-12-31'
);
