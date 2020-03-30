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
import meshio


# --- main --------------------------------------------------------------------
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(4,4))
    ax = fig.add_axes([0,0,1,1], xlim=[-1,+1], ylim=[-1,+1], aspect=1)
    ax.axis("off")

    camera = Camera("ortho", scale=2)
    mesh = meshio.read("data/bunny.obj")
    vertices = mesh.points
    faces = mesh.cells[0].data
    vertices = glm.fit_unit_cube(vertices)
    mesh = Mesh(ax, camera.transform, vertices, faces,
                cmap=plt.get_cmap("magma"),  edgecolors=(0,0,0,0.25))
    camera.connect(ax, mesh.update)
    plt.savefig("bunny.png", dpi=600)
    plt.show()
