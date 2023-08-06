import pymssql

import pandas as pd

from toucan_connectors.abstract_connector import AbstractConnector, MissingQueryParameter


class MSSQLConnector(AbstractConnector, type='MSSQL'):
    """ A back-end connector to retrieve data from a MSSQL database """

    def __init__(self, *, host, user,
                 db=None, password=None, port=None, connect_timeout=None):
        self.params = {
            'server': host,
            'user': user,
            'database': db,
            'password': password,
            'port': port,
            'login_timeout': connect_timeout,
            'as_dict': True
        }
        # remove None value
        self.params = {k: v for k, v in self.params.items() if v is not None}
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = pymssql.connect(**self.params)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.connection.close()

    def _query(self, query):
        """ query and get_df are basically the same and return a df """
        return pd.read_sql(query, con=self.connection)

    def _get_df(self, config):
        """ query and get_df are basically the same and return a df """
        if 'query' not in config:
            raise MissingQueryParameter('query must be in the config')
        query = config['query']
        self.logger.info(f'{query} : executing...')
        return self._query(query.encode('utf8'))
