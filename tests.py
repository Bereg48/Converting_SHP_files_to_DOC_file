import shapefile
import pyproj

def convert_coordinates(input_shapefile, target_projections, output_shapefile):
    sf = shapefile.Reader(input_shapefile)

    with open(input_shapefile.replace('.shp', '.prj'), 'r') as prj_file:
        prj_string = prj_file.read()

    records = sf.records()

    for i, record in enumerate(records):
        x = record['x']
        y = record['y']

        for target_proj in target_projections:
            transformer = pyproj.Transformer.from_crs(prj_string, target_proj.crs, always_xy=True)
            new_x, new_y = transformer.transform(x, y)

            field_name = f'new_x_{target_proj.crs}'.replace(':', '_')
            records[i][field_name] = new_x

            field_name = f'new_y_{target_proj.crs}'.replace(':', '_')
            records[i][field_name] = new_y

    w = shapefile.Writer()

    fields = sf.fields[1:]  # Исключаем поля самой геометрии
    for field in fields:
        w.field(*field)

    for target_proj in target_projections:
        crs_code = target_proj.crs.replace(':', '_')
        w.field(f'new_x_{crs_code}', fieldType='N', size=20, decimal=8)
        w.field(f'new_y_{crs_code}', fieldType='N', size=20, decimal=8)

    for record in records:
        w.record(*record)

    for shape in sf.shapes():
        w.shape(shape)

    w.save(output_shapefile)


input_shapefile = 'Europe_National_Provinces_Capitals.shp'
output_shapefile = ''
target_projections = [
    pyproj.Proj(init='EPSG:4326'),  # WGS84
    pyproj.Proj(init='EPSG:3857'),  # Web Mercator
    pyproj.Proj(init='EPSG:27700')  # British National Grid
    # и так далее
]

convert_coordinates(input_shapefile, target_projections, output_shapefile)
