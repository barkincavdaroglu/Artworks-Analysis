import requests
import json
from ratelimit import limits
from bs4 import BeautifulSoup
import concurrent.futures
import time
from urllib.parse import urlparse
from threading import Thread
import http.client, sys
import queue

import concurrent.futures
import requests
import time

out = []
CONNECTIONS = 150
TIMEOUT = 5
list1 = []
with open('ObjectIDsList.json') as json_file:
    data = json.load(json_file)
    for artobject in data["objectIDs"]:
        list1.append(artobject)

response = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/objects")
artobjectlist = json.loads(response.content)
artlist = []


allartobjects = []
def load_url(url, timeout):
    ans = requests.get(url, timeout=timeout)
    artobject = json.loads(ans.content)
    print(artobject["objectID"])

    return artobject

with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
    for each in list1:
        artlist.append("https://collectionapi.metmuseum.org/public/collection/v1/objects/" + str(each))

    future_to_url = (executor.submit(load_url, url, TIMEOUT) for url in artlist)
    time1 = time.time()
    for future in concurrent.futures.as_completed(future_to_url):
        try:
            data = future.result()
        except Exception as exc:
            data = str(type(exc))
        finally:
            out.append(data)
    with open('ArtObjectsWithImageLinks.json', 'w') as f:
        json.dump(out, f)



    time2 = time.time()










cookies = {'incap_ses_1186_1661922': 'WJVsTr/vpTpmSo6N/4R1EAM9PF8AAAAAJMZq30Mwtn9GLYG3Ln2Zpg==',
           'visid_incap_1662004': 'XAvDNnL2RfeAkpfIvozoyhyIOV8AAAAAQUIPAAAAAACvTQA8Mo9AEcc3VGzSFsnh',
           '_ga': 'GA1.2.845980376.1597783314', '_gid': 'GA1.2.678224659.1597783314'}


# def APICall2(url):
#     response = requests.get("https://collectionapi.metmuseum.org/public/collection/v1/objects")
#     artobjectlist = json.loads(response.content)
#     print(artobjectlist)
#     APICall("https://www.metmuseum.org/art/collection/search/", artobjectlist["objectIDs"])


# def APICall(url, artlist):
#     with open('AllArtObjects.json', 'w') as f:
#         for objectID in artlist:
#             response2 = requests.get(
#                 "https://collectionapi.metmuseum.org/public/collection/v1/objects/" + str(objectID))
#             artobject = json.loads(response2.content)
#             print(artobject)
#             json.dump(artobject, f)
#
#
# APICall2(url2)


def WebCrawler():
    culturesToArtObjects = {}
    with open('ObjectIDsList.json') as json_file:
        data = json.load(json_file)
        with open('AllArtObjects.json', 'w') as f:
            list1 = []
            for artobject in data:
                if artobject["Is Timeline Work"] == "True":
                    url += artobject["Object ID"]
                    html_http = requests.get(url, cookies=cookies)
                    data2 = html_http.text
                    soup = BeautifulSoup(data2, "html.parser")
                    result = soup.find("div", attrs="artwork__intro__desc")
                    descr = result.get_text()
                    artobject["description"] = descr
                    list1.append(artobject)

                    url = "https://www.metmuseum.org/art/collection/search/"
            json.dump(list1, f)
