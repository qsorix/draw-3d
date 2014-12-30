from tools import Tool
import pygame
import funcs
from objects import Wall, S

class ToolPull(Tool):
    def __init__(self, wnd):
        self.wnd = wnd
        self.wall = False
        self.wall_pull_point = None
        self.length = 0

    def activate(self):
        self.wnd.select_nothing()
        pygame.mouse.set_cursor(*pygame.cursors.tri_right)

    def _shifted_walls(self, offset):
        new_walls = []

        a = funcs.unit(self.wall.normal())*offset

        points = []
        for v in self.wall.vertices:
            points.append(v + a)
        new_walls.append(Wall(points))

        s = len(self.wall.vertices)
        for i in range(s):
            new_walls.append(Wall([self.wall.vertices[i],
                                   self.wall.vertices[(i+1) % s],
                                   self.wall.vertices[(i+1) % s]+a,
                                   self.wall.vertices[i]+a]))
        return new_walls

    def _shifted_segments(self, offset):
        new_segments = []
        a = funcs.unit(self.wall.normal())*offset

        s = len(self.wall.vertices)
        for i in range(s):
            new_segments.append(S(self.wall.vertices[i],
                                  self.wall.vertices[i]+a))
            new_segments.append(S(self.wall.vertices[i]+a,
                                  self.wall.vertices[(i+1)%s]+a))
        return new_segments

    def _pick_wall(self, mouse_pos):
        objs = self.wnd.get_objects_pointed_at(*mouse_pos, type="w")
        if objs:
            w=objs[0][0]
            w.active = True
            self.wall = w
            self.wall_pull_point = objs[0][1]
            self.wnd.drawn_indicators = [self.wall_pull_point]

    def mouseUp(self, button, pos):
        if not self.wall:
            self._pick_wall(pos)

        if not self.length:
            return

        self.wnd.walls.extend(self._shifted_walls(self.length))
        self.wnd.segments.extend(self._shifted_segments(self.length))
        self.wnd.drawn_walls = []
        self.wnd.drawn_segments = []
        self.wall = None
        self.length = None

    def mouseMotion(self, buttons, pos, rel):
        if not self.wall:
            return

        direction = funcs.unit(self.wall.normal())

        wall_plane = self.wall.plane()
        pull_plane = self.wnd.orthogonal_plane_facing_camera(wall_plane)
        pull_plane.p0 = self.wall_pull_point

        view_ray = self.wnd.get_view_ray(*pos)
        target_point = funcs.ray_plane_intersection(view_ray, pull_plane)
        if not target_point:
            return

        target_plane = funcs.Plane(wall_plane.normal, target_point)
        
        self.length = funcs.point_to_plane_distance(target_plane,
                                                    self.wall.vertices[0])

        self.wnd.drawn_walls = self._shifted_walls(self.length)
        self.wnd.drawn_segments = self._shifted_segments(self.length)