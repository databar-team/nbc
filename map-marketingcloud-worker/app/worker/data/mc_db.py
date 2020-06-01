from kasasa_common.database.connection import Connection
from kasasa_common.logger import logger


class McDb:
    """
    DB Model for Mc
    :param connection: Connection
    """
    def __init__(self, connection: Connection = None):
        """
        Attributes _table, _table_fields_map are REQUIRED for db-table opperations.
        """
        self._connection = connection
        self._table = ""
        self._table_fields_map = {}
        self._insert_sql_statement = "INSERT INTO `{fi_id}`.`{table}` ({fields}) VALUES {values}"
        self._on_duplicate_key_update = "ON DUPLICATE KEY UPDATE {update_value}"

    def _create_update_values(self):
        base_string = '`{field}` = VALUES(`{field}`)'
        return ", ".join([base_string.format(field=field) for field in self._table_fields_map])

    def _get_mask_values(self, values):
        """
        Generates a tuple with the required mask and flattened values for multiple row insertion.
        Validation is performed in this process.
        :param values: list List of dict()
        """
        mask = []
        mask_values = []
        set_values_mask = f"({','.join(['%s' for val in self._table_fields_map])})"
        for set_of_values in values:
            # Get Values as a list
            if self.validate(set_of_values):
                # Append Mask
                mask.append(set_values_mask)

                # Append Values
                flattened_values = self._flattened_data(set_of_values)
                mask_values += flattened_values
            else:
                logger.warning("No valid record found. It was not processed.")

        return ','.join(mask), mask_values

    def _flattened_data(self, set_of_values):
        """
        Performs basic processing of set of values. This method could be overwritten to provide more specific process.
        :param set_of_values: dict()
        """
        return [set_of_values.get(field, 'NULL') for field in self._table_fields_map.values()]

    def _build_sql(self, values=[], fi_id=None, on_duplicate_key_update=False):
        """
        Generates sql statement and a list of values to be used in a cursor.execute() method
        :param values: list List of dict()
        """
        mask, insert_values = self._get_mask_values(values)
        sql = self._insert_sql_statement.format(
            fi_id=fi_id,
            table=self._table,
            fields=','.join([f"`{key}`" for key in self._table_fields_map.keys()]),
            values=mask
        )
        if on_duplicate_key_update:
            update_value = self._create_update_values()
            on_dupe = self._on_duplicate_key_update.format(update_value=update_value)
            sql = "\n".join([sql, on_dupe])

        return sql, insert_values

    def insert(self, values=dict(), fi_id=None, on_duplicate_key_update=False):
        """
        Inserts given dict() containing ONE set of values to be inserted.
        :param values: list
        """
        return self.insert_many(values=[values],
                                fi_id=fi_id,
                                on_duplicate_key_update=on_duplicate_key_update)

    def insert_many(self, values=[], fi_id=None, on_duplicate_key_update=False):
        """
        Inserts given list of dict()'s containing records to be inserted.
        :param values: list List of dict()
        """
        affected_rows = 0
        sql, insert_values = self._build_sql(values=values,
                                             fi_id=fi_id,
                                             on_duplicate_key_update=on_duplicate_key_update)

        if insert_values:
            affected_rows = self._connection.insert_with_sql(sql, insert_values)

        logger.info(f"{len(values)} records received to be processed, {affected_rows} records inserted into the DB.")

        return affected_rows

    def validate(self, set_of_values):
        """
        Required Validation for the Model
        If 'False' the set of values won't be processed for insertion.
        """
        return True
