from decimal import Decimal
from docx import Document
import pandas as pd
import shapefile
import geopandas as gpd
import time
from tkinter import Tk, Button, Label, OptionMenu, filedialog
from tkinter.ttk import Progressbar
from tkinter import StringVar


# Функция для преобразования числа в формат градусы-минуты-секунды
def decimal_degree_to_dms(coord):
    degrees = int(coord)
    minutes_float = (coord - degrees) * 60
    minutes = int(minutes_float)
    seconds_float = (minutes_float - minutes) * 60
    seconds = Decimal(seconds_float).quantize(Decimal('0.0'))
    return f"{degrees}-{minutes}-{seconds}\""


def convert_shp_to_tab(shapefile_path, tabfile):
    # Чтение SHP файла
    gdf = gpd.read_file(shapefile_path)

    # Сохранение слоя в формате TAB
    gdf.to_file(tabfile, driver='MapInfo File')

    print(f'Слой успешно сохранен в файл "{tabfile}"')


# def save_coordinates_to_shp(shapefile_path):
#     """Функция позволяет добавить координаты точек
#     в таблицу атрибутов файла shapefile в различных
#     системах координат, преобразовав их в формат
#     градусы-минуты-секунды."""
#     # Чтение SHP файла
#     sf = shapefile.Reader(shapefile_path)
#
#     # Задание различных систем координат
#     crs_list = ['EPSG:4326', 'EPSG:3857', 'EPSG:3857']
#
#     # Создание пустого списка записей
#     records = []
#
#     # Загрузка полей из DBF файла
#     fields = sf.fields[1:]
#
#     # Добавление столбца с названием из таблицы атрибутов
#     field_names = [field[0] for field in fields]
#     field_names.append('CNTRY_NAME')
#
#     # Получение записей из DBF файла
#     for shape_record in sf.shapeRecords():
#         record = shape_record.record
#         record.append(record['CNTRY_NAME'])
#         records.append(record)
#
#     # Присвоение координат точкам в различных системах координат и преобразование их в формат градусы-минуты-секунды
#     for crs in crs_list:
#         for i, shape_record in enumerate(sf.shapeRecords()):
#             shape = shape_record.shape
#             for j, point in enumerate(shape.points):
#                 point = shapefile.point_to_decimal_degrees(point)
#                 shape.points[j] = shapefile.decimal_degrees_to_dms(
#                     point[0]), shapefile.decimal_degrees_to_dms(point[1])
#
#         # Сохранение полученных координат в таблицу атрибутов
#         with shapefile.Writer(shapefile_path) as shp_writer:
#             shp_writer.fields = sf.fields
#             shp_writer.records.extend(records)
#
#         print(f'Координаты в системе координат {crs} успешно сохранены в таблицу атрибутов файла SHP')
def save_coordinates_to_shp(shapefile_path):
    """Функция позволяет добавить координаты точек
    в таблицу атрибутов файла shapefile в различных
    системах координат, преобразовав их в формат
    градусы-минуты-секунды."""
    # Чтение SHP файла
    gdf = gpd.read_file(shapefile_path)

    # Задание различных систем координат
    crs_list = ['EPSG:4326', 'EPSG:3857', 'EPSG:3857']

    # Создание пустого датафрейма
    df = pd.DataFrame()

    # Добавление столбца с названием из таблицы атрибутов
    df['CNTRY_NAME'] = gdf['CNTRY_NAME']

    # Присвоение координат точкам в различных системах координат и преобразование их в формат градусы-минуты-секунды
    for crs in crs_list:
        gdf_crs = gdf.to_crs(crs)
        df[crs] = gdf_crs.geometry.apply(lambda geom: (decimal_degree_to_dms(geom.x), decimal_degree_to_dms(geom.y)))

    # Сохранение полученных координат в таблицу атрибутов
    with shapefile.Writer(shapefile_path) as shp_writer:
        shp_writer.fields = shapefile.load_dbf(shapefile_path).fields
        for i, row in df.iterrows():
            shp_writer.record(*row.tolist())

    print('Координаты успешно сохранены в таблицу атрибутов файла SHP')
# def save_coordinates_to_shp(shapefile_path):
#     gdf = gpd.read_file(shapefile_path)
#
#     crs_list = ['EPSG:4326', 'EPSG:3857', 'EPSG:3857']
#
#     df = pd.DataFrame()
#
#     # Добавление столбца с названием из таблицы атрибутов
#     df['CNTRY_NAME'] = gdf['CNTRY_NAME']
#
#     for crs in crs_list:
#         gdf_crs = gdf.to_crs(crs)
#         df[crs] = gdf_crs.geometry.apply(lambda geom: (decimal_degree_to_dms(geom.x), decimal_degree_to_dms(geom.y)))
#
#     # Сохранение полученных координат в таблицу атрибутов
#     with shapefile.Writer(shapefile_path) as shp_writer:
#         shp_writer.field('COORDINATES', 'C', '255')  # Добавление нового поля
#         shp_writer.shapeType = shapefile.POINT
#         for i, row in df.iterrows():
#             # Создать точку с координатами заданными в столбцах 'EPSG:4326'
#             point = shapefile.Point(row['EPSG:4326'][0], row['EPSG:4326'][1])
#
#             # Добавить точку в файл SHP
#             shp_writer.point(*point)
#
#             # Записать данные в файл DBF
#             coordinates = []
#             for value in row[crs_list]:
#                 if value is not None:
#                     coordinates.append(str(value))
#                     shp_writer.record(row['CNTRY_NAME'], ', '.join(coordinates))
#
#     print('Координаты успешно сохранены в таблицу атрибутов файла SHP')

def create_docx_from_shapefile(shapefile_path, crs_list, doc_path):
    """Функция позволяет создать документ docx на основе данных
    из shapefile с возможностью преобразования координат для разных
    систем координат"""
    gdf = gpd.read_file(shapefile_path)

    df = pd.DataFrame()
    df['CITY_NAME'] = gdf['CITY_NAME']
    df['CNTRY_NAME'] = gdf['CNTRY_NAME']

    for crs in crs_list:
        gdf_crs = gdf.to_crs(crs)
        df[crs] = gdf_crs.geometry.apply(lambda geom: (decimal_degree_to_dms(geom.x), decimal_degree_to_dms(geom.y)))

    doc = Document()
    table = doc.add_table(rows=1, cols=len(df.columns))
    header_cells = table.rows[0].cells
    for i, col_name in enumerate(df.columns):
        header_cells[i].text = col_name

    for _, row in df.iterrows():
        cells = table.add_row().cells
        for i, value in enumerate(row):
            cells[i].text = str(value)

    doc.save(doc_path)
    print(f'Данные успешно записаны в файл "{doc_path}"')


import geopandas as gpd



def merge_lines(shapefile_path):
    # Загрузка shp файла с линиями
    lines_gdf = gpd.read_file(shapefile_path)

    # Объединение всех линий в одну линию
    merged_line = lines_gdf.unary_union

    return merged_line


def calculate_area(shapefile_path):
    # Загрузка shp файла с полигонами
    polygons_gdf = gpd.read_file(shapefile_path)

    # Подсчет общей площади полигонов
    total_area = polygons_gdf.geometry.area.sum()

    return total_area
