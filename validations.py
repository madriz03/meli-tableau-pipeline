def validate_search_term(search_term):
    if search_term.strip():
        return True
    else:
        print('Error: Search term cannot be empty')
        return False
