from flask import Flask, jsonify, request #, api_session
from flask_cors import CORS
from query_database import get_session, query_wiktionary_entries, get_wiktionary_entry, get_sutian_lemma
import time
# session = get_session()

app = Flask(__name__)
CORS(app)

def time_since(since):
    now = time.time()
    s = now - since
    m = s // 60
    s -= m * 60
    return f'{int(m)}m {int(s)}s'

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
        # print(results_data)
        return jsonify(results_data)  # Return the dict with results and last_entry_id
    finally:
        session.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
