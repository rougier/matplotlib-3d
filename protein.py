# -----------------------------------------------------------------------------
# Copyright (c) 2020 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
# This example shows how to display a scatter plot and to manipulate colors
# based on zbuffer to suggest depth.
# -----------------------------------------------------------------------------
import numpy as np
from mpl3d import glm
from mpl3d.mesh import Mesh
from mpl3d.camera import Camera

class Scatter:

    def __init__(self, ax, transform,
                 vertices, sizes=50, facecolors="white", edgecolors="black"):

        self.vertices = vertices
        self.sizes = sizes
        self.facecolors = facecolors
        self.edgecolors = edgecolors
        self.scatter = ax.scatter([], [])
        self.outline = ax.scatter([], [], zorder=-20,
                     linewidth=2, edgecolor="black", facecolor="black")
        self.update(transform)
        
    def update(self, transform):
        vertices = glm.transform(self.vertices, transform)

        I = np.argsort(-vertices[:,2])
        vertices = vertices[I]
        facecolors = self.facecolors[I]
        edgecolors = self.edgecolors[I]
        sizes = self.sizes[I]
        self.outline.set_offsets(vertices[:,:2])
        self.outline.set_sizes(sizes)

        vertices = np.repeat(vertices,2,axis=0)
        facecolors = np.repeat(facecolors,2,axis=0)
        facecolors[::2] = 0,0,0,.1
        edgecolors = np.repeat(edgecolors,2,axis=0)
        edgecolors[::2] = 0,0,0,0
        sizes = np.repeat(sizes,2,axis=0)
        sizes[::2] *= 2

        Z = vertices[:,2]
        Z = (Z-Z.min())/(Z.max()-Z.min())
        Z = Z[::2].reshape(-1,1)
        facecolors[1::2,:3] = Z + (1-Z)*facecolors[1::2,:3]
        edgecolors[1::2,:3] = Z + (1-Z)*edgecolors[1::2,:3]
        self.scatter.set_offsets(vertices[:,:2])
        self.scatter.set_sizes(sizes)
        self.scatter.set_facecolors(facecolors)
        self.scatter.set_edgecolors(edgecolors)



# --- main --------------------------------------------------------------------
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(4,4))
    ax = fig.add_axes([0,0,1,1], xlim=[-1,+1], ylim=[-1,+1], aspect=1)
    ax.axis("off")

    P = np.load("data/protein.npy")
    V,C,S = P["position"], P["color"], P["radius"]

    FC = np.ones((len(V),4))
    FC[:,:3] = C
    EC = np.ones((len(V),4))
    EC[:] = 0,0,0,.75
    S = 100+S*300
    V = glm.fit_unit_cube(V)
    
    camera = Camera("ortho", 55, -15, scale=2)
    scatter = Scatter(ax, camera.transform, V,
                      facecolors = FC, edgecolors = EC, sizes=S)
    camera.connect(ax, scatter.update)

    plt.savefig("protein.png", dpi=600)
    plt.show()
