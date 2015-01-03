class Tool:
    def __init__(self, wnd):
        self.wnd = wnd
        self.reset()

    def keyDown(self, key):
        pass

    def mouseDown(self, button, pos):
        pass

    def mouseUp(self, button, pos):
        pass

    def mouseMotion(self, buttons, pos, rel):
        pass

    def deactivate(self):
        self.wnd.drawn_segments = []
        self.wnd.drawn_walls = []
        self.wnd.drawn_indicators = []
        self.wnd.plain_rects = []

    def reset(self):
        pass

    def activate(self):
        pass
