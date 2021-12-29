from pathlib import Path
import rasterio
import numpy as np
from geoalert_unify.data_process import RastersProcess

def get_rgb(b1_path : str = '', b2_path : str = '', b3_path : str = '', output_path : str = ''
                                                  , output_name : str = '') -> None:
    raster = RastersIO()
    raster.get_rgb(b1_path, b2_path, b3_path)
    raster.output_rgb(output_path, output_name)    


class RastersIO():
    def __init__(self) -> None:
        self.output_options = {}
        self.rgb = []
        self.first_input_path = ''

    def get_rgb(self, b1_path : str = '', b2_path : str = '', b3_path : str = '') -> None:
        """
            get a stacked RGB image from 3 bands input,
            calls RasterProcess constrcut_rgb method.

            args:
            ----
            b1_path: str
            path to the first band image(red band).
            b2_path: str
            path to the second band image(green band).
            b3_path: str
            path to the third band image(blue band).
        """
        rater_process = RastersProcess()
        img_ob = rater_process.construct_rgb( b1_path, b2_path, b3_path)
        self.rgb, self.output_options =  img_ob['img'], img_ob['input_options']
        self.first_input_path = str(Path(b1_path).parent)

    def output_rgb(self, output_path : str, output_name : str) -> None:
        """
        writes the image to a tiff file via rasterio.
        
        args:
        output_path: str
            path to which the file will be output,
            if it's not provided the path of the
            first band will be used.
        output_name: str
            if the name of the output file,
            if it's not provided the default
            name would be "output".
        """
        if output_path == '':
            output_path = self.first_input_path
        if output_name == '':
            output_name = '/output'

        output_path = output_path + output_name + '.tif'
        self.output_options.update({'driver':'GTiff'})
        self.output_options.update({'count':3})
        self.output_options.update({'dtype':np.uint8})

        with rasterio.open(output_path,'w',
        **self.output_options) as output:
            output.write(self.rgb)


# pathes = [str(Path(__file__).parent.parent.joinpath('data/T38VNP_20190521T081611_B02_10m.jp2')),
# str(Path(__file__).parent.parent.joinpath('data/T38VNP_20190521T081611_B03_10m.jp2')),
# str(Path(__file__).parent.parent.joinpath('data/T38VNP_20190521T081611_B04_10m.jp2'))
# ]

# get_rgb(pathes[0], pathes[1], pathes[2])

