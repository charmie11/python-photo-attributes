""" A series of unittest for PhotoAttributeExtractor """
import os
import re
import unittest

from photo_attribute_extractor import make_test_image
from photo_attribute_extractor import PhotoAttributeExtractor


class TestPhotoAttributeExtractor(unittest.TestCase):
    """ A series of unittest for PhotoAttributeExtractor """

    def test_file_not_exist(self):
        """ 存在しないファイルを指定したときのエラー処理を確認 """
        filename = 'test.txt'
        if os.path.exists(filename):
            os.remove(filename)
        with self.assertRaises(FileNotFoundError):
            PhotoAttributeExtractor(filename)

    def test_file_not_photo(self):
        """ 写真以外のファイルを指定したときのエラー処理を確認 """
        filename = 'test.txt'
        with open(filename, 'w'):
            pass
        with self.assertRaises(IOError):
            PhotoAttributeExtractor(filename)
        os.remove(filename)

    def test_extract_date(self):
        """ extract_date()が指定したフォーマットで日時を返すか確認 """
        make_test_image()
        filename = 'photo-with-exif.jpg'
        extractor = PhotoAttributeExtractor(filename)
        date_time_taken = extractor.extract_date()
        self.assertIsNotNone(
            re.fullmatch(r'\d{4}年\d{2}月\d{2}日', date_time_taken),
            print(f'{date_time_taken} must be formatted as YYYY年MM月DD日')
        )
        os.remove('photo-with-exif.jpg')
        os.remove('photo-without-exif.jpg')

    def test_extract_address(self):
        """ extract_address()が指定したフォーマットで住所を返すか確認 """
        make_test_image()

        filename = 'photo-with-exif.jpg'
        extractor = PhotoAttributeExtractor(filename)

        # address must be string with some length
        address = extractor.extract_address()
        self.assertGreaterEqual(
            len(address), 1,
            print(f'{address} must be non-empty')
        )

        # address must be empty string if latitude is unavailable
        latitude = extractor.image.gps_latitude
        del extractor.image.gps_latitude
        address = extractor.extract_address()
        self.assertEqual(
            len(address), 0,
            print(f'address must be empty if latitude is not available')
        )
        extractor.image.gps_latitude = latitude

        # address must be empty string if longitude is unavailable
        longitude = extractor.image.gps_longitude
        del extractor.image.gps_longitude
        address = extractor.extract_address()
        self.assertEqual(
            len(address), 0,
            print(f'address must be empty if longitude is not available')
        )
        extractor.image.gps_latitude = longitude

        os.remove('photo-with-exif.jpg')
        os.remove('photo-without-exif.jpg')


if __name__ == '__main__':
    unittest.main()
