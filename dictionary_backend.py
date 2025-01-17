from flask import Flask, jsonify, request #, api_session
from flask_cors import CORS
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
    hokkien = params.get('hokkien')
    english = params.get('english')
    hanzi = params.get('hanzi')
    syllable_count = params.get('syllable_count')

    # Ensure a session is created
    session = get_session()
    try:
        if not any([hokkien, english, hanzi, syllable_count]):
            return jsonify({"error": "No valid search parameters provided"}), 400

        import time
        start = time.time()
        results = query_wiktionary_entries(
            hokkien=hokkien,
            english=english,
            hanzi=hanzi,
            syllable_count=syllable_count,
            session=session
        )
        print(f"Found {len(results)} entries matching the search criteria, took {time_since(start)}")
        return jsonify(results)
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
