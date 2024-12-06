from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.util import PopulateDict

Base = declarative_base()

##### Sutian Database Structure #####

# Hanzi characters in 名.jsonl have the following fields:
# 漢字 (hant), 羅馬字 （romanization), 建議順序 (suggested_order), 類型 (type)
class SutianCharacter(Base):
    __tablename__ = 'sutian_characters'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    hant = Column('hant', String)
    romanization = Column('romanization', String)
    suggested_order = Column('suggested_order', Integer)
    type = Column('type', String)

    def __repr__(self):
        return f"<SutianCharacter(hant='{self.hant}', romanization='{self.romanization}', suggested_order={self.suggested_order}, type='{self.type}')>"

    def to_dict(self):
        character_dict = {
            'id': self.id,
            'hant': self.hant,
            'romanization': self.romanization,
            'suggested_order': self.suggested_order,
            'type': self.type
        }
        return character_dict

# Lemmas in 詞目.jsonl have the following fields:
# 詞目id (lemma_id), 漢字 (hant), 羅馬字 (romanization), 分類 (classification), 羅馬字音檔檔名 (audio)
class SutianLemma(Base):
    __tablename__ = 'sutian_lemma'
    id = Column('id', Integer, primary_key=True)
    hant = Column('hant', String)
    romanization = Column('romanization', String)
    classification = Column('classification', String)
    audio = Column('audio', String)
    senses = relationship('SutianSense', back_populates='lemma')
    variant_writings = relationship('SutianVariantWriting', back_populates='lemma')
    common_variant_pronunciations = relationship('SutianCommonVariantPronunciation', back_populates='lemma')
    other_variant_pronunciations = relationship('SutianOtherVariantPronunciation', back_populates='lemma')
    wiktionary_entries = relationship('WiktionaryEntry', back_populates='sutian_lemma')

    def __repr__(self):
        return f"<SutianLemma(hant='{self.hant}', romanization='{self.romanization}', classification='{self.classification}')>"

    def to_dict(self):
        lemma_dict = {
            'id': self.id,
            'hant': self.hant,
            'romanization': self.romanization,
            'classification': self.classification,
            'audio': self.audio,
            'senses': [],
            'variant_writings': [],
            'common_variant_pronunciations': [],
            'other_variant_pronunciations': [],
        }
        if self.senses:
            lemma_dict['senses'] = [sense.to_dict() for sense in self.senses]
        if self.variant_writings:
            lemma_dict['variant_writings'] = [v.variant for v in self.variant_writings]
        if self.common_variant_pronunciations:
            lemma_dict['common_variant_pronunciations'] = [v.romanization for v in self.common_variant_pronunciations]
        if self.other_variant_pronunciations:
            lemma_dict['other_variant_pronunciations'] = [v.romanization for v in self.other_variant_pronunciations]
        return lemma_dict

    def sense_dicts(self):
        return [sense.to_dict() for sense in self.senses]

# Senses in 義項.jsonl have the following fields:
# 義項id (sense_id), 詞目id (lemma_id), 詞性 (lexical_category), 解說 (explanation)
class SutianSense(Base):
    __tablename__ = 'sutian_sense'
    id = Column('id', Integer, primary_key=True)
    lemma_id = Column('lemma_id', Integer, ForeignKey('sutian_lemma.id'))
    lexical_category = Column('lexical_category', String)
    explanation = Column('explanation', String)
    lemma = relationship('SutianLemma', back_populates='senses')

    def __repr__(self):
        return f"<SutianSense(lemma='{self.lemma.hant}', lexical_category='{self.lexical_category}', explanation='{self.explanation}')>"

    def to_dict(self):
        sense_dict = {
            'id': self.id,
            'lemma_id': self.lemma_id,
            'lexical_category': self.lexical_category,
            'explanation': self.explanation
        }
        return sense_dict

# Variant writings in 異用字.jsonl have the following fields:
# 詞目id (lemma_id), 漢字 (hant), 異用字 (variant)
class SutianVariantWriting(Base):
    __tablename__ = 'sutian_variant_writings'
    # Add primary key column
    id = Column('id', Integer, primary_key=True)
    lemma_id = Column('lemma_id', Integer, ForeignKey('sutian_lemma.id'))
    hant = Column('hant', String)
    variant = Column('variant', String)
    lemma = relationship('SutianLemma', back_populates='variant_writings')

# Common variant pronunciations in 俗唸作.jsonl have the following fields:
# 詞目id (lemma_id), 漢字 (hant), 羅馬字 (romanization)
class SutianCommonVariantPronunciation(Base):
    __tablename__ = 'sutian_common_variant_pronunciations'
    id = Column('id', Integer, primary_key=True)
    lemma_id = Column('lemma_id', Integer, ForeignKey('sutian_lemma.id'))
    hant = Column('hant', String)
    romanization = Column('romanization', String)
    lemma = relationship('SutianLemma', back_populates='common_variant_pronunciations')

# Other variant pronunciations in 又唸作.jsonl have the following fields:
# 詞目id (lemma_id), 漢字 (hant), 羅馬字 (romanization)
class SutianOtherVariantPronunciation(Base):
    __tablename__ = 'sutian_other_variant_pronunciations'
    id = Column('id', Integer, primary_key=True)
    lemma_id = Column('lemma_id', Integer, ForeignKey('sutian_lemma.id'))
    hant = Column('hant', String)
    romanization = Column('romanization', String)
    lemma = relationship('SutianLemma', back_populates='other_variant_pronunciations')



##### Wiktionary Database Structure #####
# TODO: General problem: wiktextract removes to much data for pronunciation and glosses,
#  especially when dealing with Chinese dialects.

class WiktionaryEntry(Base):
    __tablename__ = 'wiktionary_entries'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    word = Column('word', String)
    pos = Column('pos', String)
    syllable_count = Column('syllable_count', Integer)
    pronunciations = relationship('WiktionaryPronunciation', back_populates='entry')
    glosses = Column('glosses', String)
    raw_glosses = Column('raw_glosses', String)
    etymology = Column('etymology', String)
    sutian_lemma_id = Column('sutian_lemma_id', Integer, ForeignKey('sutian_lemma.id'))
    sutian_lemma = relationship('SutianLemma', back_populates='wiktionary_entries')

    def __repr__(self):
        return f"<WiktionaryEntry(word='{self.word}', pos='{self.pos}', syllable_count={self.syllable_count})>"

    def to_dict(self):
        entry_dict = {
            'id': self.id,
            'word': self.word,
            'pos': self.pos,
            'syllable_count': self.syllable_count,
            'pronunciations': {},
            'glosses': self.glosses.split('\n'),
            'raw_glosses': self.raw_glosses.split('\n'),
            'etymology': self.etymology,
            'sutian_lemma': None
        }
        for pronunciation in self.pronunciations:
            if pronunciation.language.language not in entry_dict['pronunciations']:
                entry_dict['pronunciations'][pronunciation.language.language] = []
            entry_dict['pronunciations'][pronunciation.language.language].append(pronunciation.pronunciation)
        if self.sutian_lemma:
            entry_dict['sutian_lemma'] = self.sutian_lemma.to_dict()
        return entry_dict
        # pronunciations = {}
        # for pronunciation in self.pronunciations:
        #     if pronunciation.language.language not in pronunciations:
        #         pronunciations[pronunciation.language.language] = []
        #     pronunciations[pronunciation.language.language].append(pronunciation.pronunciation)
        # lemma_dict = None
        # if self.sutian_lemma:
        #     lemma_dict = self.sutian_lemma.to_dict()
        #     if self.sutian_lemma.senses:
        #         lemma_dict['senses'] = [sense.to_dict() for sense in self.sutian_lemma.senses]
        # return {'word': self.word, 'pos': self.pos, 'syllable_count': self.syllable_count,
        #         'pronunciations': pronunciations, 'glosses': self.glosses, 'raw_glosses': self.raw_glosses,
        #         'etymology': self.etymology, 'sutian_lemma': lemma_dict}

class WiktionaryPronunciation(Base):
    # Here, we handle the different pronunciations of a word
    __tablename__ = 'wiktionary_pronunciations'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    entry_id = Column('entry_id', Integer, ForeignKey('wiktionary_entries.id'))
    language_id = Column('language_id', Integer, ForeignKey('wiktionary_languages.id'))
    pronunciation = Column('pronunciation', String)
    normalized_pronunciation = Column('normalized_pronunciation', String)
    entry = relationship('WiktionaryEntry', back_populates='pronunciations')
    language = relationship('WiktionaryLanguage', back_populates='pronunciations')

    def __repr__(self):
        return f"<WiktionaryPronunciation(pronunciation='{self.pronunciation}', language={self.language.language}, entry={self.entry.word}')>"

class WiktionaryLanguage(Base):
    __tablename__ = 'wiktionary_languages'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    language = Column('language', String)
    pronunciations = relationship('WiktionaryPronunciation', back_populates='language')
