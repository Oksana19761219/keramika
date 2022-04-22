from PIL import Image
import numpy as np

def open_file(): # i sia funkcija dar reikia ideti dpi korekcija
    im = Image.open("images/234_k.tif") # reikes sutvarkyti falu atidaryma, sitas variantas juodrastinis
    return im


def _get_data_from_image(im):
    data = im.getdata()
    data_np = np.array(data)
    return data_np


def _calculate_pixel_coordinates(pixel_index, image_width):
    x = pixel_index % image_width
    y = pixel_index // image_width
    return x, y

def _find_green_pixels(image):
    pixels = _get_data_from_image(image)
    r, g, b = pixels[:,0], pixels[:, 1], pixels[:,2]
    green_color = (g > 200) & (g - r > 100) & (g - b > 100)
    green_color_place = np.where(green_color)
    return green_color_place


def _get_green_pixels_coordinates(image):
    green_color_place = _find_green_pixels(image)
    calculate_coordinates_v = np.vectorize(_calculate_pixel_coordinates)
    image_width = image.size[0]
    x, y = calculate_coordinates_v(green_color_place, image_width)
    return x, y



def calculate_frame_corners_coordinates(image):
    x, y = _get_green_pixels_coordinates(image)
    coordinates = list(zip(x[0], y[0]))
    x_avg, y_avg = np.average(x), np.average(y)
    top_left_corner = [coord for coord in coordinates if coord[0] < x_avg and coord[1] < y_avg][0]
    top_right_corner = [coord for coord in coordinates if coord[0] > x_avg and coord[1] < y_avg][0]
    bottom_left_corner = [coord for coord in coordinates if coord[0] < x_avg and coord[1] > y_avg][0]
    bottom_right_corner = [coord for coord in coordinates if coord[0] > x_avg and coord[1] > y_avg][0]
    return top_left_corner, \
           top_right_corner, \
           bottom_left_corner, \
           bottom_right_corner


im = open_file()

top_left_corner, \
top_right_corner,  \
bottom_left_corner, \
bottom_right_corner = calculate_frame_corners_coordinates(im)

print(top_left_corner, \
top_right_corner,  \
bottom_left_corner, \
bottom_right_corner)









# blue_location = np.where((b > 165) & (b > g) & (b - r > 100))
# red_location = np.where((r > 200) & (r - g > 100) & (r - b > 100))
# green_location = np.where((g > 200) & (g - r > 100) & (g - b > 100))
# black_location = np.where((r < 20) & (g < 20) & (b < 20))
# image_dpi = image.info['dpi']


# pixels = get_data_from_image(im)
# r, g, b = pixels[:,0], pixels[:, 1], pixels[:,2]
# frame_location = np.where((b > 165) & (b > g) & (b - r > 100))
# print(frame_location)



# new_data = []
# for pixel in data:
#     r, g, b = pixel
#     frame_color = (b > 165) and (b > g) and (b - r > 100)
#     if frame_color:
#         new_data.append((0, 0, 0))
#     else:
#         new_data.append((255, 255, 255))
# im.putdata(new_data)
# im.show()

