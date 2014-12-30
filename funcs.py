import math

class P:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, vector):
        return P(self.x + vector.x,
                 self.y + vector.y,
                 self.z + vector.z)

    def __repr__(self):
        return "({0}, {1}, {2})".format(self.x, self.y, self.z)

    def __eq__(self, other):
        return (abs(self.x - other.x) < 0.0001 and
                abs(self.y - other.y) < 0.0001 and
                abs(self.z - other.z) < 0.0001)

class Ray:
    def __init__(self, v, p0):
        self.v = v # vector
        self.p0 = p0 # point

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, scalar):
        assert(isinstance(scalar, int) or isinstance(scalar, float))
        return Vector(self.x * scalar,
                      self.y * scalar,
                      self.z * scalar)

    __rmul__ = __mul__

class Plane:
    def __init__(self, normal, p0):
        self.normal = normal
        self.p0 = p0

def vector_from_to(a, b):
    return Vector(b.x-a.x, b.y-a.y, b.z-a.z)

def point_to_plane_distance(plane, point):
    sn = -dot(plane.normal, vector_from_to(plane.p0, point))
    return sn/length(plane.normal)

def point_lies_on_segment(seg, p):
    v1 = vector_from_to(seg.a, p)
    v2 = vector_from_to(p, seg.b)
    parallel = length(cross(v1, v2)) < 0.0001
    close = abs(length(v1)+length(v2) - length(vector_from_to(seg.a, seg.b))) < 0.0001
    return parallel and close

def unit(v):
    l = length(v)
    if l == 0:
        return Vector(0, 0, 0)
    return Vector(v.x/l, v.y/l, v.z/l)

def project_point_onto_vector(point, v0, vector):
    if length(vector) == 0:
        return None
    p = vector_from_to(v0, point)
    return v0 + unit(vector)*(dot(vector, p)/length(vector))


# distance from a segment to a point
def dist(x1,y1, x2,y2, x3,y3): # x3,y3 is the point
    px = x2-x1
    py = y2-y1

    something = px*px + py*py
    if (something == 0):
        return math.sqrt((x1-x3)*(x1-x3)+(y1-y3)*(y1-y3))

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

def cos_angle(a, b):
    return dot(a, b) / (length(a)*length(b))

def is_point_in_polygon(point, poly):
    x, y = point.x, point.y

    n = len(poly)
    inside = False

    p1x,p1y = poly[0].x, poly[0].y
    for i in range(n+1):
        p2x,p2y = poly[i % n].x, poly[i % n].y
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside


def vector_plane_intersection(l0, l, point_on_a_z_plane, N):
    # Plane:
    # (P - point_on_a_z_plane) dot N = 0

    # Line:
    # P = l0 + d*l

    dd = dot(l, N)
    if abs(dd) < 0.0001:
        return None

    d = dot(P(point_on_a_z_plane.x - l0.x,
              point_on_a_z_plane.y - l0.y,
              point_on_a_z_plane.z - l0.z), N) / dd

    p = P(d*l.x + l0.x, d*l.y + l0.y, d*l.z + l0.z)
    return p

def ray_plane_intersection(ray, plane):
    return vector_plane_intersection(ray.p0, ray.v, plane.p0, plane.normal)

def orthogonal_plane(plane):
    normal = Vector(plane.normal.y, plane.normal.z, plane.normal.x)
    return Plane(normal, plane.p0)
