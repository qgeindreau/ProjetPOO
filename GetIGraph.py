import igraph as ig
def reseaux_de_citations(document):
    graphe_cit = ig.Graph(directed=True)
    with open(document,mode='rb') as f:
        for line in f:
            ligne = (line.decode(encoding='utf8')).replace('\n','').split(' ')
            graphe_cit.add_vertices(ligne[0])
            graphe_cit.add_vertices(ligne[1])
            graphe_cit.add_edge(ligne[0], ligne[1])
    return graphe_cit

a=reseaux_de_citations('hep-th-test')
