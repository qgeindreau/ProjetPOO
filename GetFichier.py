import requests
import tarfile
import os

url_abs ="https://math.univ-angers.fr/~ducrot/pyds1/data/hep-th-abs.tar.gz"
url_cit = "https://math.univ-angers.fr/~ducrot/pyds1/data/hep-th-citations.tar.gz"

def get_name(url):
    URL=url.split("/")
    return URL[len(URL)-1]





def download(url):
    get = requests.get(url)
    name=get_name(url)
    open(name,'wb').write(get.content)
    return

def dl_unzip(url):
    download(url)
    with tarfile.open(get_name( url )) as f:
        f.extractall()
    os.remove(get_name(url))
dl_unzip(url_abs)
dl_unzip(url_cit)