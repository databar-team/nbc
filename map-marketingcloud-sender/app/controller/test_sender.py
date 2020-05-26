import pytest
import queue

from controller.sender import batch_consumers, map_row_to_marketingcloud_api
from data.consumer import BATCH_SIZE


@pytest.fixture(scope="function")
def consumer_row():
    return [{
        "surrogate_id": 12345,
        "person_link_id": "random_id",
        "contact_status": "Thing",
        "full_name": "Joe Smoe",
        "first_name": "Joe",
        "last_name": "Smoe",
        "middle_name": "",
        "suffix": "Sr.",
        "city": "Austin",
        "state": "TX",
        "zipcode": "78727",
        "address_1": "1234 Made Up Road",
        "address_2": "",
        "zipcode_extended": "1234",
        "email_address": "test@example.com",
        "phone_number": "555-555-5555",
        "identity_protection": "1",
        "prescription_savings": "1",
        "vision_insurance": "1",
        "dental_insurance": "1",
        "asset_protection": "1",
        "marketplace_product_id": "1",
        "kasasa_personal_loans":""
    }]


@pytest.fixture(scope="function")
def valid_fi_ids():
    return [2211]


def test_batch_consumers(consumer_row, valid_fi_ids):
    # given
    num_consumers = BATCH_SIZE

    q = queue.Queue()

    consumers = consumer_row * num_consumers

    def test_gen():
        for i in range(0, len(consumers), 10):
            yield consumers[i: i+10]

    # when
    batch_consumers(valid_fi_ids[0], test_gen(), q, batch_limit=num_consumers / 20)

    # then
    msg = q.get()

    assert msg["batch_num"] == 1
    assert msg["fi_id"] == 2211
    assert len(msg["data"]) == 10


def test_batch_consumers_many(consumer_row, valid_fi_ids):
    # given
    num_consumers = BATCH_SIZE * 100

    q = queue.Queue()

    consumers = consumer_row * num_consumers

    def test_gen():
        for i in range(0, len(consumers), 1000):
            yield consumers[i: i+1000]

    # when
    batch_consumers(valid_fi_ids[0], test_gen(), q, batch_limit=num_consumers / 500)

    # then
    assert 100 == q.qsize()

    batch_num = 1
    while not q.empty():
        msg = q.get()

        assert batch_num == msg["batch_num"]
        assert 2211 == msg["fi_id"]
        assert BATCH_SIZE == len(msg["data"])

        batch_num += 1


def test_batch_consumers_many_with_leftover(consumer_row, valid_fi_ids):
    # given
    leftover = 50
    num_consumers = (BATCH_SIZE * 100) + leftover

    q = queue.Queue()

    consumers = consumer_row * num_consumers

    def test_gen():
        for i in range(0, len(consumers), 1000):
            yield consumers[i: i+1000]
    # when
    batch_consumers(valid_fi_ids[0], test_gen(), q, batch_limit=num_consumers / 500)

    # then
    assert 101 == q.qsize()

    batch_num = 1
    while not q.empty():
        msg = q.get()

        assert batch_num == msg["batch_num"]
        assert 2211 == msg["fi_id"]

        if q.empty():
            assert leftover == len(msg["data"])
        else:
            assert BATCH_SIZE == len(msg["data"])

        batch_num += 1


def test_map_row_to_marketingcloud_api(consumer_row, valid_fi_ids):
    # given
    expected = {
        "keys": {
            "Subscriber_Key": consumer_row[0]["surrogate_id"]
        },
        "values": {
            "Person_ID": consumer_row[0]["person_link_id"],
            "FI_ID_Number": valid_fi_ids[0],
            "Contact_Status": consumer_row[0]["contact_status"],
            "Full_Name": consumer_row[0]["full_name"],
            "First_Name": consumer_row[0]["first_name"],
            "Middle_Name": consumer_row[0]["middle_name"],
            "Last_Name": consumer_row[0]["last_name"],
            "Suffix": consumer_row[0]["suffix"],
            "Primary_Address": consumer_row[0]["address_1"],
            "Secondary_Address": consumer_row[0]["address_2"],
            "City": consumer_row[0]["city"],
            "State": consumer_row[0]["state"],
            "Zip_Code": consumer_row[0]["zipcode"],
            "Zip_4": consumer_row[0]["zipcode_extended"],
            "Email_Address": consumer_row[0]["email_address"],
            "Phone": consumer_row[0]["phone_number"],
            "Urbanicity": "",
            "Audience": "All",
            "Prospect_Product_ID": "Null",
            "Welcome_Product_ID": "",
            "Enter_Birthday": "",
            "Enter_Anniversary": "",
            "Adoption_Type": "",
            "Adoption_Product_ID": "",
            "KCS_Cross_Sell_Product_ID": "",
            "KCS_Cross_Sell_Winback_Product_ID": "",
            "Identity_Protection_Product_Id": consumer_row[0]["identity_protection"],
            "Prescription_Savings_Product_Id": consumer_row[0]["prescription_savings"],
            "Vision_Insurance_Product_Id": consumer_row[0]["vision_insurance"],
            "Dental_Insurance_Product_Id": consumer_row[0]["dental_insurance"],
            "Asset_Protection_Product_Id": consumer_row[0]["asset_protection"],
            "Marketplace_Product_Id": consumer_row[0]["marketplace_product_id"]
        }
    }

    # when
    actual = map_row_to_marketingcloud_api(consumer_row[0], valid_fi_ids[0])

    # then
    assert expected == actual
