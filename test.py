import requests
import json
import os
from tableauhyperapi import HyperProcess, Connection, Telemetry, CreateMode, \
    TableDefinition, TableName, SqlType, Inserter
from settings import URL, COLUMN_NAMES


# I have to get data from API MELI

def get_items(search_term, n_items):
    search_term = input('What do you want? ')
    url = f'https://api.mercadolibre.com/sites/MLA/search?q={search_term}&limit=50#json'
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


# I have to generate hyper and I need to define the data structure table

def hyper_structure_generator(search_term):
    local_path = os.path.join(os.getcwd(), 'public_data_meli.hyper') # Tabla
    with HyperProcess(Telemetry.SEND_USAGE_DATA_TO_TABLEAU,
                parameters = {"default_database_version": "2"}) as hyper:
        with Connection(endpoint=hyper.endpoint, database=local_path, create_mode=CreateMode.CREATE_AND_REPLACE) as connection:
            connection.catalog.create_schema('data_meli') # schema

            # I will get 150 productos from meli API
            items = get_items(search_term, n_items=150)
            # create columns names with intems from get_products for table
            column_names = COLUMN_NAMES
            
            table = TableDefinition(TableName('data_meli', 'data_meli'), [
            TableDefinition.Column('id', SqlType.text()),
            TableDefinition.Column('title', SqlType.text()),
            TableDefinition.Column('condition', SqlType.text()),
            TableDefinition.Column('price', SqlType.double()),
            TableDefinition.Column('sold_quantity', SqlType.big_int()),
            TableDefinition.Column('available_quantity', SqlType.big_int())
            
        ])
            connection.catalog.create_table(table)

            # Insert elements into the table
            with Inserter(connection, table) as inserter:
                try:
                    for item in items:
                        
                        row = [item.get(column, 'error') for column in column_names]
                        inserter.add_row(row)
                    inserter.execute()
                except Exception as e:
                    print(f"Error al insertar los datos en la tabla: {str(e)}")
   
    return local_path


# Use example
search_term = input('What do you want to search?: ')
hyper_path = hyper_structure_generator(search_term)
print(f'se ejecuto todo {hyper_path}')