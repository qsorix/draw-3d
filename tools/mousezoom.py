from tools import Tool
import pygame
import funcs

class ToolMouseZoom(Tool):
    WHEELUP = 4
    WHEELDOWN = 5

    # each zoom takes you closer by this many percent
    ZOOM_SPEED = 0.04

    # in radians/pixel
    ROTATION_SPEED = 0.003

    # camera move speed. this should not be a constant actually, as it should
    # depend on the distance to visible objects
    PAN_SPEED = 0.5

    # move camera at least by this length, so it will pass through objects near
    # the screen plane
    MIN_MOVE = 1

    # by how much to move when mouse points at void
    FREE_MOVE = 10

    def reset(self):
        self._rotation_start_angle = None
        self._rotation_start_angle_vert = None
        self._rotation_point = None
        self._start_mouse_pos = None

    def _get_mouse_target(self, pos):
        objects = self.wnd.get_objects_pointed_at(*pos)
        if objects:
            destination = objects[0][1]
        else:
            view_ray = self.wnd.get_view_ray(*pos)
            destination = self.wnd.camera + view_ray.v*self.FREE_MOVE

        return destination

    def mouseDown(self, button, pos):
        if button != 2:
            return

        self._rotation_start_angle = self.wnd.camera_angle
        self._rotation_start_angle_vert = self.wnd.camera_angle_vert
        self._start_mouse_pos = pos

    def mouseMotion(self, buttons, pos, rel):
        if not self._start_mouse_pos:
            return

        dx = (pos[0] - self._start_mouse_pos[0])
        dy = (pos[1] - self._start_mouse_pos[1])

        if self.wnd.shift_down():
            self.wnd._move_camera(-self.PAN_SPEED*dx, self.PAN_SPEED*dy, 0)

        else:
            angle = self.ROTATION_SPEED * dx
            angle_vert = self.ROTATION_SPEED * dy

            self.wnd.camera_angle += angle
            self.wnd.camera_angle_vert += angle_vert

        self._start_mouse_pos = pos

    def mouseUp(self, button, pos):
        self._start_mouse_pos = None

        destination = self._get_mouse_target(pos)

        move = self.ZOOM_SPEED*funcs.vector_from_to(self.wnd.camera, destination)
        if funcs.length(move) < self.MIN_MOVE:
            move = funcs.unit(move) * self.MIN_MOVE
        if button == self.WHEELUP:
            self.wnd.camera = self.wnd.camera + move
        elif button == self.WHEELDOWN:
            self.wnd.camera = self.wnd.camera - move
