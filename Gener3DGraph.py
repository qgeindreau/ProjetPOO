import networkx as nw
import numpy as np
from mayavi import mlab


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

k=nw.DiGraph()
dico=({'voiture':'4roues','moto':'2roues'})
k.add_edges_from((key,dico[key])for key in dico.keys())