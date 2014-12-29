import math

def dist(x1,y1, x2,y2, x3,y3): # x3,y3 is the point
    px = x2-x1
    py = y2-y1

    something = px*px + py*py

    u =  ((x3 - x1) * px + (y3 - y1) * py) / float(something)

    if u > 1:
        u = 1
    elif u < 0:
        u = 0

    x = x1 + u * px
    y = y1 + u * py

    dx = x - x3
    dy = y - y3

    # Note: If the actual distance does not matter,
    # if you only want to compare what this function
    # returns to other results of this function, you
    # can just return the squared distance instead
    # (i.e. remove the sqrt) to gain a little performance

    dist = math.sqrt(dx*dx + dy*dy)

    return dist

def rotate(x, y, z, alpha, beta):
    cos = math.cos
    sin = math.sin

    xr = x * cos(alpha) - z * sin(alpha)
    yr = y
    zr = x * sin(alpha) + z * cos(alpha)

    x, y, z = xr, yr, zr

    xr = x
    yr = z * sin(beta) + y * cos(beta)
    zr = z * cos(beta) - y * sin(beta)

    x, y, z = xr, yr, zr

    return x, y, z

def unrotate(x, y, z, alpha, beta):
    alpha = -alpha
    beta = -beta
    cos = math.cos
    sin = math.sin

    xr = x
    yr = z * sin(beta) + y * cos(beta)
    zr = z * cos(beta) - y * sin(beta)

    x, y, z = xr, yr, zr

    xr = x * cos(alpha) - z * sin(alpha)
    yr = y
    zr = x * sin(alpha) + z * cos(alpha)

    x, y, z = xr, yr, zr

    return x, y, z

def dot(a, b):
    return a.x*b.x + a.y*b.y + a.z*b.z
