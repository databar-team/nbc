"""tests

Revision ID: 225dd1b9769d
Revises: 
Create Date: 2020-02-18 09:44:20.018843

"""
from alembic import op
import sqlalchemy as sa
import os


# revision identifiers, used by Alembic.
revision = '225dd1b9769d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # creating subset schema since we don't use all columns
    conn = op.get_bind()

    conn.execute("CREATE DATABASE IF NOT EXISTS map_global_data;")

    op.create_table(
        'feature_signup',
        sa.Column('financial_institution_id', sa.Integer),
        sa.Column('active_start_date', sa.Date),
        sa.Column('active_end_date', sa.Date),
        sa.Column('marketing_cloud', sa.SmallInteger),
    )

    op.create_table(
        'customer_attribute',
        sa.Column('customer_kasasa_key', sa.String(100)),
        sa.Column('attribute_object', sa.JSON)
    )

    op.create_table(
        'customer_attribute_hashes',
        sa.Column('customer_kasasa_key', sa.String(100)),
        sa.Column('date_last_updated', sa.DATETIME)
    )

    op.create_table(
        'customer',
        sa.Column('customer_kasasa_key', sa.String(100)),
        sa.Column('full_name', sa.String(100)),
        sa.Column('first_name', sa.String(50)),
        sa.Column('middle_name', sa.String(30)),
        sa.Column('last_name', sa.String(50)),
        sa.Column('suffix', sa.String(10))
    )

    op.create_table(
        'surrogates',
        sa.Column('surrogate_id', sa.BigInteger, primary_key=True),
        sa.Column('record_key', sa.String(100))
    )

    op.create_table(
        'surrogate_person_link_mappings',
        sa.Column('surrogate_id', sa.BigInteger, primary_key=True),
        sa.Column('person_link_id', sa.String(32)),
        sa.Column('financial_institution_id', sa.Integer),
        sa.Column('person_link_update_datetime', sa.DATETIME, server_default=sa.func.current_timestamp()),
        schema="map_global_data"
    )

    op.create_table(
        'acxiom_sourced_prospects',
        sa.Column('prospect_kasasa_key', sa.String(100)),
        sa.Column('full_name', sa.String(100), nullable=True),
        sa.Column('first_name', sa.String(50), nullable=True),
        sa.Column('middle_name', sa.String(30), nullable=True),
        sa.Column('last_name', sa.String(50), nullable=True),
        sa.Column('city', sa.String(30), nullable=True),
        sa.Column('state', sa.String(2), nullable=True),
        sa.Column('zipcode', sa.String(5), nullable=True),
        sa.Column('address_1', sa.String(49), nullable=True),
        sa.Column('address_2', sa.String(33), nullable=True),
        sa.Column('zipcode_extended', sa.String(4), nullable=True),
        sa.Column('email', sa.String(100), nullable=True),
        sa.Column('email_2', sa.String(100), nullable=True),
        sa.Column('expiration_date', sa.DATETIME),
        sa.Column('data_load_date', sa.DATETIME, server_default=sa.func.current_timestamp())
    )

    op.create_table(
        'fico_sourced_prospects',
        sa.Column('prospect_kasasa_key', sa.String(100)),
        sa.Column('full_name', sa.String(100), nullable=True),
        sa.Column('first_name', sa.String(50), nullable=True),
        sa.Column('middle_name', sa.String(30), nullable=True),
        sa.Column('last_name', sa.String(50), nullable=True),
        sa.Column('suffix', sa.String(10), nullable=True),
        sa.Column('city', sa.String(30), nullable=True),
        sa.Column('state', sa.String(2), nullable=True),
        sa.Column('zipcode', sa.String(5), nullable=True),
        sa.Column('address_1', sa.String(49), nullable=True),
        sa.Column('address_2', sa.String(33), nullable=True),
        sa.Column('zipcode_extended', sa.String(4), nullable=True),
        sa.Column('email', sa.String(100), nullable=True),
        sa.Column('phone_number', sa.String(100), nullable=True),
        sa.Column('expiration_date', sa.DATETIME),
        sa.Column('data_load_date', sa.DATETIME, server_default=sa.func.current_timestamp())
    )

    op.create_table(
        'prospect_customer_mapping',
        sa.Column('prospect_kasasa_key', sa.String(100)),
        sa.Column('customer_kasasa_key', sa.String(100)),
        sa.Column('financial_institution_id', sa.BigInteger),
        sa.Column('data_load_date', sa.DATETIME)
    )

    op.create_table(
        'task_last_run',
        sa.Column('run_id', sa.BigInteger),
        sa.Column('task_id', sa.BigInteger),
        sa.Column('last_run_date_time', sa.DATETIME, server_default=sa.func.current_timestamp())
    )

    seed_data(conn)

def downgrade():
    conn = op.get_bind()

    conn.execute("DROP DATABASE IF EXISTS map_global_data;")

    op.drop_table('feature_signup')
    op.drop_table('customer_attribute')
    op.drop_table('customer_attribute_hashes')
    op.drop_table('customer')
    op.drop_table('surrogates')
    op.drop_table('fico_sourced_prospects')
    op.drop_table('acxiom_sourced_prospects')
    op.drop_table('prospect_customer_mapping')
    op.drop_table('task_last_run')

def seed_data(conn):
    conn.execute(
        """INSERT INTO `feature_signup` (`financial_institution_id`, `active_start_date`, `active_end_date`, `marketing_cloud`)
            VALUES
                (2211, '2020-02-01', '9999-12-31', 1);
        """)
    conn.execute(
        """INSERT INTO `acxiom_sourced_prospects` (`prospect_kasasa_key`, `full_name`, `email`, `expiration_date`, `data_load_date`)
            VALUES
                ('2211-dummy_prospect_kasasa_key_a_a', 'DUMMY RECORD Prospect', 'noreply@kasasa.com', DATE_ADD(CURDATE(), INTERVAL 1 YEAR), DATE_ADD(CURDATE(), INTERVAL 7 DAY)),
                ('2211-dummy_prospect_kasasa_key_a_a_2', 'DUMMY RECORD Converted', 'noreply@kasasa.com', DATE_ADD(CURDATE(), INTERVAL 1 YEAR), DATE_SUB(CURDATE(), INTERVAL -1 DAY));
        """)

    conn.execute(
        """INSERT INTO `fico_sourced_prospects` (`prospect_kasasa_key`, `full_name`, `email`, `phone_number`, `expiration_date`, `data_load_date`)
            VALUES
                ('2211-dummy_prospect_kasasa_key', 'DUMMY RECORD', 'noreply@kasasa.com', '555-555-5555', DATE_ADD(CURDATE(), INTERVAL 1 YEAR), DATE_ADD(CURDATE(), INTERVAL -1 DAY));
        """)

    conn.execute(
        """INSERT INTO `customer` (`customer_kasasa_key`, `first_name`, `last_name`)
            VALUES
                ('0004e6cc-75c8-11e8-8c02-027b0d8eb925', 'Nicholas', 'Keith'),
                ('0005c4d2-6ac9-11e8-8c02-027b0d8eb925', 'Bobby', 'McPherson'),
                ('0005c6a1-6ac9-11e8-8c02-027b0d8eb925', 'Taylor', 'Peck');
        """)

    conn.execute(
        """INSERT INTO `customer_attribute` (`customer_kasasa_key`, `attribute_object`)
            VALUES
                ('0004e6cc-75c8-11e8-8c02-027b0d8eb925', '{"city": "Hagan", "state": "OF", "zipcode": "09165", "address_1": "458 Arlington Rd", "address_2": null, "phone_number": null, "dda_relationship": 0, "zipcode_extended": null, "customer_since_date": "1998-04-13", "customer_date_of_birth": "1977-03-05", "customer_email_address": "vdunlap1@ma1l2u.us", "customer_account_holder": 0, "customer_kasasa_start_date": "9999-12-31", "customer_kasasa_account_holder": 0, "beta_customer_kasasa_start_date": "9999-12-31", "customer_kasasa_cash_start_date": "9999-12-31", "customer_kasasa_cash_account_holder": 0, "customer_kasasa_cash_back_start_date": "9999-12-31", "customer_kasasa_saver_account_holder": 0, "customer_kasasa_cash_back_account_holder": 0}'),
                ('0005c4d2-6ac9-11e8-8c02-027b0d8eb925', '{"city": "Hagan", "state": "OF", "zipcode": "18771", "address_1": "1502 Pennisula Square", "address_2": null, "phone_number": null, "dda_relationship": 0, "zipcode_extended": null, "customer_since_date": "2018-06-07", "customer_date_of_birth": "1961-12-02", "customer_email_address": "numbershot@yah00.us", "customer_account_holder": 0, "customer_kasasa_start_date": "9999-12-31", "customer_kasasa_account_holder": 0, "beta_customer_kasasa_start_date": "9999-12-31", "customer_kasasa_cash_start_date": "9999-12-31", "customer_kasasa_cash_account_holder": 0, "customer_kasasa_cash_back_start_date": "9999-12-31", "customer_kasasa_saver_account_holder": 0, "customer_kasasa_cash_back_account_holder": 0}'),
                ('0005c6a1-6ac9-11e8-8c02-027b0d8eb925', '{"city": "Hagan", "state": "OF", "zipcode": "72178", "address_1": "1110 Harlan Court", "address_2": null, "phone_number": null, "dda_relationship": 0, "zipcode_extended": null, "customer_since_date": "2018-06-07", "customer_date_of_birth": "1963-09-18", "customer_email_address": "illthey@somema1l.us", "customer_account_holder": 0, "customer_kasasa_start_date": "9999-12-31", "customer_kasasa_account_holder": 0, "beta_customer_kasasa_start_date": "9999-12-31", "customer_kasasa_cash_start_date": "9999-12-31", "customer_kasasa_cash_account_holder": 0, "customer_kasasa_cash_back_start_date": "9999-12-31", "customer_kasasa_saver_account_holder": 0, "customer_kasasa_cash_back_account_holder": 0}');
        """)

    conn.execute(
        """INSERT INTO `customer_attribute_hashes` (`customer_kasasa_key`, `date_last_updated`)
            VALUES
                ('0004e6cc-75c8-11e8-8c02-027b0d8eb925', DATE_ADD(CURDATE(), INTERVAL 1 DAY)),
                ('0005c4d2-6ac9-11e8-8c02-027b0d8eb925', DATE_ADD(CURDATE(), INTERVAL 1 DAY)),
                ('0005c6a1-6ac9-11e8-8c02-027b0d8eb925', DATE_ADD(CURDATE(), INTERVAL -1 DAY));
        """)

    conn.execute(
        """INSERT INTO `surrogates` (`surrogate_id`, `record_key`)
            VALUES
                (24600024, '2211-dummy_prospect_kasasa_key_a_a_2'),
                (24600023, '2211-dummy_prospect_kasasa_key_a_a'),
                (34600023, '2211-dummy_prospect_kasasa_key'),
                (24567242, '0004e6cc-75c8-11e8-8c02-027b0d8eb925'),
                (24567243, '0005c4d2-6ac9-11e8-8c02-027b0d8eb925'),
                (24567244, '0005c6a1-6ac9-11e8-8c02-027b0d8eb925');
        """)

    conn.execute(
        """INSERT INTO `map_global_data`.`surrogate_person_link_mappings` (`surrogate_id`, `person_link_id`, `financial_institution_id`)
            VALUES
                (24567242, '24567242mctest', 1122),
                (24567243, '24567243mctest', 1122),
                (24567244, '24567244mctest', 1122),
                (24600023, '24600023mctest', 1122),
                (24600024, '24600023mctest', 1122),
                (34600023, '34600023mctest', 1122);
        """)
    conn.execute(
        """
        UPDATE `map_global_data`.`surrogate_person_link_mappings`
        SET
        person_link_update_datetime = DATE_ADD(NOW(), INTERVAL 8 DAY);
        """
    )
    conn.execute(
        """INSERT INTO `prospect_customer_mapping` (`prospect_kasasa_key`, `customer_kasasa_key`, `financial_institution_id`, `data_load_date`)
            VALUES
            ('2211-dummy_prospect_kasasa_key_a_a_2', '2211-dummy_customer_kasasa_key_a_a_2', 2211, DATE_ADD(CURDATE(), INTERVAL 2 DAY));
        """)
    conn.execute(
        """INSERT INTO `task_last_run` (`run_id`, `task_id`)
            VALUES (1,1);
        """)