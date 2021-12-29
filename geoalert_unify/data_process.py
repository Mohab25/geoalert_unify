import rasterio
import numpy as np
  

class RastersProcess():
    def __init__(self) -> None:
        self.input_options = {}

    def construct_rgb(self, b1_path : str = '', b2_path : str = '', b3_path : str = '') -> dict:
        """
            construct a stacked RGB image from 3 bands input,
            returns ab object holds the unified image, and
            input options of the bands (crs, transform ..etc.)

            args:
            ----
            b1_path: str
            path to the first band image(red band).
            b2_path: str
            path to the second band image(green band).
            b3_path: str
            path to the third band image(blue band).
        """
        img = {}
        self.get_band(b1_path, 'b1', img)
        self.get_band(b2_path, 'b2', img)
        self.get_band(b3_path, 'b3', img)

        rgb_img = self.get_rgb(img)
        return {'img':rgb_img, 'input_options': self.input_options}

    def get_band(self, b_path : str, b_name : str, img : dict)-> None:
        """
            reads the band via rasterio, calls 
            scaleband method to scale down images 
            from Unit16 to Unit8.

            args:
            ----
            b_path: str
                path to the band image.
            b_name: str
                name of the band, used 
                to construct and img
                object that holds all
                bands of the image.
            img: dict
                an object that holds all
                bands of the image.
        """
        with rasterio.open(b_path) as b_ds:
            band = b_ds.read(1)
            sband = self.scale_band(band)
            img.update({b_name:sband})
            self.input_options = b_ds.profile

    def scale_band(self,band)-> np.array:
        """
            scales 16-bit bands values
            to 8-bit values (0-255) range,
            returns a numpy array.

            args:
            ----
            band: np array
                an array of numerical values
                of the band image. 
        """
        max, min = np.amax(band), np.amin(band)
        scale = max-min
        scale = 255/scale
        sband = (band - min) * scale
        sband = (sband.clip(0, 255)+ 0.5).astype(np.uint8)
        return sband

    def get_rgb(self, img:dict)-> np.array:
        """
            combine bands to one image using
            numpy stack function.
            returns numpy array.

            args:
            ----
            img: dict
                an object that holds three image 
                bands.
        """
        return np.stack([img['b1'], img['b2'], img['b3']])
