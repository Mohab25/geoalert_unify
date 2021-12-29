from pathlib import Path
from geoalert_unify.data_process import RastersProcess
import numpy as np
import rasterio

raster = RastersProcess()
output_path = Path(__file__).parent.joinpath('test_data')

def test_scale_band():
    b1_path = str(output_path.joinpath('T38VNP_20190521T081611_B02_10m.jp2'))
    band = rasterio.open(b1_path).read(1)
    sband = raster.scale_band(band)
    assert np.amax(sband) == 255

def test_get_rgb():
    b1_path = str(output_path.joinpath('T38VNP_20190521T081611_B02_10m.jp2'))
    b2_path = str(output_path.joinpath('T38VNP_20190521T081611_B03_10m.jp2'))
    b3_path = str(output_path.joinpath('T38VNP_20190521T081611_B04_10m.jp2'))
    band1 = rasterio.open(b1_path).read(1)
    band2 = rasterio.open(b2_path).read(1)
    band3 = rasterio.open(b3_path).read(1)
    img = {'b1':band1, 'b2':band2, 'b3':band3}
    rgb = raster.get_rgb(img)
    assert type(rgb) == np.ndarray
    assert len(rgb) == 3
    