import pymysql

BATCH_SIZE = 1000


def get_valid_fi_ids(connection):
    sql = """SELECT DISTINCT financial_institution_id AS fi_id
    FROM feature_signup
    WHERE CURDATE() BETWEEN `active_start_date` AND `active_end_date`
        AND `marketing_cloud` = 1;"""

    with connection.cursor(pymysql.cursors.Cursor) as cursor:
        cursor.execute(sql)
        return [x[0] for x in cursor.fetchall()]


def get_recently_changed_customers_generator(connection):
    sql = """
SELECT
    S.`surrogate_id`,
    SPLM.`person_link_id`,
    "Customer" AS "contact_status",
    C.`full_name`,
    C.`first_name`,
    C.`last_name`,
    C.`middle_name`,
    C.`suffix`,
    NULLIF(CA.`attribute_object`->>"$.cse_kasasa_personal_loans", 'null') AS "kasasa_personal_loans",
    NULLIF(CA.`attribute_object`->>"$.city", 'null') AS "city",
    NULLIF(CA.`attribute_object`->>"$.state", 'null') AS "state",
    NULLIF(CA.`attribute_object`->>"$.zipcode", 'null') AS "zipcode",
    NULLIF(CA.`attribute_object`->>"$.address_1", 'null') AS "address_1",
    NULLIF(CA.`attribute_object`->>"$.address_2", 'null') AS "address_2",
    NULLIF(CA.`attribute_object`->>"$.zipcode_extended", 'null') AS "zipcode_extended",
    NULLIF(CA.`attribute_object`->>"$.customer_email_address", 'null') AS "email_address",
    NULLIF(CA.`attribute_object`->>"$.phone_number", 'null') AS "phone_number",
    NULLIF(CA.`attribute_object`->>"$.customer_anniversary", 'null') AS "enter_anniversary",
    NULLIF(CA.`attribute_object`->>"$.customer_birthday", 'null') AS "enter_birthday",
    NULLIF(CA.`attribute_object`->>"$.identity_protection_product_id", 'null') AS "identity_protection",
    NULLIF(CA.`attribute_object`->>"$.prescription_savings_product_id", 'null') AS "prescription_savings",
    NULLIF(CA.`attribute_object`->>"$.vision_insurance_product_id", 'null') AS "vision_insurance",
    NULLIF(CA.`attribute_object`->>"$.dental_insurance_product_id", 'null') AS "dental_insurance",
    NULLIF(CA.`attribute_object`->>"$.asset_protection_product_id", 'null') AS "asset_protection",
    NULLIF(CA.`attribute_object`->>"$.marketplace_product_id", 'null') AS "marketplace"
FROM `customer_attribute` CA
  INNER JOIN `customer_attribute_hashes` CAH
      ON (CAH.`customer_kasasa_key` = CA.`customer_kasasa_key`)
  INNER JOIN `customer` C
      ON (CAH.`customer_kasasa_key` = C.`customer_kasasa_key`)
  INNER JOIN `surrogates` S
      ON (CAH.`customer_kasasa_key` = S.`record_key`)
  LEFT JOIN `map_global_data`.`surrogate_person_link_mappings` SPLM
      ON (S.`surrogate_id` = SPLM.`surrogate_id`)
  INNER JOIN (SELECT COALESCE(MAX(`last_run_date_time`), "1900-01-01") as "last_run_date_time"
              FROM `task_last_run` WHERE `task_id` = 1) TLR
      ON TLR.`last_run_date_time` < GREATEST(COALESCE(CAH.`date_last_updated`, '2000-01-01'),
                                             COALESCE(SPLM.`person_link_update_datetime`, '2000-01-01'))
;"""

    with connection.cursor(pymysql.cursors.SSDictCursor) as cursor:
        cursor.execute(sql)
        while True:
            batch = cursor.fetchmany(size=BATCH_SIZE)
            if not batch:
                break
            yield batch


def get_new_acxiom_prospects_generator(connection):
    """
    The first SELECT looks for new prospects, converted, and expired based on the data load date of the prospect
    The second query looks for any newly converted prospects based on the date load of the PCM table
    The last query looks for any expired prospects that have already been loaded, but only looking back a week
    """

    sql = """
SELECT
  S.`surrogate_id`,
  SPLM.`person_link_id`,
  CASE WHEN PCM.`customer_kasasa_key` IS NOT NULL THEN "Converted" WHEN CURDATE() >= ASP.`expiration_date` THEN "Expired" ELSE "Prospect" END AS "contact_status",
  ASP.`full_name`,
  ASP.`first_name`,
  ASP.`last_name`,
  ASP.`middle_name`,
  NULL AS "suffix",
  ASP.`city`,
  ASP.`state`,
  ASP.`zipcode`,
  ASP.`address_1`,
  ASP.`address_2`,
  ASP.`zipcode_extended`,
  COALESCE(ASP.`email`, ASP.`email_2`) AS "email_address",
  NULL AS "phone_number"
FROM
  acxiom_sourced_prospects ASP
  INNER JOIN `surrogates` S ON (
    ASP.`prospect_kasasa_key` = S.`record_key`
  )
  LEFT JOIN `map_global_data`.`surrogate_person_link_mappings` SPLM ON (
    S.`surrogate_id` = SPLM.`surrogate_id`
  )
  LEFT JOIN `prospect_customer_mapping` PCM ON (
    ASP.`prospect_kasasa_key` = PCM.`prospect_kasasa_key`
  )
  INNER JOIN (SELECT COALESCE(MAX(`last_run_date_time`), "1900-01-01") as "last_run_date_time" FROM `task_last_run` WHERE `task_id` = 1) TLR ON (
    TLR.`last_run_date_time` < GREATEST(COALESCE(ASP.`data_load_date`, '2000-01-01'),
                                        COALESCE(SPLM.`person_link_update_datetime`, '2000-01-01'))
  )
UNION
SELECT
  S.`surrogate_id`,
  SPLM.`person_link_id`,
  "Converted" AS "contact_status",
  ASP.`full_name`,
  ASP.`first_name`,
  ASP.`last_name`,
  ASP.`middle_name`,
  NULL AS "suffix",
  ASP.`city`,
  ASP.`state`,
  ASP.`zipcode`,
  ASP.`address_1`,
  ASP.`address_2`,
  ASP.`zipcode_extended`,
  COALESCE(ASP.`email`, ASP.`email_2`) AS "email_address",
  NULL AS "phone_number"
FROM
  acxiom_sourced_prospects ASP
  INNER JOIN `surrogates` S ON (
    ASP.`prospect_kasasa_key` = S.`record_key`
  )
  LEFT JOIN `map_global_data`.`surrogate_person_link_mappings` SPLM ON (
    S.`surrogate_id` = SPLM.`surrogate_id`
  )
  INNER JOIN `prospect_customer_mapping` PCM ON (
    PCM.`prospect_kasasa_key` = ASP.`prospect_kasasa_key`
  )
  INNER JOIN (SELECT COALESCE(MAX(`last_run_date_time`), "1900-01-01") as "last_run_date_time" FROM `task_last_run` WHERE `task_id` = 1) TLR ON (
    TLR.`last_run_date_time` < GREATEST(COALESCE(PCM.`data_load_date`, '2000-01-01'),
                                        COALESCE(SPLM.`person_link_update_datetime`, '2000-01-01'))
  )
UNION
SELECT
  S.`surrogate_id`,
  SPLM.`person_link_id`,
  "Expired" AS "contact_status",
  ASP.`full_name`,
  ASP.`first_name`,
  ASP.`last_name`,
  ASP.`middle_name`,
  NULL AS "suffix",
  ASP.`city`,
  ASP.`state`,
  ASP.`zipcode`,
  ASP.`address_1`,
  ASP.`address_2`,
  ASP.`zipcode_extended`,
  COALESCE(ASP.`email`, ASP.`email_2`) AS "email_address",
  NULL AS "phone_number"
FROM
  acxiom_sourced_prospects ASP
  INNER JOIN `surrogates` S ON (
    ASP.`prospect_kasasa_key` = S.`record_key`
  )
  LEFT JOIN `map_global_data`.`surrogate_person_link_mappings` SPLM ON (
    S.`surrogate_id` = SPLM.`surrogate_id`
  )
  LEFT JOIN `prospect_customer_mapping` PCM ON (
    ASP.`prospect_kasasa_key` = PCM.`prospect_kasasa_key`
  )
  INNER JOIN (SELECT COALESCE(MAX(`last_run_date_time`), "1900-01-01") as "last_run_date_time" FROM `task_last_run` WHERE `task_id` = 1) TLR
    ON (
      ASP.`expiration_date` BETWEEN TLR.`last_run_date_time` AND CURDATE()
    )
WHERE PCM.`customer_kasasa_key` IS NULL;
"""

    with connection.cursor(pymysql.cursors.SSDictCursor) as cursor:
        cursor.execute(sql)
        while True:
            batch = cursor.fetchmany(size=BATCH_SIZE)
            if not batch:
                break
            yield batch


def get_new_fico_prospects_generator(connection):
    """
    The first SELECT looks for new prospects, converted, and expired based on the data load date of the prospect
    The second query looks for any newly converted prospects based on the date load of the PCM table
    The last query looks for any expired prospects that have already been loaded, but only looking back a week
    """

    sql = """
SELECT
  S.`surrogate_id`,
  SPLM.`person_link_id`,
  CASE WHEN PCM.`customer_kasasa_key` IS NOT NULL THEN "Converted" WHEN CURDATE() >= FSP.`expiration_date` THEN "Expired" ELSE "Prospect" end AS "contact_status",
  FSP.`full_name`,
  FSP.`first_name`,
  FSP.`last_name`,
  FSP.`middle_name`,
  FSP.`suffix`,
  FSP.`city`,
  FSP.`state`,
  FSP.`zipcode`,
  FSP.`address_1`,
  FSP.`address_2`,
  FSP.`zipcode_extended`,
  FSP.`email` AS "email_address",
  FSP.`phone_number`
FROM
  fico_sourced_prospects FSP
  INNER JOIN `surrogates` S ON (
    FSP.`prospect_kasasa_key` = S.`record_key`
  )
  LEFT JOIN `map_global_data`.`surrogate_person_link_mappings` SPLM ON (
    S.`surrogate_id` = SPLM.`surrogate_id`
  )
  LEFT JOIN `prospect_customer_mapping` PCM ON (
    FSP.`prospect_kasasa_key` = PCM.`prospect_kasasa_key`
  )
  INNER JOIN (SELECT COALESCE(MAX(`last_run_date_time`), "1900-01-01") as "last_run_date_time" FROM `task_last_run` WHERE `task_id` = 1) TLR ON (
    TLR.`last_run_date_time` < GREATEST(COALESCE(FSP.`data_load_date`, '2000-01-01'),
                                        COALESCE(SPLM.`person_link_update_datetime`, '2000-01-01'))
  )
UNION
SELECT
  S.`surrogate_id`,
  SPLM.`person_link_id`,
  "Converted" AS "contact_status",
  FSP.`full_name`,
  FSP.`first_name`,
  FSP.`last_name`,
  FSP.`middle_name`,
  FSP.`suffix`,
  FSP.`city`,
  FSP.`state`,
  FSP.`zipcode`,
  FSP.`address_1`,
  FSP.`address_2`,
  FSP.`zipcode_extended`,
  FSP.`email` AS "email_address",
  FSP.`phone_number`
FROM
  fico_sourced_prospects FSP
  INNER JOIN `surrogates` S ON (
    FSP.`prospect_kasasa_key` = S.`record_key`
  )
  LEFT JOIN `map_global_data`.`surrogate_person_link_mappings` SPLM ON (
    S.`surrogate_id` = SPLM.`surrogate_id`
  )
  INNER JOIN `prospect_customer_mapping` PCM ON (
    PCM.`prospect_kasasa_key` = FSP.`prospect_kasasa_key`
  )
  INNER JOIN (SELECT COALESCE(MAX(`last_run_date_time`), "1900-01-01") as "last_run_date_time" FROM `task_last_run` WHERE `task_id` = 1) TLR ON (
    TLR.`last_run_date_time` < GREATEST(COALESCE(PCM.`data_load_date`, '2000-01-01'),
                                        COALESCE(SPLM.`person_link_update_datetime`, '2000-01-01'))
  )
UNION
SELECT
  S.`surrogate_id`,
  SPLM.`person_link_id`,
  "Expired" AS "contact_status",
  FSP.`full_name`,
  FSP.`first_name`,
  FSP.`last_name`,
  FSP.`middle_name`,
  FSP.`suffix`,
  FSP.`city`,
  FSP.`state`,
  FSP.`zipcode`,
  FSP.`address_1`,
  FSP.`address_2`,
  FSP.`zipcode_extended`,
  FSP.`email` AS "email_address",
  FSP.`phone_number`
FROM
  fico_sourced_prospects FSP
  INNER JOIN `surrogates` S ON (
    FSP.`prospect_kasasa_key` = S.`record_key`
  )
  LEFT JOIN `map_global_data`.`surrogate_person_link_mappings` SPLM ON (
    S.`surrogate_id` = SPLM.`surrogate_id`
  )
  LEFT JOIN `prospect_customer_mapping` PCM ON (
    FSP.`prospect_kasasa_key` = PCM.`prospect_kasasa_key`
  )
  INNER JOIN (SELECT COALESCE(MAX(`last_run_date_time`), "1900-01-01") as "last_run_date_time" FROM `task_last_run` WHERE `task_id` = 1) TLR ON (
    FSP.`expiration_date` BETWEEN TLR.`last_run_date_time` AND CURDATE()
  )
WHERE PCM.`customer_kasasa_key` IS NULL;"""

    with connection.cursor(pymysql.cursors.SSDictCursor) as cursor:
        cursor.execute(sql)
        while True:
            batch = cursor.fetchmany(size=BATCH_SIZE)
            if not batch:
                break
            yield batch


def mark_run_as_successful(connection):
    sql = """INSERT INTO `task_last_run` (`task_id`) VALUES (1);"""

    with connection.cursor() as cursor:
        cursor.execute(sql)
        cursor.close()
    connection.commit()
