from tools import Tool
import pygame
import funcs

class ToolMouseZoom(Tool):
    WHEELUP = 4
    WHEELDOWN = 5

    # each zoom takes you closer by this many percent
    MOVESPEED = 0.04

    # move camera at least by this length, so it will pass through objects near
    # the screen plane
    MIN_MOVE = 1

    # by how much to move when mouse points at void
    FREE_MOVE = 10

    def mouseDown(self, button, pos):
        pass

    def mouseUp(self, button, pos):
        objects = self.wnd.get_objects_pointed_at(*pos)
        if objects:
            destination = objects[0][1]
        else:
            view_ray = self.wnd.get_view_ray(*pos)
            destination = self.wnd.camera + view_ray.v*self.FREE_MOVE

        move = self.MOVESPEED*funcs.vector_from_to(self.wnd.camera, destination)
        if funcs.length(move) < self.MIN_MOVE:
            move = funcs.unit(move) * self.MIN_MOVE
        if button == self.WHEELUP:
            self.wnd.camera = self.wnd.camera + move
        elif button == self.WHEELDOWN:
            self.wnd.camera = self.wnd.camera - move
