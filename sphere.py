# -----------------------------------------------------------------------------
# Copyright (c) 2020 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
# This example shows how to use lighting
# -----------------------------------------------------------------------------
import numpy as np
from mpl3d.mesh import Mesh
from mpl3d.camera import Camera
from mpl3d.lighting import lighting


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
    for i in range(stacks-1):
        for j in range(slices-1):
            indices.append(i*(slices) + j        )
            indices.append(i*(slices) + j+1      )
            indices.append(i*(slices) + j+slices+1)

            indices.append(i*(slices) + j+slices+1)
            indices.append(i*(slices) + j+slices  )
            indices.append(i*(slices) + j        )

    indices = np.array(indices)
    indices = indices.reshape(len(indices)//3,3)
    return vertices, indices


# --- main --------------------------------------------------------------------
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(4,4))
    ax = fig.add_axes([0,0,1,1], xlim=[-1,+1], ylim=[-1,+1], aspect=1)
    ax.axis("off")

    camera = Camera("perspective", -35, 60)
    vertices, faces = sphere(0.75, 128, 128)
    facecolors = lighting(vertices[faces], (-1,1,1), (1,0,0), True)
    mesh = Mesh(ax, camera.transform, vertices, faces,
                facecolors=facecolors, linewidths=0)
    camera.connect(ax, mesh.update)
    plt.show()

