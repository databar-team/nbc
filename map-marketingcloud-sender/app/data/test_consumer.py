import os
import pytest
import data.consumer
from tests import teardown_db_migrations, run_db_migrations, get_db_connection


# DB setup and teardown with migrations as well as creating the connection
@pytest.fixture(scope="function")
def db_connection():
    run_db_migrations()

    db_connection = get_db_connection()
    yield db_connection
    db_connection.close()

    teardown_db_migrations()

def test_get_valid_fi_ids(db_connection):
    valid_ids = data.consumer.get_valid_fi_ids(db_connection)

    assert 2211 in valid_ids

def test_get_recently_changed_customers_generator(db_connection):
    customers_gen = data.consumer.get_recently_changed_customers_generator(db_connection)

    count = 0
    for batch in customers_gen:
        for customer in batch:
            assert customer["city"] is not None
            assert customer["state"] is not None
            assert customer["address_1"] is not None
            assert customer["email_address"] is not None
            assert customer["address_2"] is None

            count += 1

    assert 3 == count

def test_get_new_fico_prospects_generator(db_connection):
    prospects_gen = data.consumer.get_new_fico_prospects_generator(db_connection)

    count = 0
    for batch in prospects_gen:
        for prospect in batch:
            assert None != prospect["full_name"]
            assert None != prospect["email_address"]

            count += 1

    assert 1 == count

def test_get_new_acxiom_prospects_generator(db_connection):
    prospects_gen = data.consumer.get_new_acxiom_prospects_generator(db_connection)

    count = 0
    for batch in prospects_gen:
        for prospect in batch:
            assert None != prospect["full_name"]
            assert None != prospect["email_address"]

            count += 1

    assert 2 == count