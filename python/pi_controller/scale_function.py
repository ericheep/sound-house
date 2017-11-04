def scale(val, x0, x1, y0, y1):
    normalized = (val - x0) / (x1 - x0)
    range = y1 - y0
    z = normalized * range + y0
    if z.is_integer():
        return int(z)
    else:
        return round(z, 2)