import random
import matplotlib.pyplot as plt
from numpy import std, mean
from itertools import groupby
from collections import Counter
from math import log, sqrt
k = 1.6
_CORPUS_SIZE = 10

def generate_line():
    line = []
    line.append(10000*random.random())
    while len(line) < 1000:
        a = line[-1] * 0.95
        b = line[-1] * 1.05
        line.append(random.uniform(a, b))

    return line

def add_points(line, shift=False):
    while len(line) < 1000:
        if shift:
            a = line[0] * 0.95
            b = line[0] * 1.05
            line.insert(0, random.uniform(a, b))
        else:
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
    while len(corpus.keys()) < _CORPUS_SIZE:
        line = generate_line()
        lines[len(lines.keys())] = line
        corpus[len(corpus.keys())] = dict(slice_lists(line))

    """
    max_id = len(corpus.keys())
    mutations = mutate_line(lines[0])
    for i, mutation in enumerate(mutations):
        lines[max_id+i] = mutation
        corpus[max_id+i] = dict(slice_lists(mutation))
    """

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
    dfw = len(inverted_index[word])

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
    return total / float(len(documents))

"""
def document_freq(word, documents):
    dfw = 0
    for (name, document) in documents:
        if word in document:
            dfw += 1
    return dfw
"""

def fuzz_line(line):
    return [fuzz_point(x) for x in line]

def fuzz_point(point):
    a = point * 0.95
    b = point * 1.05
    return random.uniform(a, b)

def mutate_line(line):
    plot_line(line)
    mutated_lines = []
    new_line = fuzz_line([point*3 for point in line])
    mutated_lines.append(new_line)
    #plot_line(new_line)

    new_line_2 = fuzz_line([point*0.5 for point in line])
    mutated_lines.append(new_line_2)
    #plot_line(new_line_2)

    new_line_3 = fuzz_line([point*0.1 for point in line])
    mutated_lines.append(new_line_3)
    #plot_line(new_line_3)

    new_line_4 = fuzz_line(add_points(line[100:]))
    mutated_lines.append(new_line_4)
    #plot_line(new_line_4)

    new_line_5 = fuzz_line(add_points(line[250:]))
    mutated_lines.append(new_line_5)
    #plot_line(new_line_5)

    new_line_6 = fuzz_line(add_points(line[:-100], shift=True))
    mutated_lines.append(new_line_6)
    #plot_line(new_line_6)

    new_line_7 = fuzz_line(add_points(line[:-250], shift=True))
    mutated_lines.append(new_line_7)
    #plot_line(new_line_7)

    new_line_8 = fuzz_line([point*2 for point in add_points(line[:-250], shift=True)])
    mutated_lines.append(new_line_8)
    #plot_line(new_line_8)

    new_line_9 = fuzz_line([point*3 for point in add_points(line[100:])])
    mutated_lines.append(new_line_9)
    #plot_line(new_line_9)

    new_line_10 = fuzz_line([point*0.2 for point in add_points(line[:-100], shift=True)])
    mutated_lines.append(new_line_10)
    #plot_line(new_line_10)

    #plt.show()
    return mutated_lines

random.seed("french75")
mutant_ids = range(1000, 1010)
top_20_matches = []
top_11_matches = []

for i in range(0, 100):
    corpus, lines = build_corpus()
    print len(corpus.keys())
    print "Built corpus"
    inverted_index = build_inverted_index(corpus)
    print "Built inverted index"

    ranking = []
    avgd = avg_doc_length(corpus.items())
    c = len(corpus.items())
    for (doc_id, vector) in corpus.items():
        score = tf_weighted_cosine((0, corpus[0]), (doc_id, corpus[doc_id]))
        ranking.append((0, doc_id, score))

    ranking.sort(key=lambda tup: tup[2])
    ranking = ranking[::-1]

    top_20 = ranking[:21]
    top_11 = ranking[:11]

    mutants = 0
    for (q_id, d_id, score) in top_20:
        if d_id in mutant_ids:
            mutants += 1
    top_20_matches.append((i, mutants))

    mutants = 0
    for (q_id, d_id, score) in top_11:
        if d_id in mutant_ids:
            mutants += 1
    top_11_matches.append((i, mutants))

print len(top_20_matches), top_20_matches
print len(top_11_matches), top_11_matches


