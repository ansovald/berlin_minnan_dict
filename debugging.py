
if __name__ == '__main__':
    from query_database import query_wiktionary_entries, query_hanzi, get_session
    from time import time
    start_time = time()
    session = get_session()
    # print(query_hanzi('洪'))
    # query_hanzi('堡')
    # wiktionary_entries = query_wiktionary_entries(hanzi='洪堡', session=session)
    # wiktionary_entries = query_wiktionary_entries(hokkien='^k.*', english='@shit', syllable_count=2, session=session)
    wiktionary_entries = query_wiktionary_entries(hokkien='^k*', session=session)
    for i, entry in enumerate(wiktionary_entries):
        print(f'Entry {i+1}:')
        for key in entry:
            print(f'\t{key}:')
            print(f'\t\t{entry[key]}')
        print()
    print(f'Execution time: {time() - start_time} seconds')