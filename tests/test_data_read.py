from pathlib import Path
import pytest
from geoalert_unify.data_read import get_rgb

output_path = Path(__file__).parent.joinpath('test_data')

# def get_rgb(b1_path : str = '', b2_path : str = '', b3_path : str = '', output_path : str = ''):
def test_get_rgb():
    b1_path = str(output_path.joinpath('T38VNP_20190521T081611_B02_10m.jp2'))
    b2_path = str(output_path.joinpath('T38VNP_20190521T081611_B03_10m.jp2'))
    b3_path = str(output_path.joinpath('T38VNP_20190521T081611_B04_10m.jp2'))

    output_file = output_path.joinpath('output.tif')
    get_rgb(b1_path, b2_path, b3_path)
    assert output_file.is_file() == True