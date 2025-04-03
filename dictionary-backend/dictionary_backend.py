from flask import Flask, jsonify, request #, api_session
from flask_cors import CORS
from query_database import get_session, query_wiktionary_entries, get_wiktionary_entry, get_sutian_lemma
import time
import hashlib
import json
# session = get_session()

CACHE_TIME_THRESHOLD = 3

app = Flask(__name__)
CORS(app)

def time_since(since):
    now = time.time()
    s = now - since
    m = s // 60
    s -= m * 60
    return f'{int(m)}m {int(s)}s'

def query_log(start_time, **params):
    from datetime import datetime
    with open('../logs/query_log.txt', 'a') as f:
        log_dict = { 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], 'time': f'{time.time()-start_time:.2f}'}
        log_dict.update({k: v for k, v in params.items() if v})
        f.write(str(log_dict) + '\n')

def cache_result(results, start_time, time_threshold=CACHE_TIME_THRESHOLD, **params):
    # If the query took longer than the threshold, log it to `query_log.txt` and cache it
    if time.time() - start_time > time_threshold:
        query_log(start_time, **params)
        save_cached_result(results, **params)

def save_cached_result(results, **params):
    # Create a unique identifier for the search parameters, using a hash of the parameters
    hash_params = hashlib.md5(str(params).encode()).hexdigest()
    with open(f'cache/{hash_params}.json', 'w') as f:
        json.dump(results, f)

def load_cached_result(**params):
    hash_params = hashlib.md5(str(params).encode()).hexdigest()
    try:
        with open(f'cache/{hash_params}.json', 'r') as f:
            print(f"Loaded cached result for {params}")
            return json.load(f)
    except FileNotFoundError:
        return None

@app.route('/api/search', methods=['POST'])
def search_entries():
    params = request.json
    last_entry_id = params.pop('last_entry_id', None)  # Extract last_entry_id if provided
    # Ensure a session is created
    session = get_session()
    try:
        if not any(params.values()):
            return jsonify({"error": "No valid search parameters provided"}), 400

        start_time = time.time()
        results_data = query_wiktionary_entries(**params, last_entry_id=last_entry_id, session=session)
        print(f"Found {len(results_data['results'])} entries matching the search criteria, took {time_since(start_time)}")
        print(results_data['results'][0])
        return jsonify(results_data)  # Return the dict with results and last_entry_id
    finally:
        session.close()

# @app.route('/api/search', methods=['GET'])
# def api_lookup():
#     hanzi = request.args.get('hanzi', '')
#     hokkien = request.args.get('hokkien', '')
#     english = request.args.get('english', '')
#     syllable_count = request.args.get('syllable_count', '')
#     results = query_wiktionary_entries(hanzi=hanzi, hokkien=hokkien, english=english, syllable_count=syllable_count, session=session)
#     return jsonify(results)

# @app.route('/api/entry/<entry_id>', methods=['GET'])
# def api_entry(entry_id):
#     entry = get_wiktionary_entry(entry_id=entry_id, session=session)
#     return jsonify(entry)

# @app.route('/api/lemma/<lemma_id>', methods=['GET'])
# def api_lemma(lemma_id):
#     lemma = get_sutian_lemma(lemma_id=lemma_id, session=session)
#     return jsonify(lemma)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
