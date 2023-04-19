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
