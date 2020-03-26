# -----------------------------------------------------------------------------
# Copyright (c) 2020 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
import mpl3d.glm as glm
from mpl3d.trackball import Trackball

class Camera():
    """
    Interactive trackball camera.

    This camera can be used for static or interactive rendering with mouse
    controlled movements. In this latter case, it is necessary to connect the
    camera to a mtplotlib axes using the `connect` method and to provide an
    update function that will be called each time an update is necessary
    relatively to the new transform.

    In any case, the camera transformation is kept in the `Camera.transform`
    variable.
    """
    
    def __init__(self, mode="perspective", theta=0, phi=0, scale=1):
        """
        mode : str
          camera mode ("ortho" or "perspective")

        theta: float
          angle around z axis (degrees)

        phi: float
          angle around x axis (degrees)

        scale: float
          scale factor

        view : array (4x4)
        """
        
        self.trackball = Trackball(theta, phi)
        self.aperture = 35
        self.aspect = 1
        self.near = 1
        self.far = 100
        self.mode = mode
        self.scale = scale
        self.zoom = 1
        self.zoom_max = 5.0
        self.zoom_min = 0.1
        self.view = glm.translate(0, 0, -3) @ glm.scale(scale)
        if mode == "ortho":
            self.proj = glm.ortho(-1,+1,-1,+1, self.near, self.far)
        else:
            self.proj = glm.perspective(
                self.aperture, self.aspect, self.near, self.far)
        self.transform = self.proj @ self.view @ self.trackball.model.T

    def connect(self, axes, update):
        """
        axes : matplotlib.Axes
           Axes where to connect this camera to

        update: function(transform)
           Function to be called with the new transform to update the scene
           (transform is a 4x4 matrix).
        """
        
        self.figure = axes.get_figure()
        self.axes = axes
        self.update = update
        self.mouse = None
        self.cidpress = self.figure.canvas.mpl_connect(
            'scroll_event', self.on_scroll)
        self.cidpress = self.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

        def format_coord(*args):
            phi = self.trackball.phi
            theta = self.trackball.theta
            return "Θ : %.1f, ɸ: %.1f" % (theta, phi)
        self.axes.format_coord = format_coord
                

        
    def on_scroll(self, event):
        """
        Scroll event for zooming in/out
        """
        if event.inaxes != self.axes:     return
        
        if event.button == "up":
            self.zoom  = max(0.9*self.zoom, self.zoom_min)
        elif event.button == "down":
            self.zoom = min(1.1*self.zoom, self.zoom_max)
        self.axes.set_xlim(-self.zoom,self.zoom)
        self.axes.set_ylim(-self.zoom,self.zoom)
        self.figure.canvas.draw()

        
    def on_press(self, event):
        """
        Press event to initiate a drag
        """
        if event.inaxes != self.axes:     return
        
        self.mouse = event.button, event.xdata, event.ydata

        
    def on_motion(self, event):
        """
        Motion event to rotate the scene
        """
        if self.mouse is None:            return
        if event.inaxes != self.axes:     return
        
        button, x, y = event.button, event.xdata, event.ydata
        dx, dy = x-self.mouse[1], y-self.mouse[2]
        self.mouse = button, x, y
        self.trackball.drag_to(x, y, dx, dy)
        self.transform = self.proj @ self.view @ self.trackball.model.T
        self.update(self.transform)
        self.figure.canvas.draw()

        
    def on_release(self, event):
        """
        End of drag event
        """
        self.mouse = None

        
    def disconnect(self):
        """
        Disconnect camera from the axes
        """
        self.figure.canvas.mpl_disconnect(self.cidpress)
        self.figure.canvas.mpl_disconnect(self.cidrelease)
        self.figure.canvas.mpl_disconnect(self.cidmotion)
