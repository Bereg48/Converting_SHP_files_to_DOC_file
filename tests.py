# import geopandas as gpd
# import networkx as nx
# import osmnx as ox
#
# # Указываем путь к исходному shp файлу
# shp_file = 'gis_osm_railways_free_1.shp'
#
# # Чтение shp файла в GeoDataFrame
# gdf = gpd.read_file(shp_file)
#
# # Исправление геометрии
# gdf['geometry'] = gdf['geometry'].buffer(0)
#
# # Построение графа
# graph = ox.graph_from_gdfs(gdf, network_type='all')
#
# # Задаем точки начала и конца маршрута
# point1 = (57.026619, 24.047104)
# point2 = (57.006804, 24.048792)
#
# # Получение ближайших узлов графа к заданным точкам
# nearest_node1 = ox.distance.nearest_nodes(graph, point1[1], point1[0])[0]
# nearest_node2 = ox.distance.nearest_nodes(graph, point2[1], point2[0])[0]
#
# # Построение маршрута
# route = nx.shortest_path(graph, nearest_node1, nearest_node2)
#
# # Создание нового GeoDataFrame для сохранения графа и маршрута в shp файл
# route_gdf = gdf.loc[route]
#
# # Указываем путь для сохранения результирующего shp файла
# output_shp_file = 'output_shp_file.shp'
#
# # Сохранение графа и маршрута в shp файл
# route_gdf.to_file(output_shp_file)

# import geopandas as gpd
# import networkx as nx
# import osmnx as ox
#
# # Указываем путь к исходному shp файлу
# shp_file = 'gis_osm_railways_free_1.shp'
#
# # Чтение shp файла в GeoDataFrame
# gdf = gpd.read_file(shp_file)
#
# # Исправление геометрии
# gdf['geometry'] = gdf['geometry'].buffer(0)
#
# # Преобразование геометрии полигона в полигон MultiPolygon
# polygon = gdf['geometry'].unary_union
#
# # Построение графа на основе полигона
# graph = ox.graph_from_polygon(polygon, network_type='all')
#
# # Задаем точки начала и конца маршрута
# point1 = (57.026619, 24.047104)
# point2 = (57.006804, 24.048792)
#
# # Получение ближайших узлов графа к заданным точкам
# nearest_node1 = ox.distance.nearest_nodes(graph, point1[1], point1[0])[0]
# nearest_node2 = ox.distance.nearest_nodes(graph, point2[1], point2[0])[0]
#
# # Построение маршрута
# route = nx.shortest_path(graph, nearest_node1, nearest_node2)
#
# # Создание нового GeoDataFrame для сохранения графа и маршрута в shp файл
# route_gdf = gdf.loc[route]
#
# # Указываем путь для сохранения результирующего shp файла
# output_shp_file = 'output_shp_file.shp'
#
# # Сохранение графа и маршрута в shp файл
# route_gdf.to_file(output_shp_file)

import geopandas as gpd
import networkx as nx
import osmnx as ox

# Указываем путь к исходному shp файлу
shp_file = 'gis_osm_railways_free_1.shp'

# Чтение shp файла в GeoDataFrame
gdf = gpd.read_file(shp_file)

# Проверяем геометрии на наличие значения None
has_null_geometries = gdf['geometry'].isnull().all()
if has_null_geometries:
    print("All geometries in the GeoDataFrame are None.")
    quit()

if not gdf['geometry'].empty and gdf['geometry'].notna().all():
    polygon = gdf['geometry'].unary_union
    if polygon is not None and polygon.is_valid:
        # continue with further operations
        # Your additional code here indented correctly
    else:
        print("Invalid geometries")
else:
    print("Empty GeoSeries")

# Фильтруем геометрии с None значениями
gdf = gdf[~gdf['geometry'].isnull()]

# Проверяем, что остались геометрии после фильтрации
if len(gdf) == 0:
    print("There are no valid geometries in the GeoDataFrame.")
    quit()

# Исправление геометрии
gdf['geometry'] = gdf['geometry'].buffer(0)

# Преобразование геометрии полигона в полигон MultiPolygon
polygon = gdf['geometry'].unary_union

# Проверяем, что полигон имеет правильное значение
if polygon.is_valid:
    # Построение графа на основе полигона
    graph = ox.graph_from_polygon(polygon, network_type='all')

    # Задаем точки начала и конца маршрута
    point1 = (57.026619, 24.047104)
    point2 = (57.006804, 24.048792)

    # Получение ближайших узлов графа к заданным точкам
    nearest_node1 = ox.distance.nearest_nodes(graph, point1[1], point1[0])[0]
    nearest_node2 = ox.distance.nearest_nodes(graph, point2[1], point2[0])[0]

    # Построение маршрута
    route = nx.shortest_path(graph, nearest_node1, nearest_node2)

    # Создание нового GeoDataFrame для сохранения графа и маршрута в shp файл
    route_gdf = gdf.loc[route]

    # Указываем путь для сохранения результирующего shp файла
    output_shp_file = 'output_shp_file.shp'

    # Сохранение графа и маршрута в shp файл
    route_gdf.to_file(output_shp_file)
else:
    print("The generated polygon is not valid.")
