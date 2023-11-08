from osgeo import gdal, ogr, osr
from glob import glob


def mosaic_and_reproject_tiles(input_folder, output_file, target_srs):
    input_files = glob(input_folder + "/*.tif")
    mosaic = gdal.Warp(output_file, input_files, format="GTiff", options=["COMPRESS=DEFLATE", "PREDICTOR=2"])
    dataset = gdal.Open(output_file)

    source_srs = osr.SpatialReference()
    source_srs.ImportFromWkt(dataset.GetProjection())
    transform = osr.CoordinateTransformation(source_srs, target_srs)

    output_file_reprojected = output_file[:-4] + "_reprojected.tif"
    gdal.Warp(output_file_reprojected, dataset, srcSRS=source_srs, dstSRS=target_srs,
              xRes=0.1, yRes=0.1, width=1000, height=1000, options=["COMPRESS=DEFLATE", "PREDICTOR=2"])

    dataset = None
    mosaic = None

    return output_file_reprojected


# Example usage
input_folder = "/path/to/input/folder"
output_file = "/path/to/output/mosaic.tif"
target_srs = osr.SpatialReference()
target_srs.ImportFromEPSG(4326)

mosaic_and_reproject_tiles(input_folder, output_file, target_srs)
