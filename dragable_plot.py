import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class MoveGraphLine(object):
    def __init__(self, ax, r0):
        self.ax = ax
        self.figcanvas = self.ax.figure.canvas
        self.x, self.y = r0
        self.moved = None
        self.point = None
        self.pressed = False
        self.start = False
        roi = patches.Circle(r0,0.1,linewidth=1, fill=None,edgecolor='r')
        self.ax.add_patch(roi)
        self.graf = roi

        self.figcanvas.mpl_connect('button_press_event', self.mouse_press)
        self.figcanvas.mpl_connect('button_release_event', self.mouse_release)
        self.figcanvas.mpl_connect('motion_notify_event', self.mouse_move)

    def mouse_release(self, event):
        if self.ax.get_navigate_mode()!= None: return
        if not event.inaxes: return
        if event.inaxes != self.ax: return
        if self.pressed: 
            self.pressed = False
            self.start = False
            self.point = None
            return

    def mouse_press(self, event):
        if self.ax.get_navigate_mode()!= None: return
        if not event.inaxes: return
        if event.inaxes != self.ax: return
        if self.start: return
        self.point = [event.xdata, event.xdata]
        self.pressed = True

    def mouse_move(self, event):
        if self.ax.get_navigate_mode()!= None: return
        if not event.inaxes: return
        if event.inaxes != self.ax: return
        if not self.pressed: return
        self.start = True

        self.x, self.y = event.xdata, event.ydata
        self.ax.patches = []
        self.graf = patches.Circle([event.xdata, event.ydata],0.1,linewidth=1, fill=None,edgecolor='r')
        self.ax.title.set_text(str(self.x))
        self.ax.add_patch(self.graf)
        self.figcanvas.draw()





fig, ax1 = plt.subplots(nrows=1, ncols=1)
roi_center = [0,0]
x0, y0 = roi_center
ax1.title.set_text(str(x0))

moveline = MoveGraphLine(ax1, (x0, y0))

plt.show()