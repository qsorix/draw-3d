class Tool:
    def __init__(self, wnd):
        self.wnd = wnd

    def mouseUp(self, button, pos):
        pass

    def mouseMotion(self, buttons, pos, rel):
        pass

    def deactivate(self):
        self.wnd.drawn_segments = []
        self.wnd.drawn_walls = []
        self.wnd.drawn_indicators = []

    def activate(self):
        pass
