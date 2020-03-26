# -----------------------------------------------------------------------------
# Copyright (c) 2020 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
# This example shows how to interact with the mouse:
#  - Click and drag to change view point
#  - Scroll up/down for zooming in/out
# -----------------------------------------------------------------------------
import numpy as np
from mpl3d import glm
from mpl3d.camera import Camera

class Cube():
    """ A simple cube """
    
    def __init__(self, ax, transform):
        self.vertices = np.array(
            [ [+1,+1,+1], [-1,+1,+1], [-1,-1,+1], [+1,-1,+1],
              [+1,-1,-1], [+1,+1,-1], [-1,+1,-1], [-1,-1,-1] ])/2
        self.faces = [ [0, 1, 2, 3], [0, 3, 4, 5], [0, 5, 6, 1],
                       [1, 6, 7, 2], [7, 4, 3, 2], [4, 7, 6, 5] ]
        self.collection = PolyCollection([],
                                         closed = True,
                                         linewidths = 1.0,
                                         facecolors = (1,1,1,0.75),
                                         edgecolors = (0,0,0,1))
        self.update(transform)
        ax.add_collection(self.collection, autolim=False)

    def update(self, transform):
        V = glm.transform(self.vertices, transform)
        F = np.array([V[face] for face in self.faces])
        I = np.argsort(-np.mean(F[:,:,2].squeeze(), axis=-1))
        verts = F[I][...,:2]
        self.collection.set_verts(verts)



# --- main --------------------------------------------------------------------
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection

    fig = plt.figure(figsize=(4,4))
    ax = fig.add_axes([0,0,1,1], xlim=[-1,1], ylim=[-1,1], aspect=1)
    ax.axis("off")

    camera = Camera(theta=65, phi=40)
    cube = Cube(ax, camera.transform)
    camera.connect(ax, cube.update)
    plt.show()
