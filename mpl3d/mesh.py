# -----------------------------------------------------------------------------
# Copyright (c) 2020 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np
import mpl3d.glm as glm
import matplotlib as mpl
from matplotlib.collections import PolyCollection


class Mesh():
    """
    Mesh described by vertices and faces
    """
    
    def __init__(self, ax, transform,  vertices, faces,
                 cmap=None, facecolors="white", edgecolors="black",
                 linewidths=0.5, mode="front"):
        """
        """
        
        self.collection = PolyCollection([], clip_on=False, snap=False)
        self.vertices = vertices
        self.faces = faces
        self.cmap = cmap
        self.facecolors = mpl.colors.to_rgba_array(facecolors)
        self.edgecolors = mpl.colors.to_rgba_array(edgecolors)
        self.linewidths = linewidths
        self.mode = mode
        self.update(transform)
        ax.add_collection(self.collection, autolim=False)
        
        
    def update(self, transform):
        """
        Update mesh according to transform (4x4 array)
        """
        
        T = glm.transform(self.vertices, transform)[self.faces]
        Z = -T[:,:,2].mean(axis=1)

        if self.cmap is not None:
            # Facecolors using depth buffer
            norm = mpl.colors.Normalize(vmin=Z.min(),vmax=Z.max())
            facecolors = self.cmap(norm(Z))

        else:
            facecolors = self.facecolors
        edgecolors = self.edgecolors
        linewidths = self.linewidths
        
        # Back face culling
        if self.mode == "front":
            front, back = glm.frontback(T)
            T, Z = T[front], Z[front]
            if len(facecolors) == len(self.faces):
                facecolors = facecolors[front]
            if len(edgecolors) == len(self.faces):
                edgecolors = edgecolors[front]

        # Front face culling
        elif self.mode == "back":
            front, back = glm.frontback(T)
            T, Z = T[back], Z[back]
            if len(facecolors) == len(faces):
                facecolors = facecolors[back]
            if len(edgecolor) == len(faces):
                edgecolors = edgecolors[back]

        # Separate 2d triangles from zbuffer
        triangles = T[:,:,:2]
        antialiased = linewidths > 0
        
        # Sort triangles according to z buffer
        I = np.argsort(Z)
        triangles = triangles[I,:]
        if len(facecolors) == len(I):
            facecolors = facecolors[I,:]
        if len(edgecolors) == len(I):
            edgecolors = edgecolors[I,:]

        self.collection.set_verts(triangles)
        self.collection.set_linewidths(linewidths)
        self.collection.set_facecolors(facecolors)
        self.collection.set_edgecolors(edgecolors)
        self.collection.set_antialiased(antialiased)
        
