### Imports
#
# Import some Python 3 features to use in Python 2
from __future__ import print_function
from __future__ import unicode_literals

# gives us access to command-line arguments
import sys

# The Counter collection is a convenient layer on top of
# python's standard dictionary type for counting iterables.
from collections import Counter

# The standard python regular expression module:
import re

try:
    # Import NLTK if it is installed
    import nltk

    # This imports NLTK's implementation of the Snowball
    # stemmer algorithm
    from nltk.stem.snowball import SnowballStemmer

    # NLTK's interface to the WordNet lemmatizer
    from nltk.stem.wordnet import WordNetLemmatizer
except ImportError:
    nltk = None
    print("NLTK is not installed, so we won't use it.")

try:
    # Import spaCy if it is installed
    import spacy
except ImportError:
    spacy = None
    print("spaCy is not installed, so we won't use it.")

try:
    # Import Pattern if it is installed
    from pattern.en import parse
except ImportError:
    parse = None
    print("Pattern is not installed, so we won't use it.")

from nltk.tokenize import word_tokenize


def tokenize(to_be_tokenized):
    return word_tokenize(to_be_tokenized)


def nltk_stem_hapaxes(tokens):
    """
    Takes a list of tokens and returns a list of the word
    stem hapaxes.
    """
    if not nltk:
        # Only run if NLTK is loaded
        return None

    # Apply NLTK's Snowball stemmer algorithm to tokens:
    stemmer = SnowballStemmer("italian")
    stems = [stemmer.stem(token) for token in tokens]

    # Filter down to hapaxes:
    counts = nltk.FreqDist(stems)
    hapaxes = counts.hapaxes()
    return hapaxes


def nltk_lemma_hapaxes(tokens):
    """
    Takes a list of tokens and returns a list of the lemma
    hapaxes.
    """
    if not nltk:
        # Only run if NLTK is loaded
        return None

    # Tag tokens with part-of-speech:
    tagged = nltk.pos_tag(tokens)

    # Convert our Treebank-style tags to WordNet-style tags.
    tagged = [(word, pt_to_wn(tag))
              for (word, tag) in tagged]

    # Lemmatize:
    lemmer = WordNetLemmatizer()
    lemmas = [lemmer.lemmatize(token, pos)
              for (token, pos) in tagged]

    return nltk_stem_hapaxes(lemmas)


def pt_to_wn(pos):
    """
    Takes a Penn Treebank tag and converts it to an
    appropriate WordNet equivalent for lemmatization.

    A list of Penn Treebank tags is available at:
    https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
    """

    from nltk.corpus.reader.wordnet import NOUN, VERB, ADJ, ADV

    pos = pos.lower()

    if pos.startswith('jj'):
        tag = ADJ
    elif pos == 'md':
        # Modal auxiliary verbs
        tag = VERB
    elif pos.startswith('rb'):
        tag = ADV
    elif pos.startswith('vb'):
        tag = VERB
    elif pos == 'wrb':
        # Wh-adverb (how, however, whence, whenever...)
        tag = ADV
    else:
        # default to NOUN
        # This is not strictly correct, but it is good
        # enough for lemmatization.
        tag = NOUN

    return tag


from nltk.corpus import stopwords


def get_tags(text):
    tokens = word_tokenize(text, language='italian')

    italian_stop_words = stopwords.words('italian')
    new_list = [token for token in tokens if token not in italian_stop_words]

    stemmer = SnowballStemmer("italian")
    stems = [stemmer.stem(item) for item in new_list]
    vip_stems = Counter(stems).most_common(5)
    vip_tokens = [token for token, value in Counter(new_list).most_common(5)]

    return tokens


#
# stopwords.fileids()
if __name__ == '__main__':
    source = """
    The Natural History Museum is in the bustling section of South Kensington, popular with both Londoners and tourists. The area was cordoned off Saturday by heavily armed police, according to video posted on social media. Helicopters buzzed overhead as ambulances rushed to the scene on Exhibition Road.
    """
    d = word_tokenize(source)
    print(d)
    f = nltk_stem_hapaxes(d)
    print(f)
    # res = Counter(d).most_common(3)
    # print(res)
    res = nltk_lemma_hapaxes(f)
    print(res)
