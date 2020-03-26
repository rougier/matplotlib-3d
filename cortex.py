# -----------------------------------------------------------------------------
# Copyright (c) 2020 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
# This example shows how to display a mesh using nibabel for mesh loading
# -----------------------------------------------------------------------------


# --- main --------------------------------------------------------------------
if __name__ == "__main__":
    import time
    import numpy as np
    from mpl3d import glm
    from mpl3d.mesh import Mesh
    from mpl3d.lighting import lighting
    import matplotlib.pyplot as plt
    import nibabel as nb

    
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_axes([0,0,1,1], xlim=[-1,+1], ylim=[-1,+1], aspect=1)
    ax.axis("off")

    vertices, faces = nb.freesurfer.io.read_geometry('data/lh.pial')
    vertices = glm.fit_unit_cube(vertices)
    facecolors = lighting(vertices[faces], direction=(-1,0,.25),
                          color=(1.0,0.5,0.5), specular=True)

    camera = glm.ortho(-1, +1, -1, +1, 1, 100)
    camera = camera @ glm.scale(1.9) @ glm.yrotate(90) @ glm.xrotate(270) 

    start = time.time()
    Mesh(ax, camera, vertices, faces,
         facecolors=facecolors, linewidths=0, mode="front")
    elapsed = time.time() - start

    text = "{0} vertices, {1} faces rendered in {2:.2f} second(s) with matplotlib"
    text = text.format(len(vertices), len(faces), elapsed)
    ax.text(0, 0, text, va="bottom", ha="left",
            transform=ax.transAxes, size="x-small")
    plt.savefig("cortex.png", dpi=600)
    plt.show()

