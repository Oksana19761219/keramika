import os
import re

from PIL import Image
from image_transformation import transform_image



path = 'C:/Users/Lenovo/PycharmProjects/keramika_archeo/images'
entries = os.listdir(path)

pattern = re.compile(r'^(\w+)_(k|d)\.tif$')
for entry in entries:
    result = pattern.search(entry)
    if result:
        ceramic_nr = result.group(1)
        ceramic_orientation = result.group(2)
        print(entry, ceramic_nr, ceramic_orientation)
        im = Image.open(path+"/"+entry)
        # im.show()
        im = transform_image(im, 30, 30)
        im.save(path + "/" + ceramic_nr + 'corr.tif')
