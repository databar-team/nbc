import os
import pytest
import random
import string
from worker.data.fi_mc import FiMarketingCloud
from tests.worker.data import run_db_migrations, get_db_connection, teardown_db_migrations


@pytest.fixture(scope="function")
def db_connection():
    run_db_migrations()

    db = get_db_connection()
    yield db
    try:
        db.close()
    except Exception as e:
        pass

    teardown_db_migrations()


@pytest.fixture(scope='function')
def mc_values():
    return {
        'fi_id' : 'test_db', # Using the unique db in test env as FI_ID
        'product_data': [
            {
                "AcctProdIDFull__c": f"{sub_number + 1}_{_random_value(10)}",
                "AcctProductExternalID__c": _random_value(40),
                "Name": "RxSaver",
                "Product Class": _random_value(50),
                "Include for Cross Sell": "No",
                "AccountNumber": "test_db",
                "Product__c": _random_value(18),
                "BillingKrpPid__c": random.randint(200, 299),
                "Market_This_Product": _random_value(255),
                "Product_Priority": _random_value(255),
                "Opt-In_Status": _random_value(255)
            } for sub_number in range(3)
        ]
    }
    

@pytest.fixture(scope='function')
def mc_mapping():
    return {
           "salesforce_product_id": "AcctProdIDFull__c",
           "fi_crm_record_id": "AcctProductExternalID__c",
           "product_type": "Product Class",
           "product_name": "Product__c",
           "krp_base_product_id": "BillingKrpPid__c",
           "market_this_product": "Market_This_Product",
           "product_priority": "Product_Priority",
           "opt_in_status": "Opt-In_Status"
    }


def test_fimc_mapping_assignation(mc_mapping):
    # Given
    # When
    fi_mc_mapping = FiMarketingCloud()._table_fields_map
    # Then
    assert fi_mc_mapping == mc_mapping
    

def test_mc_db_get_mask_values(mc_values):
    # Given
    mc_db = FiMarketingCloud()
    expected_values = _get_values(mc_values['product_data'], mc_db._table_fields_map)
    expected_mask = _get_mask(mc_values['product_data'], mc_db._table_fields_map)
    # When
    mask, values = mc_db._get_mask_values(mc_values['product_data'])
    # Then
    assert expected_values == values
    assert expected_mask == mask


def test_mc_db_build_sql(mc_values):
    # Given
    mc_db = FiMarketingCloud()
    expected_sql = "INSERT INTO `test_db`.`sfmc_product_master` (`salesforce_product_id`,`fi_crm_record_id`,`product_type`,`product_name`,`krp_base_product_id`,`market_this_product`,`product_priority`,`opt_in_status`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s),(%s,%s,%s,%s,%s,%s,%s,%s),(%s,%s,%s,%s,%s,%s,%s,%s)"
    expected_values = _get_values(mc_values['product_data'], mc_db._table_fields_map)
    # When
    sql, values = mc_db._build_sql(mc_values['product_data'], mc_values['fi_id'])
    # Then
    assert expected_sql == sql
    assert expected_values == values


@pytest.mark.skipif(os.getenv('SKIP_INTEGRATION', False), reason="No database spun up")
def test_insert_many(db_connection, mc_values):
    # Given
    # When
    fi_mc_mapping = FiMarketingCloud(db_connection)
    inserted = fi_mc_mapping.insert_many(values=mc_values['product_data'], fi_id=f"{mc_values['fi_id']}", on_duplicate_key_update=True)
    # Then
    assert inserted == len(mc_values['product_data'])


def _random_value(k=30):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=k))


def _get_mask(values, mapping_values):
    mask = []
    mask_row = f"({','.join(['%s' for val in mapping_values])})"
    for set_values in values:
        mask.append(mask_row)
    return ','.join(mask)


def _get_values(values, field_map):
    flattened_values = []
    for set_values in values:
        flattened_values += [set_values.get(field, 'NULL') for field in field_map.values()]
    return flattened_values