def build_search_pattern(search_term, gloss_search=False, case_sensitive=True, hanzi_search=False):
    # Returns operator `REGEXP` or `=` and search_term
    # operator = '=' if gloss_search else 'REGEXP'
    if search_term[0] == '/' and search_term[-1] == '/':
        search_term = search_term[1:-1]
    else:
        if gloss_search:
            search_term = '\\b' + search_term + '\\b'
            search_term = search_term.replace('*', '.*')
        elif hanzi_search:
            search_term = search_term.replace('*', '.*')
        else:
            if not search_term[0] == '*':
                search_term = '\\b' + search_term
            if not search_term[-1] == '*':
                search_term = search_term + '\\b'
            search_term = search_term.replace('*', '.*')
    
    if not case_sensitive:
        search_term = f"(?i){search_term}"  # Add case-insensitive flag to the regex
    
    return 'REGEXP', search_term