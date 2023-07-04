from math import sqrt

def distance(x1 : float, y1 : float, x2 : float, y2 : float) -> float:
    """ Calculate euclidean distance between two points """
    distance = sqrt ((x2-x1)**2) + ((y2-y1)**2)
    return distance

def calculate_ratio(heart_length: float, thorax_length: float) -> float:
    """ Calculate ratio between heart and thorax """
    print("TODO: calculate_ratio")
    return 0