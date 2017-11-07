from math import sqrt

def scale(val, x0, x1, y0, y1, scale_type='linear'):
    normalized = (val - x0) / (x1 - x0)
    range = y1 - y0
    if scale_type == 'linear':
        z = normalized * range + y0
    elif scale_type == 'exp':
        z = (normalized ** 2) * range + y0
    elif scale_type == 'log':
        if normalized < 0:
            normalized = 0
        z = sqrt(normalized) * range + y0
    if z.is_integer():
        return int(z)
    else:
        return round(z, 2)
