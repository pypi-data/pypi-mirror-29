#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Python Word Sense Disambiguation (pyWSD)
#
# Copyright (C) 2014-2018 alvations
# URL:
# For license information, see LICENSE.md

import string
import pickle
from itertools import chain

from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag

from pywsd.cosine import cosine_similarity as cos_sim
from pywsd.utils import lemmatize, porter, lemmatize_sentence, synset_properties

pywsd_stopwords = [u"'s", u"``", u"`"]
EN_STOPWORDS = set(stopwords.words('english') + list(string.punctuation) + pywsd_stopwords)


def synset_signatures(ss, hyperhypo=True, adapted=False,
                      remove_stopwords=True, to_lemmatize=True, remove_numbers=True,
                      lowercase=True, original_lesk=False):
    """
    :param ss: A WordNet synset.
    :type ss: nltk.corpus.wordnet.Synset
    """
    # Collects the signatures from WordNet.
    signature = []
    # Adds the definition, example sentences and lemma_names.
    signature += word_tokenize(ss.definition())
    # If the original lesk signature is requested, skip the other signatures.
    if original_lesk:
        synsets_signatures[ss] = signature
        return set(signature)
    # Adds the examples and lemma names.
    signature += chain(*[word_tokenize(eg) for eg in ss.examples()])
    signature += ss.lemma_names()

    # Includes lemma_names of hyper-/hyponyms.
    if hyperhypo:
        hyperhyponyms = set(ss.hyponyms() + ss.hypernyms() + ss.instance_hyponyms() + ss.instance_hypernyms())
        signature += set(chain(*[i.lemma_names() for i in hyperhyponyms]))

    # Includes signatures from related senses as in Adapted Lesk.
    if adapted:
        # Includes lemma_names from holonyms, meronyms and similar_tos
        related_senses = set(ss.member_holonyms() + ss.part_holonyms() + ss.substance_holonyms() + \
                             ss.member_meronyms() + ss.part_meronyms() + ss.substance_meronyms() + \
                             ss.similar_tos())
        signature += set(chain(*[i.lemma_names() for i in related_senses]))

    # Lowercase.
    signature = set(s.lower() for s in signature) if lowercase else signature
    # Removes stopwords.
    signature = set(signature).difference(EN_STOPWORDS) if remove_stopwords else signature

    # Lemmatized context is preferred over stemmed context.
    if to_lemmatize:
        signature = [lemmatize(s) if lowercase else lemmatize(s) # Lowercasing checks here.
                     for s in signature
                     # We only throw away if both remove_numbers and s is a digit are true.
                     if not (remove_numbers and s.isdigit())
                     ]
    # Keep only the unique bag-of-words
    return signature


def signatures(ambiguous_word, pos=None, hyperhypo=True, adapted=False,
               remove_stopwords=True, to_lemmatize=True, remove_numbers=True,
               lowercase=True, to_stem=False, original_lesk=False):
    """
    :param ambiguous_word: The ambiguous word.
    :type ambiguous_word: str
    """
    # Ensure that the POS is supported.
    pos = pos if pos in ['a', 'r', 's', 'n', 'v', None] else None
    # Holds the synset->signature dictionary.
    ss_sign = {}
    for ss in wn.synsets(ambiguous_word, pos):
        ss_sign[ss] = synset_signatures(ss, hyperhypo=True, adapted=False,
                                        remove_stopwords=True, to_lemmatize=True,
                                        remove_numbers=True, lowercase=True,
                                        original_lesk=False)

    # Matching exact words may cause sparsity, so optional matching for stems.
    # Not advisible to use thus left out of the synsets_signatures()
    if to_stem == True:
        ss_sign = {ss:[porter.stem(s) for s in signature]
                   for ss, signature in ss_sign.items()}
    return ss_sign


def compare_overlaps_greedy(context, synsets_signatures):
    """
    Calculate overlaps between the context sentence and the synset_signatures
    and returns the synset with the highest overlap.

    Note: Greedy algorithm only keeps the best sense,
    see https://en.wikipedia.org/wiki/Greedy_algorithm

    Only used by original_lesk(). Keeping greedy algorithm for documentary sake,
    because original_lesks is greedy.
    """
    max_overlaps = 0; lesk_sense = None
    for ss in synsets_signatures:
        overlaps = set(synsets_signatures[ss]).intersection(context)
        if len(overlaps) > max_overlaps:
            lesk_sense = ss
            max_overlaps = len(overlaps)
    return lesk_sense


def compare_overlaps(context, synsets_signatures, \
                     nbest=False, keepscore=False, normalizescore=False):
    """
    Calculates overlaps between the context sentence and the synset_signture
    and returns a ranked list of synsets from highest overlap to lowest.
    """
    overlaplen_synsets = [] # a tuple of (len(overlap), synset).
    for ss in synsets_signatures:
        overlaps = set(synsets_signatures[ss]).intersection(context)
        overlaplen_synsets.append((len(overlaps), ss))

    # Rank synsets from highest to lowest overlap.
    ranked_synsets = sorted(overlaplen_synsets, reverse=True)

    # Normalize scores such that it's between 0 to 1.
    if normalizescore:
        total = float(sum(i[0] for i in ranked_synsets))
        ranked_synsets = [(i/total,j) for i,j in ranked_synsets]

    if not keepscore: # Returns a list of ranked synsets without scores
        ranked_synsets = [i[1] for i in sorted(overlaplen_synsets, \
                                               reverse=True)]

    # Returns a ranked list of synsets otherwise only the best sense.
    return ranked_synsets if nbest else ranked_synsets[0]


def original_lesk(context_sentence, ambiguous_word, dictionary=None):
    """
    This function is the implementation of the original Lesk algorithm (1986).
    It requires a dictionary which contains the definition of the different
    sense of each word. See http://dl.acm.org/citation.cfm?id=318728
    """
    ambiguous_word = lemmatize(ambiguous_word)
    if not dictionary: # If dictionary is not provided, use the WN defintion.
        dictionary = signatures(ambiguous_word, original_lesk=True)
    best_sense = compare_overlaps_greedy(context_sentence.split(), dictionary)
    return best_sense


def simple_signatures(ambiguous_word, pos=None, lemma=True, stem=False, \
                     hyperhypo=True, stop=True):
    """
    Returns a synsets_signatures dictionary that includes signature words of a
    sense from its:
    (i)   definition
    (ii)  example sentences
    (iii) hypernyms and hyponyms
    """
    synsets_signatures = signatures(ambiguous_word, pos=pos, hyperhypo=hyperhypo,
                            remove_stopwords=stop, to_lemmatize=lemma,
                            remove_numbers=True, lowercase=True, to_stem=stem)
    return synsets_signatures

def simple_lesk(context_sentence, ambiguous_word, \
                pos=None, lemma=True, stem=False, hyperhypo=True, \
                stop=True, context_is_lemmatized=False, \
                nbest=False, keepscore=False, normalizescore=False):
    """
    Simple Lesk is somewhere in between using more than the
    original Lesk algorithm (1986) and using less signature
    words than adapted Lesk (Banerjee and Pederson, 2002)
    """
    # Ensure that ambiguous word is a lemma.
    ambiguous_word = lemmatize(ambiguous_word, pos=pos)
    # If ambiguous word not in WordNet return None
    if not wn.synsets(ambiguous_word):
        return None
    # Get the signatures for each synset.
    ss_sign = simple_signatures(ambiguous_word, pos, lemma, stem, hyperhypo, stop)
    # Disambiguate the sense in context.
    context_sentence = context_sentence.split() if context_is_lemmatized else lemmatize_sentence(context_sentence)
    return compare_overlaps(context_sentence, ss_sign, nbest=nbest,
                            keepscore=keepscore, normalizescore=normalizescore)


def adapted_lesk(context_sentence, ambiguous_word, \
                pos=None, lemma=True, stem=False, hyperhypo=True, \
                stop=True, context_is_lemmatized=False, \
                nbest=False, keepscore=False, normalizescore=False):
    """
    This function is the implementation of the Adapted Lesk algorithm,
    described in Banerjee and Pederson (2002). It makes use of the lexical
    items from semantically related senses within the wordnet
    hierarchies and to generate more lexical items for each sense.
    see www.d.umn.edu/~tpederse/Pubs/cicling2002-b.pdf‎
    """
    # Ensure that ambiguous word is a lemma.
    ambiguous_word = lemmatize(ambiguous_word)
    # If ambiguous word not in WordNet return None
    if not wn.synsets(ambiguous_word):
        return None
    # Get the signatures for each synset.
    ss_sign = signatures(ambiguous_word, pos=pos, hyperhypo=hyperhypo, adapted=True,
                            remove_stopwords=stop, to_lemmatize=lemma,
                            remove_numbers=True, lowercase=True, to_stem=stem)

    # Disambiguate the sense in context.
    context_sentence = context_sentence.split() if context_is_lemmatized else lemmatize_sentence(context_sentence)
    return compare_overlaps(context_sentence, ss_sign, nbest=nbest,
                            keepscore=keepscore, normalizescore=normalizescore)


def cosine_lesk(context_sentence, ambiguous_word, \
                pos=None, lemma=True, stem=True, hyperhypo=True, \
                stop=True, context_is_lemmatized=False, \
                nbest=False):
    """
    In line with vector space models, we can use cosine to calculate overlaps
    instead of using raw overlap counts. Essentially, the idea of using
    signatures (aka 'sense paraphrases') is lesk-like.
    """
    # Ensure that ambiguous word is a lemma.
    ambiguous_word = lemmatize(ambiguous_word)
    # If ambiguous word not in WordNet return None
    if not wn.synsets(ambiguous_word):
        return None
    ss_sign = simple_signatures(ambiguous_word, pos, lemma, stem, hyperhypo, stop)
    if context_is_lemmatized:
        context_sentence = " ".join(context_sentence.split())
    else:
        context_sentence = " ".join(lemmatize_sentence(context_sentence))

    scores = []
    for ss, signature in ss_sign.items():
        # Lowercase and replace "_" with spaces.
        signature = " ".join(map(str, signature)).lower().replace("_", " ")
        scores.append((cos_sim(context_sentence, signature), ss))

    scores = sorted(scores, reverse=True)
    return scores if nbest else scores[0][1]
