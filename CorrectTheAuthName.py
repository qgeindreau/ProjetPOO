import requests
import json
def correctName(nom):
    if type (nom)==(str):
        try:
            ndf=nom.split(' ')
            ndf=ndf[len(ndf)-1]
        except IndexError:
            print('Nom non valide')
            return(nom)
        url="https://inspirehep.net/api/authors?sort=bestmatch&size=25&page=1&q="+nom.replace(' ','%20')
        response= requests.get(url)
        raw_data=response.text
        jsondata=json.loads(raw_data)
        for i in range(5):
            try:
                if jsondata['hits']['hits'][i]['metadata']['name']['preferred_name'].find(ndf)!=(-1) and jsondata['hits']['hits'][i]['metadata']['name']['preferred_name'][0]==nom.replace(' ','')[0]:
                    return(jsondata['hits']['hits'][i]['metadata']['name']['preferred_name'])
            except IndexError:
                print('Nom non valide')
                return(nom)
        return(jsondata['hits']['hits'][0]['metadata']['name']['preferred_name'])
    if type(nom)==(list):
        for i in range(len(nom)):
                nom[i]=correctName(nom[i])
        return nom
