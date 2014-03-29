import random
import matplotlib.pyplot as plt
from numpy import std, mean
from itertools import groupby
from collections import Counter
from math import log, sqrt
k = 1.6

def generate_line():
    line = []
    line.append(10000*random.random())
    while len(line) < 1000:
        a = line[-1] * 0.95
        b = line[-1] * 1.05
        line.append(random.uniform(a, b))

    return line

def plot_line(line):
    time = range(1, 10000, 10)
    plt.plot(time, line)
    plt.draw()

def build_corpus():
    corpus = {}
    lines = {}
    while len(corpus.keys()) < 10000:
        line = generate_line()
        lines[len(lines.keys())] = line
        corpus[len(corpus.keys())] = dict(slice_lists(line))
    return corpus, lines

def slice_lists(l):
    sub_lists = zip(l, l[1:], l[2:], l[3:], l[4:], l[5:], l[6:], l[7:])

    for i, sub_list in enumerate(sub_lists):
        l_mean = mean(sub_list)
        l_std = std(sub_list)
        sub_lists[i] = [(x - l_mean) / l_std for x in sub_list]

    for j, sub_list in enumerate(sub_lists):
        for i, element in enumerate(sub_list):
            if element < -0.43:
                sub_list[i] = "a"
            elif element > 0.43:
                sub_list[i] = "c"
            else:
                sub_list[i] = "b"
        sub_lists[j] = ''.join(sub_list)

    return Counter([k for k, g in groupby(sub_lists)])

def build_inverted_index(corpus):
    inverted_index = {}

    for doc_id, line in corpus.items():
        for word in line:
            if word not in inverted_index:
                inverted_index[word] = [doc_id]
            else:
                inverted_index[word].append(doc_id)
    return inverted_index

"""
def tf_idf(query, document):
    tfidf = 0
    avgd = avg_doc_length(corpus)
    kd = k * len(document)
    c = len(corpus)
    for word in query:
        tfwq = query[word]
        tfwd = document.get(word, 0)
        dfw = document_freq(word, corpus)
        middle = tfwd / float(tfwd + float(kd/avgd))
        tfidf += tfwq * middle * log(c/float(dfw), 2)
    return tfidf
"""

def solo_tf_idf(word, document):
    tfwd = document.get(word, 0)
    kd = k * len(document)
    avgd = avg_doc_length(corpus.items())
    c = len(corpus)
    dfw = document_freq(word, corpus.items())

    return (tfwd / float(tfwd + float(kd/avgd))) * log(c/float(dfw), 2)

def tf_weighted_cosine((name_a, doc_a), (name_b, doc_b)):
    top = 0
    for word in doc_a:
        top += solo_tf_idf(word, doc_a) * solo_tf_idf(word, doc_b)
    #print "top", top
    left = 0
    for word in doc_a:
        left += solo_tf_idf(word, doc_a)**2
    left = sqrt(left)
    #print "left", left

    right = 0
    for word in doc_b:
        right += solo_tf_idf(word, doc_b)**2
    right = sqrt(right)
    #print "right", right

    bottom = float(left * right)
    if bottom != 0.0:
        return top / float(left * right)
    else:
        return 0

def avg_doc_length(documents):
    total = 0
    for (name, document) in documents:
        total += len(document)
    return total / len(documents)

def document_freq(word, documents):
    dfw = 0
    for (name, document) in documents:
        if word in document:
            dfw += 1
    return dfw

random.seed("french75")
corpus, lines = build_corpus()
print "Built corpus"
inverted_index = build_inverted_index(corpus)
print "Built inverted index"

ranking = []

for (doc_id, vector) in corpus.items():
    score = tf_weighted_cosine((0, corpus[0]), (doc_id, corpus[doc_id]))
    ranking.append((0, doc_id, score))

ranking.sort(key=lambda tup: tup[2])
ranking = ranking[::-1]

best = ranking[1:11]
worst = ranking[-10:]

for (q_id, d_id, score) in best:
    plot_line(lines[0])
    plot_line(lines[d_id])
    plt.show()

for (q_id, d_id, score) in worst:
    plot_line(lines[0])
    plot_line(lines[d_id])
    plt.show()
