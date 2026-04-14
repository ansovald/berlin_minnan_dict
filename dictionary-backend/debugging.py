
from query_database import query_wiktionary_entries, get_session
from time import time
import json

if __name__ == '__main__':
    start_time = time()
    session = get_session()
    # print(query_hanzi('洪'))
    # query_hanzi('堡')
    # wiktionary_entries = query_wiktionary_entries(hanzi='洪堡', session=session)
    wiktionary_entries = query_wiktionary_entries(english='exempt', hokkien='/^h?ua/', session=session, verbose=True, page_size=200)
    # wiktionary_entries = query_wiktionary_entries(hokkien='^k*', session=session)
    print(f'Found {len(wiktionary_entries["results"])} entries.')
    # for i, entry in enumerate(wiktionary_entries['results']):
    #     print(f'Entry {i+1}:')
    #     try:
    #         for key in entry:
    #             print(f'\t{key}:')
    #             print(f'\t\t{json.dumps(entry[key], ensure_ascii=False, indent=2)}')
    #     except Exception as e:
    #         print(f'Error printing entry: {e}')
    #         print(f'\t{entry}')
    #     print()
    print(f'Execution time: {time() - start_time} seconds')
    with open('query_results.json', 'w', encoding='utf-8') as f:
        json.dump(wiktionary_entries, f, ensure_ascii=False, indent=4)