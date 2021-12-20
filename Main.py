import pickle
from pathlib import Path
from parsivar import FindStems
import stopWords
import openpyxl
import matplotlib.pyplot as plt
from collections import OrderedDict

punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
xlsx_file = Path('../IR1_7k_news.xlsx')
wb_obj = openpyxl.load_workbook(xlsx_file)
def find_freq():
    freq = []
    for item in pos_index:
       freq.append(pos_index[item][0])
    return freq


def normalize_query(words):
    my_stemmer = FindStems()
    stemFree = []
    for word in stopWords.stopWords:
        for token in words:
            if token == word:
                words.remove(token)
    for word in words:
        stemFree.append(my_stemmer.convert_to_stem(word))
    return stemFree
def query_oneWord(word):
    doc_ids = []
    if not pos_index.get(word):
        return doc_ids

    dictionary = pos_index[word]
    for k in sorted(dictionary[1], key=lambda k: len(dictionary[1][k]), reverse=True):
        doc_ids.append(k)
    return doc_ids

def query_twoWord(word1,word2,distance):
    same = []
    not_k = []
    if not pos_index.get(word1) or pos_index.get(word2):
        return same , not_k
    for i in pos_index[word1][1]:
        for j in pos_index[word2][1]:
            if (i == j):
                not_k.append(i)
                for f in pos_index[word1][1][i]:
                    for g in pos_index[word2][1][j]:
                        if (f == g - distance):
                            same.append(i)
    same = list(set(same))
    not_k = list(set(not_k))
    not_k = list(set(not_k).difference(set(same)))

    return same , not_k

def intersection_lists(one_word_list,two_word_list):

    same = []
    i = set.intersection(*two_word_list)
    same.append(i)
    same.append(*two_word_list)
    same.append(*one_word_list)
    return same

def search_query(normalized_query):
    same = []
    if len(normalized_query) == 1:
        # print(normalized_query)
        same = query_oneWord(normalized_query[0])
        if len(same) == 0:
            print("notFound")
            return same

    elif len(normalized_query) == 2 :
        same , not_k = query_twoWord(normalized_query[0],normalized_query[1],1)
        # print(same)
        word_one = query_oneWord(normalized_query[0])
        word_two = query_oneWord(normalized_query[1])
        same = same + not_k
        for w in word_one:
            if w not in same:
                same.append(w)
        for w in word_two:
            if w not in same:
                same.append(w)

    elif len(normalized_query) == 3:
        same = []
        query_words = {}
        not_k = {}
        one_words = {}
        i = 0
        for j in range(0, len(normalized_query)):
            one_words[j] = (query_oneWord(normalized_query[j]))
        query_words[0], not_k[0] = (query_twoWord(normalized_query[0], normalized_query[1], 1))
        query_words[1], not_k[1] = (query_twoWord(normalized_query[0], normalized_query[2], 2))
        query_words[2], not_k[2] = (query_twoWord(normalized_query[1], normalized_query[2], 1))
        # for i in range(1,len(normalized_query)):
        #     query_words[i],not_k[i] = (query_twoWord(normalized_query[0], normalized_query[i], i))
        intersect_one_two_three2 = list(set(query_words[0]).intersection(query_words[1]))
        intersect_one_two_three = list(set(intersect_one_two_three2).intersection(query_words[2]))
        same = intersect_one_two_three
        same = same + query_words[0] + query_words[1] + query_words[2] + not_k[0] +not_k[1] + not_k[0] + one_words[0] + one_words[1] + one_words[2]
        same = list(OrderedDict.fromkeys(same))
    elif len(normalized_query) > 3:
        same = []
        not_k = {}
        query_words = {}
        one_words = {}
        intersect = {}
        i = 0
        for j in range(0, len(normalized_query)):
            one_words[j] = (query_oneWord(normalized_query[j]))
        for i in range(1,len(normalized_query)):
            query_words[i],not_k[i] = (query_twoWord(normalized_query[0], normalized_query[i], i))
        for j in range(1, len(normalized_query)):
            intersect[j] = list(set(one_words[j-1]).intersection(one_words[j]))
            same = same + intersect[j]
        # same = same + query_words[0] + query_words[1] + query_words[2] + not_k[0] + not_k[1] + not_k[0] + one_words[0] + \
        #        one_words[1] + one_words[2]
        same = list(OrderedDict.fromkeys(same))

       # same = intersect_one_two_three

    return same





#reading from file
posindex_file = open("withstem.pkl", "rb")
pos_index = pickle.load(posindex_file)

#get query & normalaizing
while(True):

    print("enter your query:")
    query = input()
    for p in punc:
        query = query.replace(p, "")
    sep_query=query.split()
    normalized_query = normalize_query(sep_query)
    print(normalized_query)
    same = search_query(normalized_query)
    for doc_id in same:
        print(wb_obj.active.cell(doc_id + 1, 2).value)
        print(wb_obj.active.cell(doc_id + 1, 3).value)


# a = find_freq()
# print(a)
# a.sort(reverse=True)
# plt.yscale('log')
# plt.xscale('log')
# plt.plot(a)
# plt.yscale('log')
# plt.xscale('log')
# plt.show()

# len = len(pos_index)
# sum = 0
# for i in pos_index:
#     sum = sum + pos_index[i][0]
#
# print(len)
# print(sum)

#
# plt.plot([102867,202964,305166,455227],[8650,12170,14700,20457])
# plt.plot([102867,202964,305166,455227],[10885,15504,18842,26763])
# plt.axis([0, 1000000, 0, 100000])
# plt.yscale('log')
# plt.xscale('log')
# plt.show()