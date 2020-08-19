import json

import requests
from bs4 import BeautifulSoup

url = "https://www.metmuseum.org/art/collection/search/"

cookies = {'incap_ses_1186_1661922': 'WJVsTr/vpTpmSo6N/4R1EAM9PF8AAAAAJMZq30Mwtn9GLYG3Ln2Zpg==',
           'visid_incap_1662004': 'XAvDNnL2RfeAkpfIvozoyhyIOV8AAAAAQUIPAAAAAACvTQA8Mo9AEcc3VGzSFsnh',
           '_ga': 'GA1.2.845980376.1597783314', '_gid': 'GA1.2.678224659.1597783314'}

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
