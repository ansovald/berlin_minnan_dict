from database_structure import SutianCharacter, SutianLemma
from query_database import get_session
import unicodedata
import json
import argparse

def lookup_sutian_lemma(hanzi, session=None):
    session = get_session(session=session)
    query = session.query(SutianLemma).filter(SutianLemma.hant == hanzi)
    return [lemma.romanization for lemma in query.all()]
    
def romanize_hokkien_char(hanzi, session=None):
    session = get_session(session=session)
    print(f"Looking up character '{hanzi}'")
    query = session.query(SutianCharacter).filter(SutianCharacter.hant == hanzi)
    # there might be several romanizations, so return a list of all of them
    characters = query.all()
    romanizations = []
    if characters:
        for char in characters:
            romanizations.append({
                'romanization': char.romanization,
                'type': char.type,
            })
        # romanizations = [char.romanization for char in characters]
        # print(f"Found character(s) for '{hanzi}': {', '.join(romanizations)}")
        return romanizations
    else:
        # print(f"No character found for '{hanzi}'")
        return [{
            'romanization': hanzi,
            'type': None
        }]

def romanize_hokkien(hanzi, session=None):
    print(f"romanize_hokkien called with '{hanzi}'")
    session = get_session(session=session)
    romanization_dict = {}
    covered_end_idx = None
    # first, try to find a lemma for the entire string. If that fails, try one char less, and so on until we find a match or run out of characters
    for i in range(len(hanzi), 0, -1):
        substring = hanzi[:i]
        if len(substring) == 1:
            romanization = romanize_hokkien_char(substring, session=session)
        else:
            romanization = lookup_sutian_lemma(substring, session=session)
        if romanization:
            romanization_dict[substring] = romanization
            print(f"Matched '{substring}' to '{romanization}'")
            covered_end_idx = i
            break
    if covered_end_idx is None:
        # try to match the first character
        print(f"\tNo romanization found for any substring starting from '{hanzi[0]}', trying to match first character '{hanzi[0]}'")
        romanization = romanize_hokkien_char(hanzi[0], session=session)
        romanization_dict[hanzi[0]] = romanization
        print(f"Matched '{hanzi[0]}' to '{', '.join(romanization)}'")
        covered_end_idx = 1
    if covered_end_idx < len(hanzi):
        print(f"Remaining string after matching '{hanzi[:covered_end_idx]}': '{hanzi[covered_end_idx:]}'")
        sub_rom_dict = romanize_hokkien(hanzi[covered_end_idx:], session=session)
        romanization_dict.update(sub_rom_dict)
    return romanization_dict

tone_markers = {
    '́': '2',
    '̀': '3',
    '̂': '5',
    '̌': '6',
    '̄': '7',
    '̍': '8'
}

dark_entering_offsets = ['p', 't', 'k', 'h']

def normalize_romanization(romanization: str):
    # apply canonical decomposition (NFD) to the romanization
    normalized = unicodedata.normalize('NFD', romanization)
    if normalized[-1] in dark_entering_offsets:
        return normalized
    # replace tone markers with numbers
    for marker, number in tone_markers.items():
        normalized = normalized.replace(marker, number)
        if marker in romanization:
            marker_found = True
    return normalized

def suggest_romanization(romanization_dict, favored_types=['白', '不標'], normalize=True):
    suggestion = []
    for hanzi, romanizations in romanization_dict.items():
        if len(romanizations) == 1:
            rom = romanizations[0]['romanization']
            if normalize:
                rom = normalize_romanization(rom)
            suggestion.append(rom)
        else:
            for romanization_info in romanizations:
                if romanization_info['type'] in favored_types:
                    rom = romanization_info['romanization']
                    if normalize:
                        rom = normalize_romanization(rom)
                    suggestion.append(rom)
                    break
    return ' '.join(suggestion)

if __name__ == "__main__":

    # add argparser to allow user to input hanzi string
    parser = argparse.ArgumentParser(description='Romanize a Hokkien string using the Sutian database.')
    parser.add_argument('hanzi', type=str, help='The Hokkien string to romanize')
    args = parser.parse_args()
    if not args.hanzi:
        print("Please provide a Hokkien string to romanize.")
        exit(1)

    rom_dict = romanize_hokkien(args.hanzi)
    print(json.dumps(rom_dict, ensure_ascii=False, indent=2))
    print(suggest_romanization(rom_dict))