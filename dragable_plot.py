import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class MoveGraphLine(object):
    def __init__(self, path, ax, r0, radius):
        self.path = path
        from lyse import Run
        self.run = Run(self.path)
        self.ax = ax
        self.figcanvas = self.ax.figure.canvas
        self.x, self.y = r0
        self.moved = None
        self.point = None
        self.pressed = False
        self.start = False
        self.radius = radius
        roi = patches.Circle(r0,self.radius,linewidth=1, fill=None,edgecolor='r')
        self.ax.add_patch(roi)
        self.graf = roi
        self.run.save_result('ROI', (self.x, self.y, self.radius))

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
            self.run.save_result('ROI', (self.x, self.y, self.radius))
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
        self.graf = patches.Circle([event.xdata, event.ydata],self.radius,linewidth=1, fill=None,edgecolor='r')
        self.ax.add_patch(self.graf)
        self.figcanvas.draw()
        
    def submit_radius(self, text):
        self.radius = eval(text)
        self.ax.patches = []
        self.graf = patches.Circle([self.x, self.y],self.radius,linewidth=1, fill=None,edgecolor='r')
        self.ax.add_patch(self.graf)
        self.run.save_result('ROI', (self.x, self.y, self.radius))


if __name__ == '__main__':
    fig, ax1 = plt.subplots(nrows=1, ncols=1)
    roi_center = [0,0]
    x0, y0 = roi_center
    radius = 0.1
    ax1.title.set_text(str(x0))

    moveline = MoveGraphLine(path, ax1, (x0, y0), radius)
    from matplotlib.widgets import TextBox


    axbox = plt.axes([0.7, 0.85, 0.1, 0.05])
    text_box = TextBox(axbox, 'Radius', initial='0.1')
    text_box.on_submit(moveline.submit_radius)


    plt.show()