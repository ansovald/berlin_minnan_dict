def build_search_pattern(search_term, gloss_search=False, case_insensitive=False):
    # Returns op: REGEXP/= and search_term
    if search_term[0] == '@':
        if gloss_search:
            return 'REGEXP', '\\b' + search_term[1:] + '\\b'
        return '=', search_term[1:]
    elif '*' in search_term:
        if search_term[0] == '*':
            search_term = '.*' + search_term[1:]
        else:
            search_term = '\\b' + search_term
        if search_term[-1] == '*':
            search_term = search_term[:-1] + '.*'
        else:
            search_term = search_term + '\\b'
    elif search_term[0] == '/' and search_term[-1] == '/':
        search_term = search_term[1:-1]
    else:
        search_term = '.*' + search_term + '.*'
    
    if case_insensitive:
        search_term = f"(?i){search_term}"  # Add case-insensitive flag to the regex
    
    return 'REGEXP', search_term