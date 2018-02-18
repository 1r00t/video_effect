import colorsys


def rescale(value, in_min, in_max, out_min, out_max):
    """
    Maps an input value in a given range (in_min, in_max)
    to an output range (out_min, out_max) and returns it as float.
    usage:
        >>> rescale(20, 10, 30, 0, 100)
        <<< 50.0
    """

    in_range = in_max - in_min
    out_range = out_max - out_min

    return (value - in_min) * (out_range / in_range) + out_min


def generate_palette(count):
    colors = []
    for i in range(0, 360, 360 // count):
        rgb = colorsys.hsv_to_rgb(i / 360, 1, 1)
        colors.append([int(255*i) for i in rgb])
    colors.reverse()

    return colors
