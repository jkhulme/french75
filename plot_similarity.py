from math import log, sqrt

"""
#x@y
line_1 = {'aacc': 1, 'ccaa': 1, 'acba': 1, 'aabc': 1, 'abbc': 1}
#x@a
line_2 = {'aacc': 1, 'aabc': 1, 'abbc': 1}
#x@z
line_3 = {'aacc': 1, 'aabc': 1}
"""

"""
#X@Y
line_1 = {'ac': 2, 'bb': 2, 'ca': 1}
#X@A
line_2 = {'ac': 2, 'bb': 1}
#X@Z
line_3 = {'ac': 1}
"""


#aSrc_total_MB@cytoplasm
line_7 = {'ccbbaaaa': 2, 'cccccaaa': 2, 'bbbbbbbb': 2, 'bbbbbbbc': 2, 'ccbaaaaa': 2, 'caaaaccc': 1, 'cbccacaa': 1, 'accccaca': 1, 'bcaaaacc': 1, 'cccbaaaa': 1, 'aaabcccc': 1, 'cccacaaa': 1, 'ccccaaaa': 1, 'aaccccac': 1, 'acaabaca': 1, 'aaaabccc': 1, 'cbbaaaaa': 1, 'aaacccca': 1, 'aaaacccc': 1, 'aabccccc': 1, 'bbcaaaac': 1, 'cbaaaaaa': 1, 'aaaaaccc': 1, 'ccccbaaa': 1, 'bbbbbcaa': 1, 'bbbbbbca': 1, 'cacaabac': 1, 'ccacaaba': 1, 'cbbbbbbb': 1, 'abccccaa': 1, 'aaaaaacc': 1, 'aabcccca': 1}
#aSrc_total_MB@cell_membrane
line_8 = {'ccbbaaaa': 2, 'cccccaaa': 2, 'bbbbbbbb': 2, 'bbbbbbbc': 2, 'ccbaaaaa': 2, 'caaaaccc': 1, 'cbccacaa': 1, 'accccaca': 1, 'bcaaaacc': 1, 'cccbaaaa': 1, 'aaabcccc': 1, 'cccacaaa': 1, 'ccccaaaa': 1, 'aaccccac': 1, 'acaabaca': 1, 'aaaabccc': 1, 'cbbaaaaa': 1, 'aaacccca': 1, 'aaaacccc': 1, 'aabccccc': 1, 'bbcaaaac': 1, 'cbaaaaaa': 1, 'aaaaaccc': 1, 'ccccbaaa': 1, 'bbbbbcaa': 1, 'bbbbbbca': 1, 'cacaabac': 1, 'ccacaaba': 1, 'cbbbbbbb': 1, 'abccccaa': 1, 'aaaaaacc': 1, 'aabcccca': 1}
#aSrc_total_MB@perinuclear_region
line_9 = {'ccbbaaaa': 2, 'ccbaaaaa': 2, 'caaaaccc': 1, 'cbccacaa': 1, 'accccaca': 1, 'abccccaa': 1, 'bcaaaacc': 1, 'cccccaaa': 1, 'bbbbbbbc': 1, 'bbbbbbbb': 1, 'cccbaaaa': 1, 'aaabcccc': 1, 'cccacaaa': 1, 'aaaacccc': 1, 'aaccccac': 1, 'acaabaca': 1, 'aaaabccc': 1, 'cbbaaaaa': 1, 'aaacccca': 1, 'aabcccca': 1, 'aabccccc': 1, 'cbaaaaaa': 1, 'aaaaaccc': 1, 'ccccbaaa': 1, 'cacaabac': 1, 'ccacaaba': 1, 'cbbbbbbb': 1, 'aaaaaacc': 1}

#X@Y
line_4 = {'aaabbccc': 4, 'cccbbaaa': 3, 'ccccbaaa': 2, 'aaaabccc': 2, 'bbbbbbbb': 2, 'aaabcccc': 2, 'aabcccba': 1, 'aabccccc': 1, 'cccbaaaa': 1, 'abbbbbbb': 1, 'ccbaaaaa': 1, 'aabbcccb': 1, 'ccaaaaaa': 1, 'aacccccc': 1, 'aaaaaacc': 1, 'abcccbaa': 1, 'aaabbbcc': 1, 'bbbbbbbc': 1, 'cbbbbbbb': 1, 'cccbbbaa': 1, 'aaaaabcc': 1}
#X@A
line_5 = {'aaabbccc': 10, 'aaaabccc': 5, 'aaabcccc': 5, 'cccccccc': 1, 'aabccccc': 1, 'abbbbbbb': 1, 'aacccccc': 1, 'aaaaaacc': 1, 'bbbbbbbc': 1, 'aaaaabcc': 1}
#X@Z
line_6 = {'aaabbccc': 13, 'aaaabccc': 6, 'aaabcccc': 5, 'aaabbbcc': 1}


#aSrc_total_MB@cytoplasm
line_1 = {'aaabbccc': 22, 'cccbbaaa': 19, 'aaaabccc': 13, 'cccbaaaa': 11, 'aaabcccc': 9, 'ccccbaaa': 9, 'ccbbbaaa': 5, 'bccccbaa': 4, 'aabcccba': 3, 'ccbaaabc': 3, 'ccbaaaaa': 3, 'aaabcccb': 3, 'aabccccb': 3, 'cbaaabcc': 3, 'aaabbbcc': 3, 'bbcccbaa': 3, 'ccbbaaac': 2, 'ccbbaaab': 2, 'bbbbbbbb': 2, 'baaaabcc': 2, 'abcccbaa': 2, 'aabccccc': 2, 'bbbaaacc': 2, 'aaaaabcc': 2, 'aaaaaacc': 2, 'acccbbba': 1, 'bbbcccaa': 1, 'cbbbbaaa': 1, 'baaabccc': 1, 'cccbaaab': 1, 'aabbbccc': 1, 'aabbccca': 1, 'baaabbcc': 1, 'ccaaaabb': 1, 'bcccbaaa': 1, 'cbbbbbbb': 1, 'aaccccba': 1, 'aaccccbb': 1, 'bbbbaaac': 1, 'ccaaaaaa': 1, 'bbbbbbbc': 1, 'caaabbbc': 1}
#aSrc_total_MB@cell_membrane
line_2 = {'aaabbccc': 22, 'cccbbaaa': 19, 'aaaabccc': 13, 'cccbaaaa': 11, 'aaabcccc': 9, 'ccccbaaa': 9, 'ccbbbaaa': 5, 'bccccbaa': 4, 'aabcccba': 3, 'ccbaaabc': 3, 'ccbaaaaa': 3, 'aaabcccb': 3, 'aabccccb': 3, 'cbaaabcc': 3, 'aaabbbcc': 3, 'bbcccbaa': 3, 'ccbbaaac': 2, 'ccbbaaab': 2, 'bbbbbbbb': 2, 'baaaabcc': 2, 'abcccbaa': 2, 'aabccccc': 2, 'bbbaaacc': 2, 'aaaaabcc': 2, 'aaaaaacc': 2, 'acccbbba': 1, 'bbbcccaa': 1, 'cbbbbaaa': 1, 'baaabccc': 1, 'cccbaaab': 1, 'aabbbccc': 1, 'aabbccca': 1, 'baaabbcc': 1, 'ccaaaabb': 1, 'bcccbaaa': 1, 'cbbbbbbb': 1, 'aaccccba': 1, 'aaccccbb': 1, 'bbbbaaac': 1, 'ccaaaaaa': 1, 'bbbbbbbc': 1, 'caaabbbc': 1}
#aSrc_total_MB@perinuclear_region
line_3 = {'aaabbccc': 21, 'cccbbaaa': 19, 'aaaabccc': 12, 'cccbaaaa': 11, 'ccccbaaa': 9, 'aaabcccc': 9, 'ccbbbaaa': 5, 'bccccbaa': 4, 'aabcccba': 3, 'ccbaaabc': 3, 'aaabcccb': 3, 'aabccccb': 3, 'cbaaabcc': 3, 'aaabbbcc': 3, 'bbcccbaa': 3, 'ccbaaaaa': 3, 'ccbbaaac': 2, 'ccbbaaab': 2, 'baaaabcc': 2, 'abcccbaa': 2, 'aabccccc': 2, 'bbbaaacc': 2, 'acccbbba': 1, 'bbbcccaa': 1, 'cbbbbaaa': 1, 'baaabccc': 1, 'bbbbbbbb': 1, 'cccbaaab': 1, 'aabbbccc': 1, 'aabbccca': 1, 'baaabbcc': 1, 'ccaaaabb': 1, 'bcccbaaa': 1, 'aaaaabcc': 1, 'cbbbbbbb': 1, 'aaaaaacc': 1, 'aaccccba': 1, 'aaccccbb': 1, 'bbbbaaac': 1, 'ccaaaaaa': 1, 'caaabbbc': 1}


corpus = [line_1, line_2, line_3, line_4, line_5, line_6, line_7, line_8, line_9]
inverted_index = {}

k = 1.6

for i, line in enumerate(corpus):
    for word in line:
        if word not in inverted_index:
            inverted_index[word] = [i]
        else:
            inverted_index[word].append(i)

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

def solo_tf_idf(word, document):
    tfwd = document.get(word, 0)
    kd = k * len(document)
    avgd = avg_doc_length(corpus)
    c = len(corpus)
    dfw = document_freq(word, corpus)

    return (tfwd / float(tfwd + float(kd/avgd))) * log(c/float(dfw), 2)

def tf_weighted_cosine(doc_a, doc_b):
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
    for document in documents:
        total += len(document)
    return total / len(documents)

def document_freq(word, documents):
    dfw = 0
    for document in documents:
        if word in document:
            dfw += 1
    return dfw

#print tf_idf(line_1, line_1) #y,y
#print tf_idf(line_1, line_2) #y,a
#print tf_idf(line_1, line_3) #y,z

print tf_weighted_cosine(line_1, line_1) #y,y
print tf_weighted_cosine(line_1, line_2) #y,a
print tf_weighted_cosine(line_1, line_3) #y,z
print "%%%%%%"
print tf_weighted_cosine(line_2, line_1) #a,y
print tf_weighted_cosine(line_2, line_2) #a,a
print tf_weighted_cosine(line_2, line_3) #a,z
print "%%%%%%"
print tf_weighted_cosine(line_3, line_1) #z,y
print tf_weighted_cosine(line_3, line_2) #z,a
print tf_weighted_cosine(line_3, line_3) #z,z
