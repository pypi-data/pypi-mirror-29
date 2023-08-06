import math


__all__ = ['get_star_type']


def get_star_type(index, ranking):
    """Return the icon class name for the given star index and average ranking."""
    if ranking < index or (ranking == 0 and index == 0):
        return "star_border_icon"
    elif math.floor(ranking) > index or (ranking % 1 == 0 and ranking == index):
        return "star_icon"
    else:
        return "star_half_icon"
