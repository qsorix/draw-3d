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

    def __sub__(self, vector):
        return P(self.x - vector.x,
                 self.y - vector.y,
                 self.z - vector.z)

    def __repr__(self):
        return "({0}, {1}, {2})".format(self.x, self.y, self.z)

    def __eq__(self, other):
        if not other:
            return False

        return (abs(self.x - other.x) < 0.0001 and
                abs(self.y - other.y) < 0.0001 and
                abs(self.z - other.z) < 0.0001)

    def copy(self):
        return P(self.x, self.y, self.z)

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

    def __eq__(self, other):
        return (abs(self.x - other.x) < 0.0001 and
                abs(self.y - other.y) < 0.0001 and
                abs(self.z - other.z) < 0.0001)

    def __repr__(self):
        return "V({0}, {1}, {2})".format(self.x, self.y, self.z)

    def is_zero(self):
        return (abs(self.x) < 0.0001 and
                abs(self.y) < 0.0001 and
                abs(self.z) < 0.0001)

def reverse(v):
    return Vector(-v.x, -v.y, -v.z)

def add_vectors(u, v):
    return Vector(u.x+v.x, u.y+v.y, u.z+v.z)

def sub_vectors(u, v):
    return Vector(u.x-v.x, u.y-v.y, u.z-v.z)

class Plane:
    def __init__(self, normal, p0):
        if not normal:
            raise Exception("Plane requires normal vector")
        if not p0:
            raise Exception("Plane requires contained point")
        self.normal = normal
        self.p0 = p0

def vector_from_to(a, b):
    if not a:
        raise Exception("Missing start point")
    if not b:
        raise Exception("Missing end point")
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

def point_lies_on_plane(p, plane):
    if p == plane.p0:
        return True

    v = vector_from_to(plane.p0, p)
    d = dot(v, plane.normal)
    return abs(d) < 0.0001

def segment_lies_on_plane(seg, plane):
    return (point_lies_on_plane(seg.a, plane) and
            point_lies_on_plane(seg.b, plane))

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

def segment_segment_intersection(s1, s2):
    p1, p2, p3, p4 = s1.a, s1.b, s2.a, s2.b
    # check if segments p1-p2, and p3-p4 intersect
    # if so, return intersection point

    v12 = vector_from_to(p1, p2)
    v13 = vector_from_to(p1, p3)
    v14 = vector_from_to(p1, p4)
    v34 = vector_from_to(p3, p4)

    # if all points don't belong to the same plane, segments are skew and cannot
    # intersect
    if abs(dot(v12, cross(v13, v14))) > 0.0001:
        return None

    # if segments are parallel, they don't intersect. cases when endpoints match
    # or segments overlap are ignored

    c1234 = cross(v12, v34)

    if c1234.is_zero():
        return None

    cc = dot(c1234, c1234)

    # now find intersection of two lines, then check if intersection point
    # belongs to both segments

    ka = dot(cross(v13, v34), c1234) / cc
    kb = dot(cross(v13, v12), c1234) / cc

    if 0 <= ka <= 1 and 0 <= kb <= 1:
        return p1 + v12*ka



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

def vector_vector_projection(u, v):
    # project u onto v (in direction of v)
    l = length(v)
    if not l:
        raise Exception("direction vector is empty")
    return v * (dot(u, v) / (l*l))

def plane_containing_rays(u, v):
    normal = cross(u.v, v.v)
    return Plane(normal, u.p0)

def vector_plane_projection(u, plane):
    # project u onto plane
    return sub_vectors(u, vector_vector_projection(u, plane.normal))

def ray_plane_intersection(ray, plane):
    return vector_plane_intersection(ray.p0, ray.v, plane.p0, plane.normal)

def orthogonal_plane(plane):
    normal = Vector(plane.normal.y, plane.normal.z, plane.normal.x)
    return Plane(normal, plane.p0)

def get_axes_oriented_projection(plane, v):
    x = vector_plane_projection(Vector(1, 0, 0), plane)
    y = vector_plane_projection(Vector(0, 1, 0), plane)
    z = vector_plane_projection(Vector(0, 0, 1), plane)

    lx = length(x)
    ly = length(y)
    lz = length(z)

    vx = Vector(0,0,0)
    vz = Vector(0,0,0)
    vy = Vector(0,0,0)

    if lx:
        vx = vector_vector_projection(v, x)
    if ly:
        vy = vector_vector_projection(v, y)
    if lz:
        vz = vector_vector_projection(v, z)

    lx = length(vx)
    ly = length(vy)
    lz = length(vz)

    if lx >= ly and lx >= lz:
        return vx
    elif ly >= lx and ly >= lz:
        return vy
    else:
        return vz

def closest_point_segment_ray(segment, ray):
    """Returns a point on the segment that is closest to the ray. If the point
    falls outside of the segment, returns None as currently it is used to snap
    to segments, and we don't want to snap to segments that are too far anywa."""

    # first find closest point for infinite lines
    u = vector_from_to(segment.a, segment.b)
    p0 = segment.a

    v = ray.v
    q0 = ray.p0

    # line1 === P(s) = p0 + s*u
    # line2 === Q(t) = q0 + t*v

    w0 = vector_from_to(q0, p0)

    a = dot(u, u)
    b = dot(u, v)
    c = dot(v, v)
    d = dot(u, w0)
    e = dot(v, w0)

    delta = a*c - b*b
    if abs(delta) < 0.0001:
        return None

    # s closest, t closest
    sc = (b*e - c*d) / delta
    tc = (a*e - b*d) / delta

    # now limit the closest point to be on the segment
    if sc < 0:
        return None
    if sc > 1:
        return None

    return p0 + sc*u

def rotates_clockwise_2(v1, v2, plane):
    c = unit(cross(v1, v2))
    n = unit(plane.normal)

    result = c != n

    # if result:
    #     print("clockwise from {} to {}".format(v1, v2))
    # else:
    #     print("anti-clockwise from {} to {}".format(v1, v2))
    return result

def rotates_clockwise_3(v1, v2, v3, plane):
    c12 = rotates_clockwise_2(v1, v2, plane)
    c23 = rotates_clockwise_2(v2, v3, plane)
    c31 = rotates_clockwise_2(v3, v1, plane)

    if c12 and c23:
        return True

    if c31 and c12:
        return True

    if c23 and c31:
        return True

    return False
