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

import collections

from worker.items import HomeAd

try:
    # Import NLTK if it is installed
    import nltk

    # This imports NLTK's implementation of the Snowball
    # stemmer algorithm
    from nltk.stem.snowball import SnowballStemmer
    from nltk.util import ngrams

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

italian_stop_words = stopwords.words('italian')
stemmer_it = SnowballStemmer('italian')


def get_bigrams(tokens):
    return [bigram for bigram in nltk.bigrams(tokens)]


def get_trigrams(tokens):
    return [trigram for trigram in nltk.trigrams(tokens)]


def get_tokens(text, language='italian'):
    tokens = word_tokenize(text, language=language)
    return tokens


def get_stems(tokens):
    stems = [stemmer_it.stem(item) for item in tokens]
    return stems


def remove_stop_words(tokens):
    new_list = [token for token in tokens if token not in italian_stop_words]
    return new_list


def get_tags(text, language='italian'):
    tokens = get_tokens(text, language)
    cleaned_tokens = remove_stop_words(tokens)
    return cleaned_tokens


def get_tags_from_item(item):
    tokenized_item = {}
    item_token_list = []

    tokenized_description = get_tokens(item['description'])
    # tokenized_description_bigrams = get_bigrams(tokenized_description)
    # tokenized_description_trigrams = get_trigrams(tokenized_description)

    item_token_list = remove_stop_words(tokenized_description)
    item_token_list_bigrams = get_bigrams(item_token_list)
    item_token_list_trigrams = get_trigrams(item_token_list)

    return {
        'tokens': item_token_list,
        'bigrams': item_token_list_bigrams,
        'trigrams': item_token_list_trigrams,
    }


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
