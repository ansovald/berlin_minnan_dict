from database_structure import (Base, SutianCharacter, SutianLemma, SutianSense, SutianVariantWriting,
                                SutianCommonVariantPronunciation, SutianOtherVariantPronunciation,
                                WiktionaryEntry, WiktionaryPronunciation, WiktionaryLanguage)

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from regex_search_patterns import build_search_pattern
from database_util import strip_hokkien_pronunciation, map_stripped_to_normalized
import unicodedata

import re
from sqlalchemy import event


def start_engine(database_file='data/hokkien.db'):
    engine = create_engine(f'sqlite:///{database_file}')
    print(f"Connecting to database: {database_file}")

    # Function for SQLite regex matching
    def sqlite_regex(expr, item):
        return re.search(expr, item) is not None
    # Register the function with SQLite
    @event.listens_for(engine, "connect")
    def sqlite_regex_connect(dbapi_connection, connection_record):
        dbapi_connection.create_function("REGEXP", 2, sqlite_regex)

    return engine

def get_session(session=None):
    if session:
        return session
    engine = start_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def get_wiktionary_entry(entry_id=None, session=None):
    if not entry_id:
        print("Please provide an entry_id to search for")
        return None
    session = get_session(session=session)
    query = select(WiktionaryEntry).where(WiktionaryEntry.id.op('=')(entry_id))
    entry = session.execute(query).scalars().first()
    if entry:
        # print(entry.to_dict())
        return entry.to_dict()
    else:
        print(f"No entry found with id {entry_id}")
        return None

def get_sutian_lemma(lemma_id=None, session=None):
    if not lemma_id:
        print("Please provide a lemma_id to search for")
        return None
    session = get_session(session=session)
    query = select(SutianLemma).where(SutianLemma.id.op('=')(lemma_id))
    lemma = session.execute(query).scalars().first()
    if lemma:
        # print(lemma.to_dict())
        return lemma.to_dict()
    else:
        print(f"No lemma found with id {lemma_id}")
        return None

def query_wiktionary_entries(hokkien=None, english=None, hanzi=None, syllable_count=None, session=None, case_sensitive_en=False, case_sensitive_nan=False, last_entry_id=None, page_size=20, verbose=False):
    print(f"Querying Wiktionary entries. hokkien='{hokkien}', english='{english}', hanzi='{hanzi}', syllable_count='{syllable_count}'")
    if last_entry_id:
        print(f"Last entry id: {last_entry_id}")
    session = get_session(session=session)
    if syllable_count:
        if not hokkien and not english and not hanzi:
            print("Please provide a search term for hokkien, english, or hanzi")
            return []
    # TODO: expand later for hanzi only search?
    # if hanzi and hanzi.startswith('@'):
    #         query_hanzi(hanzi[1:])

    # Base query
    query = select(WiktionaryEntry)

    search_patterns = {}

    # Apply filters
    if english:
        op, english = build_search_pattern(english, gloss_search=True, case_sensitive=case_sensitive_en)
        search_patterns['english'] = english.replace('(?i)', '')
        # Find the english query either in the glosses or the raw_glosses, or both
        query = query.where(WiktionaryEntry.glosses.op(op)(english))
        print(f"Searching for English glosses: {english}, operator: {op}")
    if hokkien:
        op, hokkien = build_search_pattern(hokkien, case_sensitive=case_sensitive_nan)
        search_patterns['hokkien'] = hokkien.replace('(?i)', '')
        # `normalized_pronunciation` here means: accents and other tone marks are removed. Currently, it searches all
        # pronunciations (Mandarin, Hokkien-TL, Hokkien-POJ) TODO: make it smarter
        query = query.where(
            WiktionaryEntry.pronunciations.any(
                            WiktionaryPronunciation.normalized_pronunciation.op(op)(hokkien)
            ), WiktionaryPronunciation.language.has(WiktionaryLanguage.language == 'Hokkien-TL'))
        print(f"Searching for Hokkien pronunciation: {hokkien}, operator: {op}")
    if hanzi:
        op, hanzi = build_search_pattern(hanzi)
        search_patterns['hanzi'] = hanzi
        query = query.where(WiktionaryEntry.word.op(op)(hanzi))
    if syllable_count and syllable_count != 0:
        if type(syllable_count) == str:
            syllable_count = int(syllable_count)
        query = query.where(WiktionaryEntry.syllable_count.op('=')(syllable_count))
    
    # Apply cursor-based pagination
    if last_entry_id:
        query = query.where(WiktionaryEntry.id > last_entry_id)
    
    # Apply ordering and limit
    query = query.order_by(WiktionaryEntry.id).limit(page_size)

    # print(f"Executing query: {query}")

    words = session.execute(query).scalars().all()
    if verbose:
        print(f"Found {len(words)} words matching the search criteria")
    results = []
    last_entry_id = None
    if words:
        for word in words:
            lemma = word.word
            if 'hanzi' in search_patterns:
                # Enclose the matched term in `***`
                lemma = re.sub(f'({search_patterns['hanzi']})', '***\g<1>***', word.word)
            wiktionary_entry = word.to_dict()
            if 'hokkien' in search_patterns and 'pronunciations' in wiktionary_entry:
                if 'Hokkien-TL' in wiktionary_entry['pronunciations']:
                    for i, pronunciation in enumerate(wiktionary_entry['pronunciations']['Hokkien-TL']):
                        print()
                        stripped = strip_hokkien_pronunciation(pronunciation)
                        normalized = unicodedata.normalize('NFD', pronunciation)
                        mapping = map_stripped_to_normalized(stripped, normalized)
                        # find first and last index of match `search_pattern['hokkien']` in `stripped`
                        if not case_sensitive_nan:
                            match = re.search(search_patterns['hokkien'], stripped, flags=re.IGNORECASE)
                        else:
                            match = re.search(search_patterns['hokkien'], stripped)
                        if match:
                            # Add `***` before the first index in `normalized`, using the mapping
                            start_index = mapping[match.start()]
                            end_index = mapping[match.end() - 1] + 1
                            normalized = normalized[:start_index] + f'***{normalized[start_index:end_index]}***' + normalized[end_index:]
                        pronunciation = unicodedata.normalize('NFC', normalized)
                        wiktionary_entry['pronunciations']['Hokkien-TL'][i] = pronunciation
            if 'english' in search_patterns and 'glosses' in wiktionary_entry:
                for i, gloss in enumerate(wiktionary_entry['glosses']):
                    print(f'search_patterns[english]: {search_patterns["english"]}')
                    if not case_sensitive_en:
                        match = re.search(search_patterns['english'], gloss, flags=re.IGNORECASE)
                    else:
                        match = re.search(search_patterns['english'], gloss)
                    print(f'gloss: {gloss}, match: {match}')
                    if match:
                        # Add `***` before the first index in `gloss`
                        start_index = match.start()
                        end_index = match.end()
                        gloss = gloss[:start_index] + f'***{gloss[start_index:end_index]}***' + gloss[end_index:]
                        wiktionary_entry['glosses'][i] = gloss
            hit_dict = { 'lemma': lemma, 'wiktionary_entry': wiktionary_entry }
            if word.sutian_lemma:
                hit_dict['sutian_lemma'] = word.sutian_lemma.to_dict()
            results.append(hit_dict)
        if len(words) == page_size:
            last_entry_id = words[-1].id
        else:
            last_entry_id = None

    return {
        'results': results,
        'last_entry_id': last_entry_id,
        'search_patterns': search_patterns
    }

def query_sutian_lemma(lemma_search, session=None):
    session = get_session(session)
    op, lemma_search = build_search_pattern(lemma_search)
    query = select(SutianLemma).where(SutianLemma.hant.op(op)(lemma_search))
    lemmata = session.execute(query).scalars().all()
    findings = []
    # print(f"Found {len(lemmata)} lemma matching the search criteria")
    if lemmata:
        for lemma in lemmata:
            # sense_dicts = lemma.sense_dicts()
            # for sense_dict in sense_dicts:
                # print(sense_dict)
            findings.append(lemma.sense_dicts())
    return findings


def query_hanzi(hanzi_search, session=None):
    if len(hanzi_search) != 1:
        print("Please provide only one hanzi character for the search")
        return
    session = get_session(session)
    print(f"Searching for hanzi: {hanzi_search}")
    query = select(SutianCharacter).where(SutianCharacter.hant.op('=')(hanzi_search))
    characters = session.execute(query).scalars().all()
    findings = []
    if characters:
        for character in characters:
            print(character.to_dict())
            findings.append(character.to_dict())
    # # Search Wiktionary entries where word is the hanzi_search and pos is 'character'
    # query = select(WiktionaryEntry).where(WiktionaryEntry.word == hanzi_search, WiktionaryEntry.pos == 'character')
    # words = session.execute(query).scalars().all()
    # if words:
    #     for word in words:
    #         print(word.to_dict())
    #         findings.append(word.to_dict())
    return findings

def query_english_glosses(english_search, engine=None, session=None):
    session = get_session(session)
    english_search = build_search_pattern(english_search)
    print(f"Searching for English glosses: {english_search}")
    query = select(WiktionaryEntry).where(WiktionaryEntry.glosses.op('REGEXP')(english_search))
    words = session.execute(query).scalars().all()
    if words:
        findings = []
        for word in words:
            findings.append(word.to_dict())
        for f in findings:
            print(f)
        return findings

def query_hokkien_pronunciation(hokkien_search, engine=None, session=None):
    session = get_session(session)
    hokkien_search = build_search_pattern(hokkien_search)
    print(f"Searching for Hokkien pronunciation: {hokkien_search}")
    # Search for pronunciations where language is Hokkien, and pronunciation matches the search term
    query = select(WiktionaryPronunciation).where(WiktionaryPronunciation.normalized_pronunciation.op('REGEXP')(hokkien_search)).join(WiktionaryPronunciation.language).filter(WiktionaryLanguage.language == 'Hokkien-TL')
    pronunciations = session.execute(query).scalars().all()
    findings = []
    if pronunciations:
        for pronunciation in pronunciations:
            findings.append(pronunciation.entry.to_dict())
        for f in findings:
            print(f)
        return findings

def query_hokkien_lemma(search_lemma='哭爸', session=None):
    session = get_session(session)
    if len(search_lemma) == 1:
        # Search the character table
        characters = session.query(SutianCharacter).filter(SutianCharacter.hant == search_lemma)
        if characters:
            for character in characters:
                print(f"Found character: {character.hant}, romanization: {character.romanization}, suggested order: {character.suggested_order}, type: {character.type}")
    lemmata = session.query(SutianLemma).filter(SutianLemma.hant == search_lemma)
    if lemmata:
        for lemma in lemmata:
            print(f"Found lemma: {lemma.hant}, romanization: {lemma.romanization}, classification: {lemma.classification} in sutian database")
            for sense in lemma.senses:
                print(f"\tlexical category: {sense.lexical_category}, explanation: {sense.explanation}")
            for variant_writing in lemma.variant_writings:
                print(f"\tVariant Writing: {variant_writing.variant}")
            for common_variant_pronunciation in lemma.common_variant_pronunciations:
                print(f"\tCommon Variant Pronunciation: {common_variant_pronunciation.romanization}")
            for other_variant_pronunciation in lemma.other_variant_pronunciations:
                print(f"\tOther Variant Pronunciation: {other_variant_pronunciation.romanization}")
    else:
        print(f"Lemma {search_lemma} not found in sutian database")
    words = session.query(WiktionaryEntry).filter(WiktionaryEntry.word == search_lemma)
    if words:
        for word in words:
            print(f"Found word {word.word}, pos: {word.pos} in Wiktionary database")
            pronunciations = {}
            for pronunciation in word.pronunciations:
                if pronunciation.language.language not in pronunciations:
                    pronunciations[pronunciation.language.language] = [pronunciation.pronunciation]
                else:
                    pronunciations[pronunciation.language.language].append(pronunciation.pronunciation)
            for key in pronunciations:
                print(f"\t{key}: {', '.join(pronunciations[key])}")
            print(f"\tglosses:\n\t\t{'\n\t\t'.join(word.glosses.split('\n'))}")
