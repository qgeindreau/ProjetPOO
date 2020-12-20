#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import chart_studio.plotly as py
from plotly.offline import iplot
import plotly.graph_objs as go

def Modelize(G,titre='',namefile='',labels='',colorgrp='',):
    N=G.vcount()
    layt=G.layout('kk3d',dim=3)
    Edges=[e.tuple for e in G.es]
    Xn=[]
    Yn=[]
    Zn=[]
    Xe=[]
    Ye=[]
    Ze=[]
    symboles=G.vs()['symbole']
    Taille=G.vs()['Taille']
    if labels=='':
        labels=G.vs()['label']
    if colorgrp=='':
        colorgrp=G.vs()['group']
    for k in range(N):
        Xn+=[layt[k][0]]
        Yn+=[layt[k][1]]
        Zn+=[layt[k][2]]
    for e in Edges:
        Xe+=[layt[e[0]][0],layt[e[1]][0],None]# x-coordinates of edge ends
        Ye+=[layt[e[0]][1],layt[e[1]][1],None]
        Ze+=[layt[e[0]][2],layt[e[1]][2],None]
    trace1=go.Scatter3d(x=Xe, y=Ye, z=Ze, mode='lines', line=dict(color='rgb(125,125,125)', width=0.5),hoverinfo='none')
    trace2=go.Scatter3d(x=Xn, y=Yn, z=Zn, mode='markers', name='actors', 
        marker=dict(symbol=symboles, size=Taille,color=colorgrp, 
        line=dict(color='rgb(50,50,50)', width=0.5)), text=labels, hoverinfo='text')
    axis=dict(showbackground=False, showline=False, zeroline=False, showgrid=False, showticklabels=False, title='')

    layout = go.Layout(
         title=titre,
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
    iplot(fig, filename=namefile)
    return
