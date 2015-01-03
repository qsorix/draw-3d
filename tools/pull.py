from tools import Tool
import pygame
import funcs
from objects import Wall, S

class ToolPull(Tool):
    def reset(self):
        self.wall = False
        self.wall_pull_point = None
        self.length = 0
        self.deactivate()

    def deactivate(self):
        Tool.deactivate(self)
        self.wnd.select_nothing()

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

        for hole in self.wall.holes:
            points = []
            for v in hole:
                points.append(v + a)
            new_walls[0].holes.append(points)

        s = len(self.wall.vertices)
        for i in range(s):
            new_walls.append(Wall([self.wall.vertices[i],
                                   self.wall.vertices[(i+1) % s],
                                   self.wall.vertices[(i+1) % s]+a,
                                   self.wall.vertices[i]+a]))
        for hole in self.wall.holes:
            s = len(hole)
            for i in range(s):
                new_walls.append(Wall([hole[i],
                                       hole[(i+1) % s],
                                       hole[(i+1) % s]+a,
                                       hole[i]+a]))
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
        for hole in self.wall.holes:
            s = len(hole)
            for i in range(s):
                new_segments.append(S(hole[i],
                                      hole[i]+a))
                new_segments.append(S(hole[i]+a,
                                      hole[(i+1)%s]+a))
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

        # walls are created automatically when segments are added
        # but i'm not yet sure if this should be this way.
        # perhaps a tool like this should instead disable automation, since we
        # can compute the walls easily here and it won't interfere with the rest
        # of the project
        #self.wnd.walls.extend(self._shifted_walls(self.length))

        for s in self._shifted_segments(self.length):
            self.wnd.add_segment(s)
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

        if abs(self.length) > 0.0001:
            print ("faking walls at", self.length)
            self.wnd.drawn_walls = self._shifted_walls(self.length)
            self.wnd.drawn_segments = self._shifted_segments(self.length)
