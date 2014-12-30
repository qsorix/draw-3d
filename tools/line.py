from tools import Tool
import pygame
from colors import *
from objects import S
import funcs
from funcs import vector_from_to, P

class ToolLine(Tool):
    def __init__(self, wnd):
        self.wnd = wnd
        self.segment_start = None

    def _can_snap_to(self, mx, my, p):
        wnd = self.wnd
        tolerance = 8
        a = wnd._project(p)
        if a:
            x0, y0 = wnd._to_zero(a)
            if abs(x0-mx) < tolerance and abs(y0-my) < tolerance:
                return p

    def _snap_to_axis(self, mx, my):
        tolerance = 10
        view_direction = self.wnd.get_view_ray(mx, my)

        N1 = self.wnd.pick_plane_facing_camera().normal
        N2 = self.wnd.pick_plane_not_facing_camera().normal

        end1 = funcs.vector_plane_intersection(view_direction.p0, view_direction.v,
                                         self.segment_start, N1)
        end2 = funcs.vector_plane_intersection(view_direction.p0, view_direction.v,
                                         self.segment_start, N2)

        points = []
        if end1:
            points.extend([
                    (P(end1.x, self.segment_start.y, self.segment_start.z),red),
                    (P(self.segment_start.x, end1.y, self.segment_start.z),blue),
                    (P(self.segment_start.x, self.segment_start.y, end1.z),green),
                ])

        if end2:
            points.extend([
                (P(end2.x, self.segment_start.y, self.segment_start.z),red),
                (P(self.segment_start.x, end2.y, self.segment_start.z),blue),
                (P(self.segment_start.x, self.segment_start.y, end2.z),green)])

        for p, color in points:
            pp = self.wnd._project(p)
            if pp:
                x,y = self.wnd._to_zero(pp)
                if abs(x-mx) < tolerance and abs(y-my) < tolerance:
                    return p, color

        return None, None

    def _free_point(self, mx, my):
        view_direction = self.wnd.get_view_ray(mx, my)

        N = self.wnd.pick_plane_facing_camera().normal

        end = funcs.vector_plane_intersection(view_direction.p0, view_direction.v, self.segment_start, N)
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


    def mouseMotion(self, buttons, pos, rel):
        mx, my = pos

        if not self.segment_start:
            points = self.wnd.get_objects_pointed_at(mx, my, "psw")
            if points:
                self.wnd.drawn_indicators = [points[0][1]]
            return


        color = black
        axis_snap = False

        end = None
        points = self.wnd.get_objects_pointed_at(mx, my, "psw")
        if points:
            self.wnd.drawn_indicators = [points[0][1]]
            end = points[0][1]
            color = purple

        if not end:
            end, c = self._snap_to_axis(mx, my)
            if end:
                axis_snap = True
                color = c

        if not end:
            end = self._free_point(mx, my)

        if end:
            self.segment_end = end
            self.wnd.drawn_segments = [S(self.segment_start, self.segment_end,
                                         color)]

            if axis_snap:
                normal_plane = funcs.Plane(vector_from_to(self.segment_end,
                                                          self.segment_start),
                                           self.segment_end)

                draw_dir = vector_from_to(self.segment_start, self.segment_end)

                min_snap_distance = False
                for p in self.wnd.points_iter():
                    pp = funcs.project_point_onto_vector(p, self.segment_start, draw_dir)
                    if not pp:
                        continue

                    if self._can_snap_to(mx, my, pp):
                        snap_distance = funcs.length(vector_from_to(pp, p))
                        if not min_snap_distance or min_snap_distance > snap_distance:
                            min_snap_distance = snap_distance
                        
                            self.segment_end = pp
                            self.wnd.drawn_segments = [S(self.segment_start,
                                                         self.segment_end, color)]

                            self.wnd.drawn_segments.append(
                                S(self.segment_end, p, gray))

        if self.segment_start and self.segment_end:
            self.wnd.set_text("{0:.2f} cm".format(funcs.length(vector_from_to(self.segment_start,
                                                                     self.segment_end))))
