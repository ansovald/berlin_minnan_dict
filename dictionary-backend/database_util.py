import unicodedata

def strip_hokkien_pronunciation(pronunciation):
    # strips hokkien pronunciation of all tone marks
    # Performs a NFD normalization, then removes all characters that are not letters or hyphens
    return ''.join([c for c in unicodedata.normalize('NFD', pronunciation) if c.isalpha() or c == '-'])

def map_stripped_to_normalized(stripped, normalized):
    # Create a mapping of the position of each character to its original character
    mapping = {}
    norm_counter = 0
    for i, c in enumerate(stripped):
        while norm_counter < len(normalized) and normalized[norm_counter] != c:
            norm_counter += 1
        if norm_counter < len(normalized):
            mapping[i] = norm_counter
            norm_counter += 1
    return mapping
