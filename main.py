#!/usr/bin/env python

import pygame
import math
import funcs
from funcs import Vector, vector_from_to, P
from pygamehelper import PygameHelper

from colors import *
from tools import Tool
from tools.select import ToolSelect
from tools.rectangle import ToolRectangle
from tools.line import ToolLine
from tools.pull import ToolPull
from tools.wall import ToolWall
from tools.move import ToolMove

from objects import S, Wall

import project



def pick_plane_facing_camera(alpha, beta):
    camera = Vector(*funcs.rotate(0, 0, 1, alpha, beta))
    nx = Vector(1, 0, 0)
    ny = Vector(0, 1, 0)
    nz = Vector(0, 0, 1)

    if abs(math.cos(beta)) < 0.52:
        return funcs.Plane(ny, P(0,0,0))

    angle_x = abs(funcs.cos_angle(camera, nx))
    angle_y = abs(funcs.cos_angle(camera, ny))
    angle_z = abs(funcs.cos_angle(camera, nz))

    # cos is max for min angle
    angle_min = max(angle_x, angle_y, angle_z)
    if angle_min == angle_x:
        return funcs.Plane(nx, P(0,0,0))
    if angle_min == angle_y:
        return funcs.Plane(ny, P(0,0,0))
    if angle_min == angle_z:
        return funcs.Plane(nz, P(0,0,0))

def pick_plane_not_facing_camera(alpha, beta):
    n = pick_plane_facing_camera(alpha, beta).normal

    return funcs.Plane(Vector(n.y, n.z, n.x), P(0,0,0))

def type_score(t):
    if isinstance(t, P):
        return 0
    if isinstance(t, S):
        return 1
    return 2

def order_by_z(renderables):
    def get_z_index(r):
        max_z = 0
        if isinstance(r, S):
            max_z = max(max_z, r.a.z, r.b.z)
        elif isinstance(r, Wall):
            for v in r.vertices:
                max_z = max(max_z, v.z)
        elif isinstance(r, P):
            max_z = r.z
        return (-max_z, -type_score(r))

    renderables.sort(key=get_z_index)

def order_by_camera_distance_and_type(camera, objects):

    def camera_distance(t):
        obj, p = t
        if not p:
            raise Exception("Weird tuple passed for sorting... {0}".format(t))
        return type_score(obj) + funcs.length(vector_from_to(camera, p))

    objects.sort(key=camera_distance)




def put_cube(s, walls, x, y, z, w, c):
    s.append(S(P(x, y, z), P(x+w, y, z), c))
    s.append(S(P(x, y, z), P(x, y+w, z), c))
    s.append(S(P(x, y+w, z), P(x+w, y+w, z), c))
    s.append(S(P(x+w, y, z), P(x+w, y+w, z), c))

    s.append(S(P(x+w, y, z), P(x+w, y, z+w), c))
    s.append(S(P(x, y+w, z), P(x, y+w, z+w), c))
    s.append(S(P(x, y, z), P(x, y, z+w), c))
    s.append(S(P(x+w, y+w, z), P(x+w, y+w, z+w), c))

    s.append(S(P(x, y, z+w), P(x+w, y, z+w), c))
    s.append(S(P(x, y, z+w), P(x, y+w, z+w), c))
    s.append(S(P(x, y+w, z+w), P(x+w, y+w, z+w), c))
    s.append(S(P(x+w, y, z+w), P(x+w, y+w, z+w), c))

    walls.append(Wall([P(x, y, z),
                       P(x, y+w, z),
                       P(x+w, y+w, z),
                       P(x+w, y, z)]))

    walls.append(Wall([P(x, y, z),
                       P(x, y+w, z),
                       P(x, y+w, z+w),
                       P(x, y, z+w)]))

    walls.append(Wall([P(x, y, z),
                       P(x+w, y, z),
                       P(x+w, y, z+w),
                       P(x, y, z+w)]))

class Starter(PygameHelper):
    def __init__(self):
        self.project = project.Project()
        self.w, self.h = 800, 600
        PygameHelper.__init__(self, size=(self.w, self.h),
                              fill=((255,255,255)))
        self.font = pygame.font.SysFont('Arial', 14)
        self.text = ""

        self.D = 500 # distance eye-screen in pixels
        self.camera = P(180, 120, -180)
        self.camera_angle = -0.3
        self.camera_angle_vert = 0.1
        self.pressed = set()

        self.tool = None
        self._set_tool(ToolLine(self))

        self.segments = self.project.segments #[]
        self.drawn_segments = []
        self.drawn_indicators = []
        self.plain_rects = []
        self.walls = self.project.walls #[]
        self.drawn_walls = []
        self.drawn_axis = []

        self.drawn_axis.append(S(P(0, 0, 0), P(10000, 0, 0), red))
        self.drawn_axis.append(S(P(0, 0, 0), P(0, 10000, 0), blue))
        self.drawn_axis.append(S(P(0, 0, 0), P(0, 0, 10000), green))

        #put_cube(self.segments, self.walls, 40, 0, 40, 20, red)
        # put_cube(self.segments, self.walls, 40, 0, 40, 20, red)
        # put_cube(self.segments, self.walls, -40, 0, 40, 20, green)
        # put_cube(self.segments, self.walls, 40,  0, -40, 20, blue)
        # put_cube(self.segments, self.walls, -40,  0, -40, 20, black)
        #
        # for a in range(0,10,10):
        #     for b in range(0,10,10):
        #         self.segments.append(S(P(a, b, 1), P(a, b, 70000), green))
        #         self.segments.append(S(P(a, 1, b), P(a, 70000, b), blue))
        #         self.segments.append(S(P(1, a, b), P(70000, a, b), red))
        #
        # self.segments.append(S(P(-1, 0, 0), P(1, 0, 0)))
        # self.segments.append(S(P(0, -1, 0), P(0, 1, 0)))
        # self.segments.append(S(P(0, 0, -1), P(0, 0, 1)))

    def set_text(self, text):
        self.text = text

    def _delete_active_segments(self):
        for s in self.project.segments.copy():
            if s.active:
                self.project.del_segment(s)
        self.walls[:] = [w for w in self.walls if not w.active]

    def _set_tool(self, tool):
        if self.tool:
            self.tool.deactivate()
        self.tool = tool
        self.tool.activate()

    def _move_camera(self, side, dy, forward):
        a = self.camera_angle
        cos = math.cos
        sin = math.sin
        dx = forward * sin(a) + side * sin(a+3.14/2)
        dz = forward * cos(a) + side * cos(a+3.14/2)

        self.camera.x += dx
        self.camera.y += dy
        self.camera.z += dz

        #print ("Camera: ", self.camera.x, self.camera.y, self.camera.z)

    def _camera_transform(self, p):
        x = p.x
        y = p.y
        z = p.z
        
        xu = self.camera.x
        yu = self.camera.y
        zu = self.camera.z

        x = x - xu
        y = y - yu
        z = z - zu

        x, y, z = funcs.rotate(x, y, z,
                               self.camera_angle,
                               self.camera_angle_vert)
        return x, y, z

    def _project(self, p):
        x, y, z = self._camera_transform(p)

        if (z <= 0.0):
            return None

        return P(int(self.D/float(z)*x),
                 int(self.D/float(z)*y),
                 z)

    def _project_end(self, a, b):
        p1 = P(*self._camera_transform(a))
        p2 = P(*self._camera_transform(b))

        # p1 is in the view, p2 is behind
        # instead of p2, we'll use the point where it intersect camera's plane

        p = funcs.vector_plane_intersection(p1, vector_from_to(p1, p2),
                                      P(0,0,1), Vector(0,0,1))

        return P(int(self.D/float(p.z)*p.x),
                 int(self.D/float(p.z)*p.y),
                 p.z)

    def _project_segment(self, s):
        a = self._project(s.a)
        b = self._project(s.b)
        if (a and not b):
            b = self._project_end(s.a, s.b)
        if (b and not a):
            a = self._project_end(s.b, s.a)

        if a and b:
            ax, ay = self._to_zero(a)
            bx, by = self._to_zero(b)
            res = S(P(ax, ay, a.z), P(bx, by, b.z), color=s.color)
            res.active = s.active
            return res

    def _draw_segment(self, s):
        if not s:
            return

        if s.active:
            width=3
            pygame.draw.line(self.screen,
                             s.color,
                             (s.a.x, s.a.y),
                             (s.b.x, s.b.y),
                             width)
        else:
            pygame.draw.aaline(self.screen,
                             s.color,
                             (s.a.x, s.a.y),
                             (s.b.x, s.b.y),
                             1)

    def _project_wall(self, w):
        points = []
        for v in w.vertices:
            p = self._project(v)
            if not p:
                return
            px, py = self._to_zero(p)
            points.append(P(px, py, p.z))
        holes = []
        for hole in w.holes:
            hp = []
            for v in hole:
                p = self._project(v)
                if not p:
                    return
                px, py = self._to_zero(p)
                hp.append(P(px, py, p.z))
            holes.append(hp)
        try:
            res = Wall(points)
        except:
            return None
        res.active = w.active
        res.holes = holes
        return res

    def _pick_wall_color(self, w):
        light = funcs.unit(Vector(1, 1, -1))
        n = funcs.unit(w.normal())
        brightness = abs(funcs.dot(light, n))

        c = 130 + 90*brightness
        if w.active and w.holes:
            return (c, 150, 250)
        if w.holes:
            return (c, 180, 200)
        if w.active:
            return (c, 100, 200)
        return (c, c, c)

    def _draw_wall(self, w):
        if not w:
            return

        points = []
        for v in w.vertices:
            points.append((v.x, v.y))

        if not w.holes:
            pygame.draw.polygon(self.screen,
                                self._pick_wall_color(w),
                                points)
        else:
            holes = pygame.Surface((self.w, self.h))
            holes.fill((255, 255, 255, 0))

            pygame.draw.polygon(holes,
                                self._pick_wall_color(w),
                                points)

            for h in w.holes:
                points = []
                for v in h:
                    points.append((v.x, v.y))
                pygame.draw.polygon(holes,
                                    (255, 255, 255, 0),
                                    points)

            self.screen.blit(holes, (0, 0), None, pygame.BLEND_RGBA_MULT)

    def _draw_point(self, p):
        x0, y0 = self._to_zero(p)
        r = 2
        try:
            r = p.radius + 2
        except:
            pass
        pygame.draw.circle(self.screen, cyan, (x0, y0), r)

    def _to_zero(self, p):
        x, y = p.x, p.y;
        return [int(x + self.w/2), int(-y + self.h/2)]

    def _draw_zero(self):
        pygame.draw.line(self.screen,
                         (200, 200, 200),
                         [0, int(self.h/2)],
                         [self.w, int(self.h/2)])
        pygame.draw.line(self.screen,
                         (200, 200, 200),
                         [int(self.w/2), 0],
                         [int(self.w/2), self.h])

    def _draw_cam_pos(self):
        pygame.draw.circle(self.screen, red, (int(self.camera.x),
                                              int(self.camera.z)), 2)

    def _draw_cam_face(self):
        N = pick_plane_facing_camera(self.camera_angle,
                                     self.camera_angle_vert).normal
        if N.x:
            color = red
        if N.y:
            color = blue
        if N.z:
            color = green

        pygame.draw.circle(self.screen, color, (10, 10), 15)

    def add_segment(self, s):
        r = self.project.add_segment(s)
        print (self.segments)
        return r

    def select_nothing(self):
        for s in self.segments:
            s.active = False
        for w in self.walls:
            w.active = False


    def points_iter(self):
        for s in self.segments:
            yield s.a
            yield s.b

    def objects_iter(self):
        for s in self.segments:
            yield s
        for w in self.walls:
            yield w

    def keyDown(self, key):
        self.pressed.add(key)
        self.tool.keyDown(key)

    def keyUp(self, key):
        self.pressed.discard(key)

    def mouseDown(self, button, pos):
        self.tool.mouseDown(button, pos)

    def mouseUp(self, button, pos):
        self.tool.mouseUp(button, pos)

    def mouseMotion(self, buttons, pos, rel):
        self.tool.mouseMotion(buttons, pos, rel)

    def shift_down(self):
        if pygame.K_LSHIFT in self.pressed or pygame.K_RSHIFT in self.pressed:
            return True

    def update(self):
        if self.shift_down():
            if pygame.K_UP in self.pressed:
                self._move_camera(0, 1, 0)
            if pygame.K_DOWN in self.pressed:
                self._move_camera(0, -1, 0)
        else:
            if pygame.K_UP in self.pressed:
                self._move_camera(0, 0, 1)
            if pygame.K_DOWN in self.pressed:
                self._move_camera(0, 0, -1)

        if pygame.K_a in self.pressed:
            self.camera_angle -= 0.03
        if pygame.K_d in self.pressed:
            self.camera_angle += 0.03
        if pygame.K_s in self.pressed:
            self.camera_angle_vert += 0.03
        if pygame.K_w in self.pressed:
            self.camera_angle_vert -= 0.03

        if pygame.K_RIGHT in self.pressed:
            self._move_camera(1, 0, 0)
        if pygame.K_LEFT in self.pressed:
            self._move_camera(-1, 0, 0)

        if pygame.K_DELETE in self.pressed:
            self._delete_active_segments()

        if pygame.K_PAGEUP in self.pressed:
            self.D += 10.0
        if pygame.K_PAGEDOWN in self.pressed:
            self.D -= 10.0

        if pygame.K_f in self.pressed:
            self._set_tool(ToolWall(self))
        if pygame.K_l in self.pressed:
            self._set_tool(ToolLine(self))
        if pygame.K_m in self.pressed:
            self._set_tool(ToolMove(self))
        if pygame.K_p in self.pressed:
            self._set_tool(ToolPull(self))
        if pygame.K_r in self.pressed:
            self._set_tool(ToolRectangle(self))
        if pygame.K_SPACE in self.pressed:
            self._set_tool(ToolSelect(self))

        if pygame.K_ESCAPE in self.pressed:
            self.tool.reset()

        if pygame.K_q in self.pressed:
            self.running = False

    def draw(self):
        self.screen.fill((255,255,255))
        #self._draw_zero()
        self._draw_cam_pos()
        self._draw_cam_face()

        to_render = []

        for s in self.segments:
            s = self._project_segment(s)
            if s:
                to_render.append(s)

        for s in self.drawn_segments:
            s = self._project_segment(s)
            if s:
                to_render.append(s)

        for s in self.drawn_axis:
            s = self._project_segment(s)
            if s:
                to_render.append(s)

        for w in self.walls:
            w = self._project_wall(w)
            if w:
                to_render.append(w)

        for w in self.drawn_walls:
            w = self._project_wall(w)
            if w:
                to_render.append(w)

        for v in self.project.vertices:
            vp = self._project(v.point)
            if vp:
                vp.radius = int(0.5*len(v.neighbors))
                to_render.append(vp)

        order_by_z(to_render)

        for r in to_render:
            if isinstance(r, S):
                self._draw_segment(r)
            elif isinstance(r, Wall):
                self._draw_wall(r)
            else:
                self._draw_point(r)

        for i in self.drawn_indicators:
            ip = self._project(i)
            if ip:
                x0, y0 = self._to_zero(ip)
                pygame.draw.circle(self.screen, red, (x0, y0), 2)

        text = self.font.render(self.text, True, (0,0,0))
        self.screen.blit(text, (self.w-max(100, text.get_width()), self.h-text.get_height()))

        for r in self.plain_rects:
            pygame.draw.rect(self.screen, black, r, 1)


    def get_view_ray(self, mx, my):
        # get a ray from camera to points under mouse
        v = Vector(*self._camera_transform(P(0,0,1)))
        p = self.camera + v
        x, y, z = p.x, p.y, p.z

        D = self.D

        mx = mx - self.w/2
        my = -my + self.h/2

        x = mx*z/D
        y = my*z/D

        x, y, z = funcs.unrotate(x, y, z, self.camera_angle, self.camera_angle_vert)

        x += self.camera.x
        y += self.camera.y
        z += self.camera.z

        r_v = vector_from_to(self.camera, P(x, y, z))
        return funcs.Ray(r_v, self.camera)

    def get_objects_pointed_at(self, mx, my, type="psw"):
        view_ray = self.get_view_ray(mx, my)
        # get a ray from camera to points under mouse
        # returns a list of tuples: object, snap-point
        tolerance = 8
        result = []

        if 'p' in type:
            for p in self.points_iter():
                pp = self._project(p)
                if pp:
                    x0, y0 = self._to_zero(pp)
                    if abs(x0-mx) < tolerance and abs(y0-my) < tolerance:
                        result.append((p,p))

        if 's' in type:
            for s in self.segments:
                a = self._project(s.a)
                b = self._project(s.b)
                if a and b:
                    x0, y0 = self._to_zero(a)
                    x1, y1 = self._to_zero(b)
                    if funcs.dist(x0, y0, x1, y1, mx, my) < tolerance:
                        cp = funcs.closest_point_segment_ray(s, view_ray)
                        if cp:
                            result.append((s, cp))

        if 'w' in type:
            for w in self.walls:
                wp = self._project_wall(w)
                if wp and funcs.is_point_in_polygon(P(mx, my, 0), wp.vertices):
                    hit_hole = False
                    for hole in wp.holes:
                        if funcs.is_point_in_polygon(P(mx, my, 0), hole):
                            hit_hole = True
                            break

                    if not hit_hole:
                        p = funcs.ray_plane_intersection(view_ray, w.plane())
                        if p: # sometimes there's no p for some strange reasons. i
                              # think the wall may be broken and i get wrong plane
                              # from it
                            result.append((w, p))

        order_by_camera_distance_and_type(self.camera, result)

        return result

    def orthogonal_plane_facing_camera(self, plane):
        n1 = Vector(plane.normal.y, plane.normal.z, plane.normal.x)
        n2 = Vector(plane.normal.z, plane.normal.x, plane.normal.y)

        camera = Vector(*funcs.rotate(0, 0, 1, self.camera_angle, self.camera_angle_vert))

        a1 = abs(funcs.cos_angle(n1, camera))
        a2 = abs(funcs.cos_angle(n2, camera))

        if a1 < a2:
            normal = n1
        else:
            normal = n2

        return funcs.Plane(normal, plane.p0)

    def pick_plane_facing_camera(self):
        return pick_plane_facing_camera(self.camera_angle,
                                        self.camera_angle_vert)

    def pick_plane_not_facing_camera(self):
        return pick_plane_not_facing_camera(self.camera_angle,
                                            self.camera_angle_vert)

    def move_selected(self, vector):
        for o in self.objects_iter():
            if not o.active:
                continue

            for p in o.vertices_iter():
                p.x += vector.x
                p.y += vector.y
                p.z += vector.z

s = Starter()

s.mainLoop(30)
