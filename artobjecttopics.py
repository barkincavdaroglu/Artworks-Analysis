import json
import string
from operator import itemgetter

import gensim
from gensim import corpora
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

stopwords = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()


def clean(artobject):
    stopwordremoval = " ".join([i for i in artobject.lower().split() if i not in stopwords])
    punctuationremoval = ''.join(ch for ch in stopwordremoval if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punctuationremoval.split())
    return normalized


with open('ArtObj.json', encoding='utf-8-sig') as json_file:
    data = json.load(json_file)
    list1 = []
    list2 = []
    for each in data:
        list1.append(each["description"])
        list2.append(each)

final = [clean(artobject).split() for artobject in list1]
dictionary = corpora.Dictionary(final)
DT_matrix = [dictionary.doc2bow(artobj) for artobj in final]
lda = gensim.models.ldamodel.LdaModel

lda_model_1 = lda(DT_matrix, num_topics=10, id2word=dictionary, passes=400, iterations=100)
print(lda_model_1.print_topics())

# [(0, '0.035*"gilt" + 0.017*"edge" + 0.014*"binding" + 0.012*"spine" + 0.012*"book" + 0.011*"panel" + 0.010*"inner" + 0.009*"title" + 0.008*"leather" + 0.008*"dated"'), (1, '0.012*"1822" + 0.006*"cameo" + 0.006*"quotation" + 0.006*"630" + 0.006*"andria" + 0.006*"cf" + 0.004*"table" + 0.002*"farnese" + 0.002*"salon" + 0.002*"p"'), (2, '0.006*"one" + 0.006*"figure" + 0.005*"art" + 0.005*"work" + 0.004*"painting" + 0.004*"made" + 0.004*"two" + 0.004*"artist" + 0.004*"century" + 0.004*"new"'), (3, '0.003*"benin" + 0.002*"dress" + 0.002*"bk" + 0.002*"oba" + 0.002*"sword" + 0.001*"fabric" + 0.001*"hersak" + 0.001*"skirt" + 0.001*"songye" + 0.001*"balenciaga"'), (4, '0.008*"periodical" + 0.007*"fleurs" + 0.003*"de" + 0.003*"chalk" + 0.003*"sheet" + 0.003*"recto" + 0.003*"jaguar" + 0.002*"inv" + 0.002*"metropolitan" + 0.002*"lucretia"'), (5, '0.018*"copy" + 0.018*"armstrong" + 0.013*"includes" + 0.013*"miss" + 0.012*"illustration" + 0.012*"book" + 0.011*"leather" + 0.010*"red" + 0.010*"title" + 0.010*"jayne"'), (6, '0.014*"copy" + 0.009*"jean" + 0.009*"edition" + 0.008*"reserved" + 0.008*"numbered" + 0.008*"numeral" + 0.008*"facsimile" + 0.008*"pol" + 0.007*"work" + 0.006*"roman"'), (7, '0.029*"endpapers" + 0.025*"marbled" + 0.022*"spine" + 0.020*"gilt" + 0.019*"red" + 0.018*"raised" + 0.018*"flexible" + 0.018*"band" + 0.016*"gold" + 0.016*"binding"'), (8, '0.008*"eisen" + 0.003*"de" + 0.002*"el" + 0.002*"di" + 0.002*"la" + 0.002*"louvre" + 0.001*"marilyn" + 0.001*"leonardo" + 0.001*"leonardo’s" + 0.001*"en"'), (9, '0.021*"sér" + 0.017*"title" + 0.015*"engraved" + 0.014*"cocteau" + 0.014*"page" + 0.013*"1" + 0.011*"cm" + 0.010*"dated" + 0.009*"parade" + 0.008*"x"')]

for artobject in list2:
    if artobject["description"].strip():
        bow2 = dictionary.doc2bow(artobject["description"].split())
        t = lda_model_1.get_document_topics(bow2)
        print(t)
        artobject["topics"] = max(t, key=itemgetter(1))[0]
    else:
        artobject["topics"] = -1

with open('Analyzed.json', 'w') as f:
    json.dump(list2, f)
