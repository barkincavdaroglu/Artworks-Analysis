import json

import requests
from bs4 import BeautifulSoup

url = "https://www.metmuseum.org/art/collection/search/"

cookies = {'incap_ses_': '',
           'visid_incap_': '',
           '_ga': '', '_gid': ''}

culturesToArtObjects = {}
with open('ArtObj.json') as json_file:
    data = json.load(json_file)
    with open('TimelineWorks.json', 'w') as f:
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
