import requests
import os
from tableauhyperapi import HyperProcess, Connection, Telemetry, CreateMode, \
TableDefinition, TableName, SqlType, Inserter
from settings import COLUMN_NAMES
from validations import validate_search_term



def get_items(url, search_term, n_items):
    """get_items Retrieves items from an API based on the provided URL, search term, and number of items.

    Parameters:
        url (str): The URL of the API to retrieve items from.
        search_term: The search term to use for querying the API.
        n_items (int): The total number of items to retrieve.

    offset (int): The offset value to specify the starting point for retrieving items

    Raises:
        requests.exceptions.RequestException: If an error occurs during the API request.

    Returns:
        list: A list of items retrieved from the API.
        """
    items = []
    offset = 0
    try:
        while offset < n_items:
            params = {
                'query': search_term,
                'offset': offset,
                'limit': min((n_items - len(items), 50))
            }

            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            results = data.get('results', [])
            items += results
            offset += len(results)

    except requests.exceptions.RequestException as e:
        print(f'Error occurred during API request: {str(e)}')
        
    return items
    

def create_hyper_table_definition():
    """
    Creates the table structure for the Hyper file.
    
    This function defines the table name, column names, and data types for each column.
    
    Returns:
        The table structure definition.
    """
    
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
    """
    Inserts items into a table in the Hyper file using the provided connection, table, items, and column names.
    
    Parameters:
        connection (tableauhyperapi.Connection): The connection to the Hyper file.
        table (tableauhyperapi.TableDefinition): The table definition of the target table.
        items (list): A list of items to be inserted into the table.
        column_name (list): A list of column names corresponding to the items' attributes.
    
    Returns:
        None
    
    Exeption:
        except if exist a problem during insertion of items
    
    """
    with Inserter(connection, table) as inserter:
        try:
            for item in items:
                row = [item.get(column, 'error') for column in column_name]
                inserter.add_row(row)
            inserter.execute()
        except Exception as e:
            print(f"There is an error with the insert data: {str(e)}")


def hyper_structure_generator(search_term):
    """
    Main function that generates the Hyper file structure by querying the API, creating a table, and inserting data.
    
    This function serves as the entry point and makes use of the following functions:
    - get_items: Retrieves items from the API based on the search term.
    - create_hyper_table_definition: Creates the table structure for the Hyper file.
    - insert_items_table: Inserts the retrieved items into the table.
    
    Parameters:
        search_term (str): The search term to use for querying the API.
        
    Returns:
        str: The local path of the generated Hyper file.
    
    Raises:
        None
    
    """
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
    

if __name__ == '__main__':
    search_term = input('What do you want to search: ')
    if validate_search_term(search_term):
        hyper_path = hyper_structure_generator(search_term)
        print(f'Executed successfully, the hyper file is in the path {hyper_path}')
