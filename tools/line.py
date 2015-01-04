from tools import Tool
import pygame
from colors import *
from objects import S
import funcs
from funcs import vector_from_to, P

class Snap:
    def __init__(self):
        self.color = black
        self.segments = []
        self.indicators = []

class ToolLine(Tool):
    def reset(self):
        self.segment_start = None
        self.segment_end = None
        self.deactivate()

    def _can_snap_to(self, mx, my, p):
        wnd = self.wnd
        tolerance = 8
        a = wnd._project(p)
        if a:
            x0, y0 = wnd._to_zero(a)
            if abs(x0-mx) < tolerance and abs(y0-my) < tolerance:
                return p

    def _snap_to_axis(self, start, mx, my):
        tolerance = 10
        view_direction = self.wnd.get_view_ray(mx, my)

        P1 = self.wnd.pick_plane_facing_camera()
        P2 = self.wnd.pick_plane_not_facing_camera()
        P1.p0 = start
        P2.p0 = start

        end1 = funcs.ray_plane_intersection(view_direction, P1)
        end2 = funcs.ray_plane_intersection(view_direction, P2)

        points = []
        if end1:
            points.extend([
                    (P(end1.x, start.y, start.z),red),
                    (P(start.x, end1.y, start.z),blue),
                    (P(start.x, start.y, end1.z),green),
                ])

        if end2:
            points.extend([
                (P(end2.x, start.y, start.z),red),
                (P(start.x, end2.y, start.z),blue),
                (P(start.x, start.y, end2.z),green)])

        for p, color in points:
            pp = self.wnd._project(p)
            if pp:
                x,y = self.wnd._to_zero(pp)
                if abs(x-mx) < tolerance and abs(y-my) < tolerance:
                    return self._length_snap(start, p), color

        return None, None

    def _length_snap(self, start, end):
        v = vector_from_to(start, end)
        l = funcs.length(v)
        l = round(l)
        return start + funcs.unit(v)*l

    def _free_point(self, mx, my):
        view_direction = self.wnd.get_view_ray(mx, my)

        N = self.wnd.pick_plane_facing_camera().normal

        end = funcs.vector_plane_intersection(view_direction.p0, view_direction.v, self.segment_start, N)
        end = self._length_snap(self.segment_start, end)
        return end

    def activate(self):
        pygame.mouse.set_cursor((8, 8), (4, 4), (24, 24, 24, 231, 231, 24, 24, 24), (0, 0, 0, 0, 0, 0, 0, 0))

    def mouseUp(self, button, pos):
        wnd = self.wnd
        mx, my = pos

        if not self.segment_start:
            points = self.wnd.get_objects_pointed_at(mx, my, "psw")
            if points:
                self.segment_start = points[0][1]

        else:
            self.wnd.drawn_segments = []
            self.wnd.add_segment(S(self.segment_start, self.segment_end))
            self.segment_start = None
            self.segment_end = None

    def _get_end(self, pos):
        snap = Snap()
        mx, my = pos
        axis_snap = False
        end = None

        if not end:
            end, c = self._snap_to_axis(self.segment_start, mx, my)
            if end:
                axis_snap = True
                snap.color = c

                normal_plane = funcs.Plane(vector_from_to(end, self.segment_start),
                                           end)

                draw_dir = vector_from_to(self.segment_start, end)

                min_snap_distance = False
                for p in self.wnd.points_iter():
                    pp = funcs.project_point_onto_vector(p, self.segment_start, draw_dir)
                    if not pp:
                        continue

                    if self._can_snap_to(mx, my, pp):
                        snap_distance = funcs.length(vector_from_to(pp, p))
                        if not min_snap_distance or min_snap_distance > snap_distance:
                            min_snap_distance = snap_distance
                        
                            end = pp
                            snap.segments.append(S(end, p, gray))


        if not end:
            points = self.wnd.get_objects_pointed_at(mx, my, "psw")
            if points:
                end = points[0][1]
                snap.color = purple
                snap.indicators = [points[0][1]]

        if not end:
            end = self._free_point(mx, my)
            snap.indicators = [end]

        return end, snap

    def mouseMotion(self, buttons, pos, rel):
        mx, my = pos

        if not self.segment_start:
            points = self.wnd.get_objects_pointed_at(mx, my, "psw")
            if points:
                self.wnd.drawn_indicators = [points[0][1]]
            else:
                self.wnd.drawn_indicators = []
            return

        self.segment_end, snap = self._get_end(pos)

        if self.segment_start and self.segment_end:
            self.wnd.drawn_segments = [S(self.segment_start, self.segment_end, snap.color)]
            self.wnd.drawn_segments.extend(snap.segments)
            self.wnd.drawn_indicators = snap.indicators

            self.wnd.set_text("{0:.2f} cm".format(funcs.length(vector_from_to(self.segment_start,
                                                                     self.segment_end))))
