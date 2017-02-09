PI = 3.141592654

# Color ranges
GREEN_COLOR_MIN = (45, 91, 77)
GREEN_COLOR_MAX = (61, 224, 255)
VIOLET_COLOR_MIN = (141, 89, 58)
VIOLET_COLOR_MAX = (161, 255, 255)
YELLOW_COLOR_MIN = (21, 100, 131)
YELLOW_COLOR_MAX = (30, 245, 255)


def ftoi_point(point):
    return int(point[0]), int(point[1])


def get_ellipse_size(ellipse):
    return max(ellipse[1][0], ellipse[1][1])


def ellipse_area(ellipse):
    return ellipse[1][0] * ellipse[1][1] * PI / 4


def get_pixel_size(marker):
    return get_ellipse_size(marker[1])