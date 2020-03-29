# -----------------------------------------------------------------------------
# Copyright (c) 2020 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
# This example shows how to use lighting
# -----------------------------------------------------------------------------
import numpy as np
from mpl3d import glm
from mpl3d.mesh import Mesh


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


def lighting(F, direction =  (1,1,1),
             ambient_color = (1,0,0), ambient_strength = 0.2,
             diffuse_color = (1,1,1), diffuse_strength = 0.8,
             specular_color = (1,1,1), shininess = 0):

    # Faces center
    C = F.mean(axis=1)
    
    # Faces normal
    N = glm.normalize(np.cross(F[:,2]-F[:,0], F[:,1]-F[:,0]))
    
    # Relative light direction
    D = glm.normalize(C - direction)
    
    # Diffuse term
    diffuse = glm.clip((N*D).sum(-1).reshape(-1,1))

    # Specular term
    specular = 0
    if shininess: specular = np.power(diffuse, shininess)
    
    return np.minimum(1, (ambient_color*ambient_strength +
                          diffuse*diffuse_color*diffuse_strength +
                          specular*specular_color))


# --- main --------------------------------------------------------------------
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(6,6))
    ax = fig.add_axes([0,0,1,1], xlim=[-1,+1], ylim=[-1,+1], aspect=1)
    ax.axis("off")

    vertices, faces = sphere(0.25, 64, 64)
    camera = glm.ortho(-1,+1,-1,+1, 1, 100)

    ambient_color = np.array([1,0,0])
    diffuse_color = np.array([1,.25,.25])
    specular_color = np.array([1,1,1])
    
    for x, d in zip(np.linspace(-0.75, 0.75, 4), [0.00, 0.25, 0.50, 0.75]):
        diffuse_strength = d
        ambient_strength = 1-d
        for y,shininess in zip(np.linspace(0.75, -0.75, 4), [0, 16, 8, 4]):
            facecolors = lighting(vertices[faces], (1.0, 0.5, 1.5),
                                  ambient_color, ambient_strength,
                                  diffuse_color, diffuse_strength,
                                  specular_color, shininess)
            mesh = Mesh(ax, camera @ glm.translate(x,y,0.0),
                        vertices, faces, facecolors=facecolors, linewidths=0)

    plt.savefig("spheres.png", dpi=600)
    plt.show()

