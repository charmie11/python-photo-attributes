# python-photo-attributes

A python package to extract attributes from photo data.

## Required packages

- [exif](https://gitlab.com/TNThieding/exif): to read EXIF
- [geopy](https://geopy.readthedocs.io/): to reverse geocode GPS
- [skimage](https://scikit-image.org/): image IO and to make test files

## How to use

```python
from photo_attribute_extractor import PhotoAttributeExtractor


filename = 'photo-with-EXIF.jpg'
extractor = PhotoAttributeExtractor(filename)

# to get created date
date_created = extractor.extract_date()
print(f'  date taken: {date_created}')
# to get address from GPS
address = extractor.extract_address()
print(f'  address: {address}')
```

The return value of `extract_address()` may contain building name.

```python
extractor = PhotoAttributeExtractor('photo-with-exif.jpg')
print(f'  Building name not contained: {extractor.extract_address()}')
extractor.image.gps_latitude = (35.0, 51.0, 86.14)
extractor.image.gps_latitude_ref = 'N'
extractor.image.gps_longitude = (134.0, 17.0, 49.25)
extractor.image.gps_longitude_ref = 'E'
print(f'  Building name contained: {extractor.extract_address()}')
```
Building name not contained: Ravenna Road, Twinsburg, Twinsburg Township, Summit County, オハイオ州, 44087, アメリカ合衆国
Building name contained: 鳥取大学前, 伏野覚寺線, 中茶屋, 鳥取市, 鳥取県, 680-0947, 日本
