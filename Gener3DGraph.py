
# -*- coding: utf-8 -*-
import networkx as nw #Module pour générer des graphes
import numpy as np#Le fameux
from mayavi import mlab#Module pour générer un affichage 3d, abandonner au profit de plotly, vtk ne voulant pas s'installer sur mon pc



#Ne servira pas de base, mais peut toujours servir


def Draw3d(H):
    G = nw.convert_node_labels_to_integers(H)
    pos = nw.spring_layout(G, dim=3)
    xyz = np.array([pos[v] for v in G])
    scalars = np.array(list(G.nodes())) + 5
    pts = mlab.points3d(
        xyz[:, 0],
        xyz[:, 1],
        xyz[:, 2],
        scalars,
        scale_factor=0.1,
        scale_mode="none",
        colormap="Blues",
        resolution=20,
    )
    pts.mlab_source.dataset.lines = np.array(list(G.edges()))
    tube = mlab.pipeline.tube(pts, tube_radius=0.01)
    mlab.pipeline.surface(tube, color=(0.8, 0.8, 0.8))
    mlab.show()
    return

if __name__ == "__main__":
    print('Voici le rendu')
    k=nw.DiGraph()
    dico=({'voiture':'4roues','moto':'2roues'})
    k.add_edges_from((key,dico[key])for key in dico.keys())
    Draw3d(k)