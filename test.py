import json
from urllib.request import urlopen
import requests
import urllib.request
import igraph as ig

import chart_studio.plotly as py
from plotly.offline import iplot
import plotly.graph_objs as go

import networkx as nx

data = []

with urllib.request.urlopen("https://raw.githubusercontent.com/plotly/datasets/master/miserables.json") as response:
   html = response.read()
data = json.loads(html)

print(data.keys())

N=len(data['nodes'])
print(N)

L=len(data['links'])
Edges=[(data['links'][k]['source'], data['links'][k]['target']) for k in range(L)]
print(data['nodes'][0])
G=ig.Graph(Edges, directed=False)
layt=G.layout('kk', dim=3) # plot network with the Kamada-Kawai layout algorithm
print(G)
print(layt[:3])
print(Edges[:3])

labels=[]
group=[]

for node in data['nodes']:
  labels.append(node['name'])
  group.append(node['group'])

print(labels[:3])
print(group[:3])

Xn=[]
Yn=[]
Zn=[]

for k in range(N):
  Xn+=[layt[k][0]]
  Yn+=[layt[k][1]]
  Zn+=[layt[k][2]]

Xe=[]
Ye=[]
Ze=[]

for e in Edges:
  Xe+=[layt[e[0]][0],layt[e[1]][0],None]# x-coordinates of edge ends
  Ye+=[layt[e[0]][1],layt[e[1]][1],None]
  Ze+=[layt[e[0]][2],layt[e[1]][2],None]
print(Xe[:3])
print(Ye[:3])
print(Ze[:3])
trace1=go.Scatter3d(x=Xe, y=Ye, z=Ze, mode='lines', line=dict(color='rgb(125,125,125)', width=1),hoverinfo='none')

trace2=go.Scatter3d(x=Xn, y=Yn, z=Zn, mode='markers', name='actors', 
                   marker=dict(symbol='circle', size=6, color=group, colorscale='Viridis', 
                      line=dict(color='rgb(50,50,50)', width=0.5)), text=labels, hoverinfo='text')

axis=dict(showbackground=False, showline=False, zeroline=False, showgrid=False, showticklabels=False, title='')

layout = go.Layout(
         title="Network of coappearances of characters in Victor Hugo's novel<br> Les Miserables (3D visualization)",
         width=1000,
         height=1000,
         showlegend=False,
         scene=dict(
             xaxis=dict(axis),
             yaxis=dict(axis),
             zaxis=dict(axis),
        ))

data=[trace1, trace2]

fig=go.Figure(data=data, layout=layout)

iplot(fig, filename='Les-Miserables')