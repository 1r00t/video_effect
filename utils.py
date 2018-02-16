
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


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


def hsv_to_rgb(h, s, v):
    if s == 0.0:
        v *= 255
        return [v, v, v]
    i = int(h * 6.)  # XXX assume int() truncates!
    f = (h * 6.) - i
    p, q, t = int(255 * (v * (1. - s))), int(255 * (v * (1. - s * f))), int(255 * (v * (1. - s * (1. - f))))
    v *= 255
    i %= 6
    if i == 0:
        return [v, t, p]
    if i == 1:
        return [q, v, p]
    if i == 2:
        return [p, v, t]
    if i == 3:
        return [p, q, v]
    if i == 4:
        return [t, p, v]
    if i == 5:
        return [v, p, q]


def get_colors(count):
    colors = []
    for i in range(0, 360, 360 // count):
        colors.append(hsv_to_rgb(i / 360, 1, 1))
    colors.reverse()
    return colors
