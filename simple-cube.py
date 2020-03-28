# -----------------------------------------------------------------------------
# Copyright (c) 2020 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
# This is the most simple example displaying a 3d cube
# -----------------------------------------------------------------------------
import numpy as np
from mpl3d import glm
from mpl3d.camera import Camera
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection


vertices =  [ [+1,+1,+1],  # A
              [-1,+1,+1],  # B
              [-1,-1,+1],  # C
              [+1,-1,+1],  # D
              [+1,-1,-1],  # E
              [+1,+1,-1],  # F
              [-1,+1,-1],  # G
              [-1,-1,-1] ] # H
faces = [ [0, 1, 2, 3],   # ABCD: top face
          [0, 3, 4, 5],   # ADEF: right face
          [0, 5, 6, 1],   # AFGB: front face
          [1, 6, 7, 2],   # BGHC: left face
          [7, 4, 3, 2],   # HEDC: back face
          [4, 7, 6, 5] ]  # EFGH: bottom face

fig = plt.figure(figsize=(6,6))
ax = fig.add_axes([0,0,1,1], xlim=[-1,1], ylim=[-1,1], aspect=1)
ax.axis("off")

camera   = Camera("perspective", 45, 35, scale=0.5)
vertices = glm.transform(vertices, camera.transform)
faces    = np.array([vertices[face] for face in faces])
index    = np.argsort(-np.mean(faces[:,:,2].squeeze(), axis=-1))
vertices = faces[index][...,:2]


collection = PolyCollection(vertices, facecolor=(1,1,1,.75), edgecolor="black")
ax.add_collection(collection)
plt.savefig("simple-cube.png", dpi=600)
plt.show()
