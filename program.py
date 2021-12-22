import openpyxl
from pathlib import Path
from parsivar import *
from parsivar import Normalizer
from parsivar import Tokenizer
import stopWords
import pickle
import itertools
import math

xlsx_file = Path('../IR1_7k_news.xlsx')
wb_obj = openpyxl.load_workbook(xlsx_file)
sheet = wb_obj.active

punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

my_normalizer = Normalizer()
def preprocessing(line):
    for p in punc:
        line = line.replace(p, "")

    my_tokenizer = Tokenizer()
    words = my_tokenizer.tokenize_words(my_normalizer.normalize(line))
    # my_stemmer = FindStems()
    # stemFree = []

    for word in stopWords.stopWords:
        for token in words:
            if token == word:
                words.remove(token)
    # for word in words:
    #     stemFree.append(my_stemmer.convert_to_stem(word))

    return words


fileno = 0

pos_index = {}
i = 0
for row in sheet.iter_rows():
    print(i)
    i += 1
    final_token_list = preprocessing(row[0].value)
    #print(final_token_list)

    for pos, term in enumerate(final_token_list):

        if term in pos_index:

            pos_index[term][0] = pos_index[term][0] + 1

            if fileno in pos_index[term][1]:
                pos_index[term][1][fileno] += 1

            else:
                pos_index[term][1][fileno] = 1
        else:

            pos_index[term] = []
            pos_index[term].append(1)
            pos_index[term].append({})
            pos_index[term][1][fileno] = 1
    fileno += 1
def make_championList():
    unique_list= []
    same = []

    for term in pos_index:
        idf = len(pos_index[term][1])
        for d in pos_index[term][1]:
            count = pos_index[term][1][d]
            wd = (1 + math.log(count, 10)) * math.log(7562 / idf, 10)
            pos_index[term][1][d] = wd
        pos_index[term][1] = dict(sorted(pos_index[term][1].items(), key=lambda item: item[1], reverse=True))
        pos_index[term][1] = dict(itertools.islice(pos_index[term][1].items(), 10))


# print(pos_index['حسین'])
# print(fileno)
posindex_file = open("phase2.pkl", "wb")
pickle.dump(pos_index, posindex_file)
posindex_file.close()

make_championList()
championList_file = open("championList.pkl", "wb")
pickle.dump(pos_index, championList_file)
championList_file.close()
