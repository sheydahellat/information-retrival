import pickle
from pathlib import Path
from parsivar import FindStems
import stopWords
import openpyxl

punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
xlsx_file = Path('../IR1_7k_news.xlsx')
wb_obj = openpyxl.load_workbook(xlsx_file)

def normalize_query(words):
    # my_stemmer = FindStems()
    # stemFree = []
    for word in stopWords.stopWords:
        for token in words:
            if token == word:
                words.remove(token)
    # for word in words:
    #     stemFree.append(my_stemmer.convert_to_stem(word))
    return words

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

def query_twoWord(word1,word2):
    same = []
    for i in pos_index[word1][1]:
        for j in pos_index[word2][1]:
            if (i == j):
                for f in pos_index[word1][1][i]:
                    for g in pos_index[word2][1][i]:
                        if (f == g - 1):
                            same.append(i)
    same = list(set(same))
    return same

def search_query(normalized_query):
    if len(normalized_query) == 1:
        print(normalized_query)
        ids = query_oneWord(normalized_query[0])
        if len(ids) == 0:
            print("notFound")
            return
        for doc_id in ids:
            print(wb_obj.active.cell(doc_id+1,2).value)

    elif len(normalized_query) == 2 :
        same = query_twoWord(normalized_query[0],normalized_query[1])

    elif len(normalized_query) == 3:

        same1 = query_twoWord(normalized_query[0], normalized_query[1])
        same2 = query_twoWord(normalized_query[1], normalized_query[2])

    for doc_id in same:
        print(wb_obj.active.cell(doc_id+1,2).value)



        print(same)




#reading from file
posindex_file = open("new2.pkl", "rb")
pos_index = pickle.load(posindex_file)

#get query & normalaizing
print("vared kon")
query = input()
for p in punc:
    query = query.replace(p, "")
sep_query=query.split()
normalized_query = normalize_query(sep_query)
print(normalized_query)
search_query(normalized_query)
