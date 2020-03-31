# -----------------------------------------------------------------------------
# Copyright (c) 2020 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
# This example shows how to render bars
# -----------------------------------------------------------------------------
from mpl3d import glm
from mpl3d.camera import Camera
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

        
class Bar:
    """ Bar (histogram) """
    
    def __init__(self, ax, transform,  Z, 
                 facecolors="white", edgecolors="black",  linewidth=0, clip=False):
        """ """
        
        self.Z = Z 
        if isinstance(facecolors, np.ndarray):
            shape = facecolors.shape
            facecolors = facecolors.reshape(-1,shape[-1])
            facecolors = mpl.colors.to_rgba_array(facecolors)
            self.facecolors = facecolors.reshape(shape[0], shape[1], 4)
        else:
            shape = Z.shape
            self.facecolors = np.zeros((shape[0], shape[1], 4))
            self.facecolors[...] = mpl.colors.to_rgba(facecolors)

        if isinstance(edgecolors, np.ndarray):
            shape = edgecolors.shape
            edgecolors = edgecolors.reshape(-1,shape[-1])
            edgecolors = mpl.colors.to_rgba_array(edgecolors)
            self.edgecolors = edgecolors.reshape(shape[0], shape[1], 4)
        else: 
            shape = Z.shape
            self.edgecolors = np.zeros((shape[0], shape[1], 4))
            self.edgecolors[...] = mpl.colors.to_rgba(edgecolors)

        self.linewidth = linewidth
        self.xlim = -0.5, +0.50
        self.ylim = -0.5, +0.50
        self.zlim = -0.5, +0.50
        self.clip = clip

        # Because all the bars have the same orientation, we can use a hack to
        # shade each face at once instead of computing individual face lighting.
        self.shade = np.array([[1.00, 1.00, 0.75, 1.00, 0.50, 1.00]])
        
        self.collection = PolyCollection([], clip_on=self.clip, snap=False)
        self.update(transform)
        ax.add_collection(self.collection, autolim=False)

        
    def update(self, transform):
        """ """

        Z = self.Z
        xmin, xmax = self.xlim
        ymin, ymax = self.ylim
        zmin, zmax = self.zlim
        dx, dy = 0.5 * 1/Z.shape[0], 0.5 * 1/Z.shape[1]
        
        # Each bar is described by 8 vertices and 6 faces
        V = np.zeros((Z.shape[0], Z.shape[1], 8, 3))
        F = np.zeros((Z.shape[0], Z.shape[1], 6, 4), dtype=int)

        # Face and edge colors for the six faces
        FC = np.zeros((Z.shape[0], Z.shape[1], 6, 4))
        FC[:,:] = self.facecolors.reshape(Z.shape[0], Z.shape[1], 1, 4)
        FC *= self.shade.T
        FC[:,:,:,3] = 1
        
        EC = np.zeros((Z.shape[0], Z.shape[1], 6, 4))
        EC[:,:] = self.edgecolors.reshape(Z.shape[0], Z.shape[1], 1, 4)

        
        # Build vertices
        X,Y = np.meshgrid(np.linspace(xmin, xmax, Z.shape[0]),
                          np.linspace(ymin, ymax, Z.shape[1]))
        V[...,0] = X.reshape(Z.shape[0], Z.shape[1],1)
        V[...,1] = Y.reshape(Z.shape[0], Z.shape[1],1)
        
        V[:,:,0] += [+dx, +dy, zmin]
        V[:,:,1] += [+dx, -dy, zmin]
        V[:,:,2] += [-dx, -dy, zmin]
        V[:,:,3] += [-dx, +dy, zmin]
        
        V[:,:,4] += [+dx, +dy, zmin]
        V[:,:,5] += [+dx, -dy, zmin]
        V[:,:,6] += [-dx, -dy, zmin]
        V[:,:,7] += [-dx, +dy, zmin]
        V[:,:,4:,2] += Z.reshape(Z.shape[0], Z.shape[1],1)

        # Build faces
        I = 8*np.arange(Z.shape[0]*Z.shape[1])
        F[:,:] = I.reshape(Z.shape[0], Z.shape[1], 1, 1)
        F[:,:] +=  [ [0, 1, 2, 3], # -Z
                     [0, 1, 5, 4], # +X
                     [2, 3, 7, 6], # -X
                     [1, 2, 6, 5], # -Y
                     [0, 3, 7, 4], # +Y
                     [4, 5, 6, 7]] # +Z

        # Actual transformation
        V = V.reshape(-1,3)
        V = glm.transform(V[F], transform) #[...,:2]

        # Depth computation
        # We combine the global "depth" of the bar (depth of the bottom face)
        # and the local depth of each face. This trick avoids problems when
        # sorting all the different faces.
        Z1 = (V[:,:,0,:,2].mean(axis=2)).reshape(Z.shape[0], Z.shape[1],1)
        Z2 = (V[...,2].mean(axis=3) + 10*Z1).ravel()

        # Sorting
        I = np.argsort(-Z2)
        V = (V[...,:2].reshape(Z.shape[0]*Z.shape[1]*6, 4, 2))
        
        self.collection.set_verts(V[I])
        self.collection.set_facecolors(FC.reshape(-1,4)[I])
        self.collection.set_edgecolors(EC.reshape(-1,4)[I])
        self.collection.set_linewidths(self.linewidth)
        if self.linewidth == 0.0:
            self.collection.set_antialiased(False)
        else:
            self.collection.set_antialiased(True)

        
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import imageio

    from matplotlib.patches import Circle
    

    Z = imageio.imread("data/island.png")[::10,::10,0]
    Z = (Z-Z.min())/(Z.max()-Z.min())
    Z += 0.05*np.random.uniform(0, 1, Z.shape)
    Z = 0.25*Z*Z
    
    cmap = plt.get_cmap("Reds")
    norm = mpl.colors.Normalize(vmin=Z.min(),vmax=Z.max())
    facecolors = cmap(norm(Z))
    
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_axes([0,0,1,1], xlim=[-1,+1], ylim=[-1,0], aspect=1)
    ax.axis("off")
    
    camera = Camera("perspective", 65, -125)
    bars = Bar(ax, camera.transform, Z, facecolors=facecolors)
    camera.connect(ax, bars.update)

    plt.savefig("bar.png", dpi=300)
    plt.show()
