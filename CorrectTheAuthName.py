import requests
import json
def correctName(nom):
    if type (nom)==(str):
        url="https://inspirehep.net/api/authors?sort=bestmatch&size=25&page=1&q="+nom
        response= requests.get(url)
        raw_data=response.text
        jsondata=json.loads(raw_data)
        if (nom.replace(' ',''))[0] == jsondata['hits']['hits'][0]['metadata']['name']['preferred_name'][0]:
                return(jsondata['hits']['hits'][0]['metadata']['name']['preferred_name'])
        elif (nom.replace(' ',''))[0] == jsondata['hits']['hits'][1]['metadata']['name']['preferred_name'][0]:
                return(jsondata['hits']['hits'][1]['metadata']['name']['preferred_name'])
        else:
                return(jsondata['hits']['hits'][0]['metadata']['name']['preferred_name'])
    if type(nom)==(list):
        for i in range(len(nom)):
                nom[i]=correctName(nom[i])
        return nom
