import requests
import os
from tableauhyperapi import HyperProcess, Connection, Telemetry, CreateMode, \
TableDefinition, TableName, SqlType, Inserter
from settings import COLUMN_NAMES
from validations import validate_search_term


def get_items(url, search_term, n_items):
    items = []
    offset = 0
    while offset < n_items:
        params = {
            'query': search_term,
            'offset': offset,
            'limit': min((n_items - len(items), 50))
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            items += results
            offset += len(results)

        else:
            print('error')
        
    return items
    

def create_hyper_table_definition():
    table = TableDefinition(TableName('data_meli', 'data_meli'), [
        TableDefinition.Column('id', SqlType.text()),
        TableDefinition.Column('title', SqlType.text()),
        TableDefinition.Column('condition', SqlType.text()),
        TableDefinition.Column('price', SqlType.double()),
        TableDefinition.Column('sold_quantity', SqlType.big_int()),
        TableDefinition.Column('available_quantity', SqlType.big_int())
    ])
    return table


def insert_items_table(connection, table, items, column_name):
    with Inserter(connection, table) as inserter:
        try:
            for item in items:
                row = [item.get(column, 'error') for column in column_name]
                inserter.add_row(row)
            inserter.execute()
        except Exception as e:
            print(f"There is an error with the insert data: {str(e)}")


def hyper_structure_generator(search_term):
    local_path = os.path.join(os.getcwd(), 'public_data_meli.hyper')
    with HyperProcess(Telemetry.SEND_USAGE_DATA_TO_TABLEAU,
                       parameters={"default_database_version": "2"}) as hyper:
        with Connection(endpoint=hyper.endpoint, database=local_path, create_mode=CreateMode.CREATE_AND_REPLACE) as connection:
            connection.catalog.create_schema('data_meli')


            url = f'https://api.mercadolibre.com/sites/MLA/search?q={search_term}&limit=50#json'
            items = get_items(url, search_term, n_items=150)
            table = create_hyper_table_definition()
            connection.catalog.create_table(table)

            column_name = COLUMN_NAMES

            insert_items_table(connection, table, items, column_name)

        return local_path
    

search_term = input('What do you want to search: ')
if validate_search_term(search_term):
    hyper_path = hyper_structure_generator(search_term)
    print(f'Executed successfully, the hyper file is in the path {hyper_path}')
