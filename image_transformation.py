from PIL import Image
import numpy as np

def open_file(): # i sia funkcija dar reikia ideti dpi korekcija
    im = Image.open("images/265_d.tif") # reikes sutvarkyti falu atidaryma, sitas variantas juodrastinis
    return im


def get_data_from_image(im):
    data = im.getdata()
    data_np = np.array(data)
    return data_np


def calculate_pixel_coords(pixel_index, image_width):
    x = pixel_index % image_width
    y = pixel_index // image_width
    return x, y


def find_green_pixels(image):
    pixels = get_data_from_image(image)
    r, g, b = pixels[:,0], pixels[:, 1], pixels[:,2]
    green_color = (g > 200) & (g - r > 100) & (g - b > 100)
    green_color_place = np.where(green_color)
    return green_color_place


def get_green_pixels_coords(image):
    green_color_place = find_green_pixels(image)
    calculate_coordinates_v = np.vectorize(calculate_pixel_coords)
    image_width = image.size[0]
    x, y = calculate_coordinates_v(green_color_place, image_width)
    return x, y


def find_frame_corners_coords(image):
    x, y = get_green_pixels_coords(image)
    coordinates = list(zip(x[0], y[0]))
    x_avg, y_avg = np.average(x), np.average(y)
    top_left = [c for c in coordinates if c[0] < x_avg and c[1] < y_avg][0]
    top_right = [c for c in coordinates if c[0] > x_avg and c[1] < y_avg][0]
    bottom_left = [c for c in coordinates if c[0] < x_avg and c[1] > y_avg][0]
    bottom_right = [c for c in coordinates if c[0] > x_avg and c[1] > y_avg][0]
    frame_coords = [top_left, top_right, bottom_left, bottom_right]
    return frame_coords


def find_transform_coeffs(new_coords, old_coords):
    """
    find coefficients for image perspective transformation
    https://stackoverflow.com/questions/14177744/how-does-perspective-transformation-work-in-pil
    """
    matrix = []
    for c1, c2 in zip(new_coords, old_coords):
        matrix.append([c1[0], c1[1], 1, 0, 0, 0, -c2[0]*c1[0], -c2[0]*c1[1]])
        matrix.append([0, 0, 0, c1[0], c1[1], 1, -c2[1]*c1[0], -c2[1]*c1[1]])

    A = np.matrix(matrix, dtype=float)
    B = np.array(old_coords).reshape(8)

    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    coeffs = np.array(res).reshape(8)
    return coeffs


def calculate_new_frame_coords(old_frame_coords):
    top_left, \
    top_right, \
    bottom_left, \
    bottom_right = old_frame_coords

    frame_length = top_right[0] - top_left[0]

    top_left_new = top_left
    top_right_new = top_right[0], top_left[1]
    bottom_left_new = top_left[0], top_left[1] + frame_length
    bottom_right_new = top_right_new[0], bottom_left_new[1]

    new_frame_coords = [top_left_new, top_right_new, bottom_left_new, bottom_right_new]
    return new_frame_coords


def resize_image(image, frame_width, frame_height, frame_coords):
    """
    :param image: frame photo
    :param frame_width: real frame width, cm
    :param frame_height: real frame height, cm
    :param frame_coords: calculated frame coordinates
    :return: resized frame photo
    """

    old_frame_width = frame_coords[1][0] - frame_coords[0][0]
    old_frame_height = frame_coords[2][1] - frame_coords[0][1]
    new_frame_width = frame_width / 2.54 * 300
    new_frame_height = frame_height / 2.54 * 300

    image_width, image_height = image.size

    width_coeff = new_frame_width / old_frame_width
    height_coeff = new_frame_height / old_frame_height

    new_image_width = int(image_width * width_coeff)
    new_image_height = int(image_height * height_coeff)

    image = image.resize((new_image_width, new_image_height), Image.Resampling.LANCZOS)
    return image


def transform_image(image, frame_width, frame_height):
    old_frame_coords = find_frame_corners_coords(image)
    new_frame_coords = calculate_new_frame_coords(old_frame_coords)
    coeffs = find_transform_coeffs(new_frame_coords, old_frame_coords)
    width, height = image.size
    image = image.transform((width, height),
                            Image.Transform.PERSPECTIVE, coeffs,
                            Image.Resampling.BICUBIC)
    image = resize_image(image, frame_width, frame_height, new_frame_coords)
    return image







im = Image.open("images/251_k.tif")
im = transform_image(im, 30, 30)
im.save("images/251_k_resize_2.tif", dpi=(300, 300))