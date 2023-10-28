import osmnx as ox
import networkx as nx

# Открытие файла OSM XML с использованием кодировки utf-8
with open('latvia-latest.osm', 'r', encoding='utf-8') as file:
    xml_data = file.read()

# Загрузка графа дорог из XML-данных
graph = ox.graph_from_xml(xml_data, simplify=False)

# Анализ графа дорог
important_nodes = nx.betweenness_centrality(graph)  # алгоритм поиска важных узлов

# Вывод результатов анализа графа
print("Important nodes:")
for node, centrality in important_nodes.items():
    print(f"Node {node}: {centrality}")

# Постановка точек А, Б и промежуточного пункта
point_A = (37.774929, -122.419416)  # пример координаты точки А (Широта, Долгота)
point_B = (37.773972, -122.430998)  # пример координаты точки Б (Широта, Долгота)
waypoints = [(37.775094, -122.425445)]  # пример координат промежуточных пунктов

# Построение кратчайшего маршрута с промежуточными пунктами
route = ox.shortest_path(graph, point_A, point_B, weight='length', nodes_waypoints=waypoints)

# Вывод кратчайшего маршрута
print("Shortest route:")
print(route)
