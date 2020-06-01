"""create_sfmc_product_master_table

Revision ID: 7bb04897c433
Revises: 
Create Date: 2020-05-07 11:12:11.695779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7bb04897c433'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'sfmc_product_master',
        sa.Column('salesforce_product_id', sa.String(50), primary_key=True),
        sa.Column('fi_crm_record_id', sa.String(40)),
        sa.Column('product_name', sa.String(18)),
        sa.Column('krp_base_product_id', sa.Integer),
        sa.Column('market_this_product', sa.String(255)),
        sa.Column('product_priority', sa.String(255)),
        sa.Column('opt_in_status', sa.String(255)),
        sa.Column('product_type', sa.String(50)),
    )


def downgrade():
    op.drop_table('sfmc_product_master')
