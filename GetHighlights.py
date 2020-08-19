import json

culturesToArtObjects = {}
with open('ArtObjects.json') as json_file:
    data = json.load(json_file)
    with open('Highlighted.json', 'w') as f:
        list1 = []
        for artobject in data:

            if artobject['Is Highlight'] == 'True':
                list1.append(artobject)
                # json.dump(artobject, f)
        json.dump(list1, f)
