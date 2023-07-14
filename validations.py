"""
This function validates the search_term.
The search_term cannot be empty. If the search_term is empty,
an error message will be displayed. If the search_term is not empty,
the code will execute.
"""

def validate_search_term(search_term):
    if search_term.strip():
        return True
    else:
        print('Error: Search term cannot be empty')
        return False
