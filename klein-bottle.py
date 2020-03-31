# -----------------------------------------------------------------------------
# Copyright (c) 2020 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
# This example shows tessagon usage (https://github.com/cwant/tessagon)
# -----------------------------------------------------------------------------
import numpy as np
from mpl3d import glm
from mpl3d.mesh import Mesh
from mpl3d.camera import Camera


# --- main --------------------------------------------------------------------
if __name__ == "__main__":
    from tessagon.misc.shapes import klein, torus
    from tessagon.types.hex_tessagon import HexTessagon
    from tessagon.adaptors.list_adaptor import ListAdaptor
    options = {
        'function': klein,
        'u_range': [0.0, 1.0], 'v_range': [0.0, 1.0],
        'u_num': 60,           'v_num': 10,
        'u_cyclic': True,      'v_cyclic': True,
                               'v_twist': True,
        'adaptor_class' : ListAdaptor
    }
    tessagon = HexTessagon(**options)
    mesh = tessagon.create_mesh()
    vertices = np.array(mesh["vert_list"])
    faces = mesh["face_list"]
    
    
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_axes([0,0,1,1], xlim=[-1,+1], ylim=[-1,+1], aspect=1)
    ax.axis("off")

    camera = Camera("perspective", 65, 15, scale=2)
    vertices = glm.fit_unit_cube(vertices)
    mesh = Mesh(ax, camera.transform, vertices, faces, mode="all",
                cmap=plt.get_cmap("magma"), edgecolors=(0,0,0,0.25)) 
    camera.connect(ax, mesh.update)
    plt.savefig("klein-bottle.png", dpi=300)
    plt.show()

