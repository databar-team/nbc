from .mc_db import McDb
from kasasa_common.database.connection import Connection


class FiMarketingCloud(McDb):
    
    def __init__(self, connection: Connection = None):
        super(FiMarketingCloud, self).__init__(connection)
        self._table = 'sfmc_product_master'
        self._table_fields_map = {
           "salesforce_product_id": "AcctProdIDFull__c",
           "fi_crm_record_id": "AcctProductExternalID__c",
           "product_type": "Product Class",
           "product_name": "Product__c",
           "krp_base_product_id": "BillingKrpPid__c",
           "market_this_product": "Market_This_Product",
           "product_priority": "Product_Priority",
           "opt_in_status": "Opt-In_Status"
        }
        
    def validate(self, set_of_values):
        return set_of_values.get('AcctProdIDFull__c') is not None