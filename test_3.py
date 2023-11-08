import tkinter as tk
from tkinter import filedialog
import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString

import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString

# Load shp file
shp_file = gpd.read_file('gis_osm_railways_free_1.shp')

# Create graph
G = nx.Graph()

# Add nodes
for i, row in shp_file.iterrows():
    G.add_node(i, pos=(row['geometry'].xy[0][0], row['geometry'].xy[1][0]))

# Add edges
for i, row in shp_file.iterrows():
    for j, row2 in shp_file.iterrows():
        if i != j:
            G.add_edge(i, j, weight=row['geometry'].distance(row2['geometry']))

# Build route
path = nx.dijkstra_path(G, source=0, target=len(G.nodes)-1)

# Visualization
pos = nx.get_node_attributes(G, 'pos')
nx.draw(G, pos, with_labels=True)

# Visualization of the route
path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2)

plt.show()


def run_code():
    shp_file_name = file_name.get()
    shp_file = gpd.read_file(shp_file_name)

    G = nx.Graph()

    for i, row in shp_file.iterrows():
        G.add_node(i, pos=(row['geometry'].x, row['geometry'].y))

    for i, row in shp_file.iterrows():
        for j, row2 in shp_file.iterrows():
            if i != j:
                G.add_edge(i, j, weight=row['geometry'].distance(row2['geometry']))

    path = nx.dijkstra_path(G, source=0, target=len(G.nodes) - 1)

    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True)

    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2)

    plt.show()


root = tk.Tk()

file_name = tk.StringVar()

tk.Label(root, text="File Name:").grid(row=0, column=0)
tk.Entry(root, textvariable=file_name).grid(row=0, column=1)

tk.Button(root, text="Browse", command=lambda: file_name.set(filedialog.askopenfilename())).grid(row=0, column=2)

tk.Button(root, text="Run", command=run_code).grid(row=1, column=1)

root.mainloop()
