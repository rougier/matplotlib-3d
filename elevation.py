# -----------------------------------------------------------------------------
# Copyright (c) 2020 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
# This example shows how to display a mesh
# -----------------------------------------------------------------------------
import numpy as np
from mpl3d import glm
from mpl3d.mesh import Mesh
from mpl3d.camera import Camera

class Surface(Mesh):
    def __init__(self, ax, transform, Z, *args, **kwargs):
        n2, n1 = Z.shape
        X, Y = np.meshgrid(np.linspace(-0.5, +0.5, n1),
                           np.linspace(-0.5, +0.5, n2))
        vertices = np.c_[X.ravel(), Y.ravel(), Z.ravel()]
        F = (np.arange((n2-1)*(n1)).reshape(n2-1,n1))[:,:-1].T
        F = np.repeat(F.ravel(),6).reshape(n2-1,n1-1,6)
        F[:,:] += 0,n1+1,1, 0,n1,n1+1
        faces = F.reshape(-1,3)

        # Recompute colors for triangles based on vertices color
        facecolors = kwargs["facecolors"].reshape(-1,4)
        facecolors =  facecolors[faces].mean(axis=-2)
        facecolors = facecolors.reshape(-1,4)[:,:3]

        F = vertices[faces]
        # Light direction
        direction = glm.normalize([1.5,1.5,-1])
        # Faces center
        C = F.mean(axis=1)
        # Faces normal
        N = glm.normalize(np.cross(F[:,2]-F[:,0], F[:,1]-F[:,0]))
        # Relative light direction
        D = glm.normalize(C - direction)
        # Diffuse term
        diffuse = glm.clip((N*D).sum(-1).reshape(-1,1))

        facecolors = (1-diffuse)*facecolors
        kwargs["facecolors"] = facecolors
        
        Mesh.__init__(self, ax, transform, vertices, faces, *args, **kwargs)


# --- main --------------------------------------------------------------------
if __name__ == "__main__":
    import time
    import matplotlib as mpl
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(8,8))
    ax = fig.add_axes([0,0,1,1], xlim=[-1,+1], ylim=[-1,+1], aspect=1)
    ax.axis("off")

    Z = np.load("data/st-helens-after.npy")
    Z[Z==-32767.] = 2231
    stride = 2
    Z = Z[20:-20:stride, 20:-20:stride]
    Z = (Z-Z.min())/(Z.max()-Z.min())
          
    camera = Camera("perspective", 45, 45, scale=1.25)
    cmap = plt.get_cmap("viridis")
    facecolors = cmap(Z)

    start = time.time()
    surface = Surface(ax, camera.transform, 0.3*Z, mode="all",
                      facecolors=facecolors, linewidths=0)
    elapsed = time.time() - start

    text = "{0} vertices, rendered in {1:.2f} second(s) with matplotlib"
    text = text.format(Z.size, elapsed)
    ax.text(0, 0, text, va="bottom", ha="left",
            transform=ax.transAxes, size="x-small")

    plt.savefig("elevation.png", dpi=600)
    plt.show()
