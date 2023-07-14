import pytest
import requests
from main import get_items
from main import create_hyper_table_definition


def test_get_items_raises_exception_when_response_is_not_200():
    # Object of false response. This cound be a wrong URL
    any_response = requests.Response()
    any_response.status_code = 400

    # `get_items()` with the object of false response
    with pytest.raises(requests.exceptions.RequestException):
        get_items(any_response, 'search_term', 10)




def test_create_hyper_table_definition():
    # Call the function to get the structure of the table
    table_definition = create_hyper_table_definition()

    # Check that the return value is not None
    assert table_definition is not None
