import os
import rasterio
import shutil
import numpy as np

color_dict = {
    1000 : np.array([255, 0, 0]),
    2100 : np.array([0, 166, 0]),
    2200 : np.array([128, 255, 0]),
    2300 : np.array([128, 255, 0]),
    3100 : np.array([255, 187, 34]),
    4100 : np.array([255, 255, 128]),
    4200 : np.array([168, 162, 50]),
    5100 : np.array([204, 242, 77]),
    5200 : np.array([166, 166, 255]),
    5300 : np.array([77, 77, 255]),
    7100 : np.array([180, 180, 180]),
    8100 : np.array([128, 242, 230]),
}

def toRaster_rgb(source_image, out_image, arr_in):
    path = source_image

    path_out = out_image

    with rasterio.open(path) as src:
        band_crs = src.crs
        band_tranform = src.transform

    meta = {
        "driver": "GTiff",
        "height": arr_in.shape[0],
        "width": arr_in.shape[1],
        "count": 3,  
        "dtype": 'uint8',
        "crs": band_crs,  
        "transform": band_tranform,

    }

    with rasterio.open(path_out, "w", **meta) as dst:
        for i in range(3):
            dst.write(arr_in[..., i], i + 1)


def convert_to_rgb(source_image, source_out, color_dict):
    with rasterio.open(source_image) as src:
        arr = src.read(1)
    
    arr_rgb = np.full(shape=(arr.shape[0], arr.shape[1], 3), fill_value=0, dtype=np.uint8)

    key_values = list(color_dict.keys())

    for k in key_values:
        mask = arr == k
        color = color_dict[k]
        arr_rgb[mask, :] = color
    toRaster_rgb(source_image, source_out, arr_rgb)


if __name__ == '__main__':
    
    if os.path.exists("images/image_reprojected.tif"):
        os.remove("images/image_reprojected.tif")

    source_image = 'images/map_2021_all.tif'
    rgb_out =  'images/map_2021_rgb.tif'
    max_zoom = 15
    nodata='255,255,255'
    convert_to_rgb(source_image, rgb_out, color_dict)

    if os.path.isdir('images/tiles'):
        shutil.rmtree('images/tiles')
    os.system(f'gdalwarp -srcnodata {nodata} -dstalpha  -t_srs EPSG:3857 {rgb_out} images/image_reprojected.tif')
    os.system(f'gdal2tiles --verbose  --processes=4  -z 0-{max_zoom} images/image_reprojected.tif images/tiles/')