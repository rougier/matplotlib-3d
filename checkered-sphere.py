# -----------------------------------------------------------------------------
# Copyright (c) 2020 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
# This example shows how to generate and display a checkered sphere
# -----------------------------------------------------------------------------
import numpy as np
from mpl3d.mesh import Mesh
from mpl3d.camera import Camera


def sphere(radius=1.0, slices=32, stacks=32):
    slices += 1
    stacks += 1
    n = slices*stacks
    vertices = np.zeros((n,3))
    theta1 = np.repeat(np.linspace(0,     np.pi, stacks, endpoint=True), slices)
    theta2 = np.tile  (np.linspace(0, 2 * np.pi, slices, endpoint=True), stacks)
    vertices[:,1] = np.sin(theta1) * np.cos(theta2) * radius
    vertices[:,2] =                  np.cos(theta1) * radius
    vertices[:,0] = np.sin(theta1) * np.sin(theta2) * radius
    indices = []
    colors = []
    for i in range(stacks-1):
        for j in range(slices-1):
            indices.append(i*(slices) + j        )
            indices.append(i*(slices) + j+1      )
            indices.append(i*(slices) + j+slices+1)
            indices.append(i*(slices) + j+slices  )
            c = (i+j) % 2
            colors.append([c,c,c,1-c*0.1])
    indices = np.array(indices).reshape(-1,4)
    return vertices, indices, np.array(colors).reshape(-1,4)


# --- main --------------------------------------------------------------------
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(4,4))
    ax = fig.add_axes([0,0,1,1], xlim=[-1,+1], ylim=[-1,+1], aspect=1)
    ax.axis("off")

    camera = Camera("perspective", 145, 35, scale=1)
    vertices, faces, facecolors = sphere(0.75)
    mesh = Mesh(ax, camera.transform, vertices, faces,
                facecolors=facecolors, edgecolors="white", mode="all")
    camera.connect(ax, mesh.update)
    plt.show()
