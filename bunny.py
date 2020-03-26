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

# Simplified wavefront loader (only vertices and faces)
def obj_load(filename):
    V, Vi = [], []
    with open(filename) as f:
       for line in f.readlines():
           if line.startswith('#'): continue
           values = line.split()
           if not values: continue
           if values[0] == 'v':
               V.append([float(x) for x in values[1:4]])
           elif values[0] == 'f' :
               Vi.append([int(x) for x in values[1:4]])
    return np.array(V), np.array(Vi)-1



# --- main --------------------------------------------------------------------
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(4,4))
    ax = fig.add_axes([0,0,1,1], xlim=[-1,+1], ylim=[-1,+1], aspect=1)
    ax.axis("off")

    camera = Camera("ortho", scale=2)
    vertices, faces = obj_load("bunny.obj")
    vertices = glm.fit_unit_cube(vertices)
    mesh = Mesh(ax, camera.transform, vertices, faces,
                cmap=plt.get_cmap("magma"),  edgecolors=(0,0,0,0.25))
    camera.connect(ax, mesh.update)

    ax.text(0.5, 0.5, "Standford Bunny", transform=ax.transAxes,
            ha="center", va="center", size=32, zorder=100)
    
    plt.show()
