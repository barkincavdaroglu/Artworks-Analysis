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

# for i in range(len(list2)):
#     if list2[i]["description"].strip():
#         bow2 = dictionary.doc2bow(list2[i]["description"].split())
#         t = lda_model_1.get_document_topics(bow2)
#         list2[i]["topics"] = max(t, key=itemgetter(1))[0]
#     else:
#         continue

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
