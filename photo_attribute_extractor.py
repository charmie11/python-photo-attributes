""" This code is to extract attributes from digital pictures """
from typing import Union
import os

from datetime import datetime
import exif
from geopy.geocoders import Nominatim
import skimage


def make_test_image():
    """ make a sample image with EXIF """

    # load a sample image
    image = skimage.data.coffee()
    filename = 'photo-without-exif.jpg'
    skimage.io.imsave(filename, image)
    extractor = exif.Image(filename)

    # add exif information
    exif_image = exif.Image(filename)
    exif_image.make = "Python"
    exif_image.gps_latitude = (41.0, 29.0, 57.48)
    exif_image.gps_latitude_ref = "N"
    exif_image.gps_longitude = (81.0, 41.0, 39.84)
    exif_image.gps_longitude_ref = "W"
    exif_image.gps_altitude = 199.034
    exif_image.gps_altitude_ref = 0
    exif_image.datetime_original = '1999:12:31 23:49:12'
    exif_image.datetime_digitized = '2020:07:11 10:11:37'

    filename = 'photo-with-exif.jpg'
    with open(filename, 'wb') as image_file:
        image_file.write(exif_image.get_file())
    extractor = exif.Image(filename)
    print(f'{filename} has exif: {extractor.has_exif}')


class PhotoAttributeExtractor:
    """ A class for extracting attributes of a digital picture """

    def __init__(
        self,
        filename: Union[str, bytes, os.PathLike]
    ):
        """ set a file path
            filename (path like object): A file path.
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f'specified {filename} does not exist!')
        try:
            skimage.io.imread(filename)
            print(f'load {filename}')
        except Exception:
            raise IOError(f'{filename} is not a picture')

        self.filename = filename
        self.image = exif.Image(self.filename)

    def extract_date(self):
        """ returns the date the photo was taken.

        If EXIF has creation date/time, this function returns the date from EXIF.
        Otherwise, this function returns the date the file created.

        The returned date is formatted as Japanese.
        """
        if 'datetime_original' in dir(self.image):
            date_time_taken = datetime.strptime(self.image.datetime_original, '%Y:%m:%d %H:%M:%S')
        else:
            date_time_taken = datetime.fromtimestamp(os.path.getmtime(self.filename))
        return date_time_taken.strftime('%Y年%m月%d日')

    def extract_address(self):
        """ returns the city name the photo was taken.

        If EXIF has GPS location data, this function returns the corresponding address.
        Otherwise, this function returns empty string.

        The returned date is formatted as Japanese.
        """
        address = ''
        if 'gps_latitude' in dir(self.image) and 'gps_longitude' in dir(self.image):
            latitude = self.image.gps_latitude
            latitude = latitude[0] + 0.01 * latitude[1] + 0.0001 * latitude[2]
            if self.image.gps_latitude_ref == 'S':
                latitude *= -1
            longitude = self.image.gps_longitude
            longitude = longitude[0] + 0.01 * longitude[1] + 0.0001 * longitude[2]
            if self.image.gps_longitude_ref == 'W':
                longitude *= -1

            geolocator = Nominatim(user_agent="test")
            address = geolocator.reverse(f"{latitude}, {longitude}", language='ja').address

        return address


def main():

    make_test_image()
    for filename in ['photo-without-exif.jpg', 'photo-with-exif.jpg']:
        print(f'filename: {filename}')
        extractor = PhotoAttributeExtractor(filename)

        print(f'  date taken: {extractor.extract_date()}')
        print(f'  address: {extractor.extract_address()}')

    #
    extractor = PhotoAttributeExtractor('photo-with-exif.jpg')
    print(f'  Building name not contained: {extractor.extract_address()}')
    extractor.image.gps_latitude = (35.0, 51.0, 86.14)
    extractor.image.gps_latitude_ref = 'N'
    extractor.image.gps_longitude = (134.0, 17.0, 49.25)
    extractor.image.gps_longitude_ref = 'E'
    print(f'  Building name contained: {extractor.extract_address()}')


if __name__ == '__main__':
    main()
