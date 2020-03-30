# -----------------------------------------------------------------------------
# Copyright (c) 2020 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
# This example shows how to have multiviews in 3d (with one interactive)
# -----------------------------------------------------------------------------
import numpy as np
from mpl3d import glm
from mpl3d.mesh import Mesh
from mpl3d.camera import Camera
import meshio


def subplot(index):
    ax = plt.subplot(index, xlim=[-1,1], ylim=[-1,1], aspect=1)
    ax.set_axisbelow(True)
    ax.set_xticks(np.linspace(-1,1,11,endpoint=True)[1:-1])
    ax.set_yticks(np.linspace(-1,1,11,endpoint=True)[1:-1])
    ax.grid(True)
    for tick in ax.xaxis.get_major_ticks():
        tick.tick1line.set_visible(False)
        tick.label.set_visible(False)
    for tick in ax.yaxis.get_major_ticks():
        tick.tick1line.set_visible(False)
        tick.label.set_visible(False)
    return ax


# --- main --------------------------------------------------------------------
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    white = (1.0, 1.0, 1.0, 0.8)
    black = (0.0, 0.0, 0.0, 1.0)

    fig = plt.figure(figsize=(8,8))

    # Model loading
    mesh = meshio.read("data/bunny.obj")
    vertices = mesh.points
    faces = mesh.cells[0].data
    
    ax = subplot(221)
    ax.axis("off")
    camera = Camera("perspective",  -20, 0, 1.5)
    mesh = Mesh(ax, camera.transform, vertices, faces, linewidths=.5,
                cmap=plt.get_cmap("magma"), edgecolors=(0,0,0,0.25))
    camera.connect(ax, mesh.update)

    ortho = glm.ortho(-1,+1,-1,+1, 1, 100) @ glm.scale(2)
    
    ax = subplot(222)
    camera = ortho @ glm.xrotate(90)
    mesh = Mesh(ax, camera, vertices, faces,
                facecolors=white,  edgecolors=black, linewidths=.25)
    ax.text(.99, .99, "Orthographic (XZ)",
            transform=ax.transAxes, ha="right", va="top")

    ax = subplot(223)
    camera = ortho @ glm.yrotate(90)
    mesh = Mesh(ax, camera, vertices, faces,
                facecolors=white,  edgecolors=black, linewidths=.25)
    ax.text(.99, .99, "Orthographic (XY)",
            transform=ax.transAxes, ha="right", va="top")

    ax = subplot(224)
    camera = ortho
    mesh = Mesh(ax, camera, vertices, faces,
                facecolors=white,  edgecolors=black, linewidths=.25)
    ax.text(.99, .99, "Orthographic (ZY)",
            transform=ax.transAxes, ha="right", va="top")

plt.tight_layout()
plt.savefig("bunnies.png", dpi=600)
plt.show()
