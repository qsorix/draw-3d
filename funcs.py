import math

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

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

def cross(a, b):
    return Vector(a.y*b.z - a.z*b.y,
                  a.z*b.x - a.x*b.z,
                  a.x*b.y - a.y*b.x)

def length(a):
    return math.sqrt(dot(a,a))

def unit(v):
    l = length(v)
    return Vector(v.x/l, v.y/l, v.z/l)


def cos_angle(a, b):
    return dot(a, b) / (length(a)*length(b))
