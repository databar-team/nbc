import threading
from time import sleep
from queue import Full

import data.consumer

from config.context import get_context
from external_accessor.db import get_db_connection
from util.logger import logger
from client.marketing_cloud import MarketingCloudClient
from concurrency.producer_consumer import ProducerConsumer

PER_THREAD_BATCH_LIMIT = 15


def send():
    context = get_context()

    client = MarketingCloudClient()
    client.set_access_token(context)

    valid_fi_ids = get_valid_fi_ids(context)

    if not len(valid_fi_ids):
        logger.info("No valid FIs to send to Marketing Cloud.")
        return

    cp = ProducerConsumer(context, client, valid_fi_ids)

    cp.add_producer("customer_producer", customer_producer_func)
    cp.add_producer("acxiom_prospect_producer", acxiom_prospect_producer_func)
    cp.add_producer("fico_prospect_producer", fico_prospect_producer_func)

    cp.set_consumer_func(consumer_func)
    cp.set_num_consumers(5)

    logger.info("Starting sending process with batch size of {}...".format(data.consumer.BATCH_SIZE))

    cp.run()

    logger.info("Done sending data to Marketing Cloud API.")

    # updating the task_last_run table for the FI to signal that there were no batches with errors
    if client.successful_fis:
        for fi_id in client.successful_fis:
            connection = get_db_connection(context, database="fi_{}".format(fi_id))

            if not connection.open:
                logger.info("Connection to DB failed.")
                return

            data.consumer.mark_run_as_successful(connection)

            connection.close()

            logger.info("Updated task_last_run for successful send for FI {}.".format(fi_id))


def get_valid_fi_ids(context):
    conn = get_db_connection(context, database="map_config")

    valid_fi_ids = data.consumer.get_valid_fi_ids(conn)

    conn.close()

    return valid_fi_ids


def consumer_func(context, client, msg):
    batch_num = msg["batch_num"]
    fi_id = msg["fi_id"]
    data = msg["data"]

    logger.debug(
        "Sending batch {} for FI {} from thread {}".format(batch_num, fi_id, threading.current_thread().getName()))

    client.send(context, fi_id, data)

    logger.debug("Sent batch {} for FI {} from thread {}".format(batch_num, fi_id, threading.current_thread().getName()))


def customer_producer_func(context, queue, fi_id):
    producer_func(context, queue, fi_id, data.consumer.get_recently_changed_customers_generator)


def acxiom_prospect_producer_func(context, queue, fi_id):
    producer_func(context, queue, fi_id, data.consumer.get_new_acxiom_prospects_generator)


def fico_prospect_producer_func(context, queue, fi_id):
    producer_func(context, queue, fi_id, data.consumer.get_new_fico_prospects_generator)


def producer_func(context, queue, fi_id, db_func):
    connection = get_db_connection(context, database="fi_{}".format(fi_id))

    if not connection.open:
        logger.info("Connection to DB failed.")
        return

    gen = db_func(connection)

    batch_consumers(fi_id, gen, queue)

    gen = None

    logger.info("Queued all batches for FI {} from thread {}".format(fi_id, threading.current_thread().getName()))

    connection.close()


def batch_consumers(fi_id, generator, q, batch_limit=PER_THREAD_BATCH_LIMIT):
    logger.info("Starting API batching for FI {}".format(fi_id))

    # iterate over each consumer
    num_batches = 0

    for batch in generator:
        api_batch = []
        num_batches += 1
        # TODO: Modify generator SQL to name fields instead of iterating over them all
        for row in batch:
            api_batch.append(map_row_to_marketingcloud_api(row, fi_id))

        # send to MC when we have gathered enough for batch limit

        while True:
            try:
                q.put({
                    "batch_num": num_batches,
                    "fi_id": fi_id,
                    "data": api_batch
                }, False)
                break
            except Full:
                sleep(1)
            except Exception:
                logger.exception('Failed to put data on the worker queue')
            
        logger.debug("Queuing batch {} for FI {} from thread {}".format(num_batches, fi_id,
                                                                       threading.current_thread().getName()))

    logger.info(f"Completed delivery of marketing cloud messages for FI {fi_id}, {num_batches} were delivered")


def map_row_to_marketingcloud_api(row, fi_id):
    return {
        "keys": {
            "Subscriber_Key": row["surrogate_id"]
        },
        "values": {
            "Person_ID": row["person_link_id"],
            "FI_ID_Number": fi_id,
            "Contact_Status": row["contact_status"],
            "Full_Name": row["full_name"],
            "First_Name": row["first_name"],
            "Middle_Name": row["middle_name"],
            "Last_Name": row["last_name"],
            "Suffix": row["suffix"],
            "Primary_Address": row["address_1"],
            "Secondary_Address": row["address_2"],
            "City": row["city"],
            "State": row["state"],
            "Zip_Code": row["zipcode"],
            "Zip_4": row["zipcode_extended"],
            "Email_Address": row["email_address"],
            "Phone": row["phone_number"],
            "Urbanicity": "",
            "Audience": "All",
            "Prospect_Product_ID": "Null",
            "Welcome_Product_ID": "",
            "Enter_Birthday": row.get("enter_birthday", ""),
            "Enter_Anniversary": row.get("enter_anniversary", ""),
            "Adoption_Type": "",
            "Adoption_Product_ID": "",
            "KCS_Cross_Sell_Product_ID": "",
            "KCS_Cross_Sell_Winback_Product_ID": "",
            "Identity_Protection_Product_Id": row.get("identity_protection", "0"),
            "Prescription_Savings_Product_Id": row.get("prescription_savings", "0"),
            "Vision_Insurance_Product_Id": row.get("vision_insurance", "0"),
            "Dental_Insurance_Product_Id": row.get("dental_insurance", "0"),
            "Asset_Protection_Product_Id": row.get("asset_protection", "0"),
            "Marketplace_Product_Id": row.get("marketplace_product_id", "0"),
            "KLS_Cross_Sell_Product_ID":row["kasasa_personal_loans"]
        }
    }
