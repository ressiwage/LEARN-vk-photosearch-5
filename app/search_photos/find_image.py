from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from annoy import AnnoyIndex
from .db import *
import spacy, sys, os
import numpy as np

enum = enumerate
PATH = "app/search_photos/vectors/"
PATH_TO_IMGS = "app/search_photos/"

def __lemmatized_sentence(sentence, nlp):
    return " ".join([j.lemma_ for j in nlp(sentence) if j.pos_ != "PUNCT"])


def save():
    nlp = spacy.load("en_core_web_lg")
    vectorizer = CountVectorizer()
    records = get_descs()
    descs = [__lemmatized_sentence(i[1], nlp) for i in records]
    tk = vectorizer.fit_transform(descs)
    names = vectorizer.get_feature_names_out()
    vector_database = AnnoyIndex(tk.shape[1], "angular")
    for ind, i in enum(tk.toarray().tolist()):
        vector_database.add_item(ind, i)
    vector_database.build(-1)
    vector_database.save(PATH+"vectors.ann")
    with open(PATH+"features", "w+") as f:
        f.write("|".join(names))


def find(sentence, n):
    records = get_descs()
    with open(PATH+"features", "r") as f:
        col_words = f.readline().split("|")
    vector_database = AnnoyIndex(len(col_words), "angular")
    vector_database.load(PATH+"vectors.ann")
    nlp = spacy.load("en_core_web_lg")
    lemmatized = __lemmatized_sentence(sentence, nlp)
    vectorizer = CountVectorizer()
    vectorized = vectorizer.fit_transform([lemmatized]).toarray().tolist()[0]
    print(vectorized)
    sentence_words = vectorizer.get_feature_names_out()
    new_vector = [0 for _ in range(len(col_words))]
    for ind, i in enum(sentence_words):
        if i in col_words:
            new_vector[col_words.index(i)] = vectorized[ind]
    found = vector_database.get_nns_by_vector(new_vector, n)
    results = []
    for i in found:
        results.append((PATH_TO_IMGS+records[i][0], records[i][1]))
    return results

# save()
# find("student girl", 20)
# print(a.get_nns_by_item(0, 100))
# print(a.get_nns_by_vector([1.0, 0.5, 0.5], 100))
