# -----------------------------------------------------------------------------
# Copyright (c) 2020 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
# This example shows tessagon usage (https://github.com/cwant/tessagon)
# -----------------------------------------------------------------------------
import numpy as np
from mpl3d import glm
from mpl3d.mesh import Mesh
from mpl3d.camera import Camera

cube = {
    "vertices":  [ [+1,+1,+1],  # A
                   [-1,+1,+1],  # B
                   [-1,-1,+1],  # C
                   [+1,-1,+1],  # D
                   [+1,-1,-1],  # E
                   [+1,+1,-1],  # F
                   [-1,+1,-1],  # G
                   [-1,-1,-1] ], # H
    "faces" :  [ [0, 1, 2, 3],   # ABCD: top face
                 [0, 3, 4, 5],   # ADEF: right face
                 [0, 5, 6, 1],   # AFGB: front face
                 [1, 6, 7, 2],   # BGHC: left face
                 [7, 4, 3, 2],   # HEDC: back face
                 [4, 7, 6, 5] ]  # EFGH: bottom face
}

class Scatter:
    def __init__(self, ax, transform, vertices, sizes, facecolors):
        self.vertices = vertices
        self.facecolors = facecolors
        self.sizes = sizes
        self.scatter = ax.scatter([], [], clip_on=False)
        self.update(transform)
        
    def update(self, transform):
        vertices = glm.transform(self.vertices, transform)
        I = np.argsort(-vertices[:,2])
        vertices = vertices[I]
        facecolors = self.facecolors[I]
        sizes = self.sizes[I]
        self.scatter.set_offsets(vertices[:,:2])
        self.scatter.set_facecolors(facecolors)
        self.scatter.set_sizes(sizes)
        self.scatter.set_antialiaseds(False)
        self.scatter.set_edgecolors("None")


# --- main --------------------------------------------------------------------
if __name__ == "__main__":
    import numpy as np
    import matplotlib as mpl
    import matplotlib.pyplot as plt

    X, Y, Z = np.mgrid[-8:8:50j, -8:8:50j, -8:8:50j]
    V = np.sin(X*Y*Z) / (X*Y*Z)
    vertices = np.zeros((X.size,3))
    vertices[:,0] = X.ravel()/16
    vertices[:,1] = Y.ravel()/16
    vertices[:,2] = Z.ravel()/16
    # Add some jitter to positions
    vertices += 0.003*np.random.normal(0,1,vertices.shape)

    V = V.ravel()
    V = (V-V.min())/(V.max()-V.min())
    
    cmap = plt.get_cmap("magma")
    norm = mpl.colors.Normalize(vmin=0,vmax=1)
    facecolors = cmap(norm(V))
    facecolors[:,3] = 0.5*V*V
    sizes = 25 + 50*V

    fig = plt.figure(figsize=(6,6))
    ax = fig.add_axes([0,0,1,1], xlim=[-1,+1], ylim=[-1,+1], aspect=1)
    ax.axis("off")

    camera = Camera("perspective", 45, 35)
    scatter = Scatter(ax, camera.transform, vertices, sizes, facecolors)
    cube = Mesh(ax, camera.transform, 
                np.array(cube["vertices"])/2,  np.array(cube["faces"]),
                facecolors="None", edgecolors=(0,0,0,.5), mode="front")

    def update(transform):
        scatter.update(transform)
        cube.update(transform)

    camera.connect(ax, update)
    plt.savefig("volume.png", dpi=300)
    plt.show()

