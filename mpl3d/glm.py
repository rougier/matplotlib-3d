# -----------------------------------------------------------------------------
# Copyright (c) 2020 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import numpy as np


def normalize(X):
    return X/(1e-16+np.sqrt((np.array(X)**2).sum(axis=-1)))[..., np.newaxis]

def clip(V, vmin=0, vmax=1):
    return np.minimum(np.maximum(V,vmin),vmax)


def viewport(x, y, w, h, d):
    """ Viewport matrix """
    return np.array([[w/2, 0, 0, x+w/2],
                     [0, h/2, 0, y+h/2],
                     [0, 0, d/2,   d/2],
                     [0, 0, 0,       1]])


def frustum(left, right, bottom, top, znear, zfar):
    """Create view frustum

    Parameters
    ----------
    left : float
        Left coordinate of the field of view.
    right : float
        Right coordinate of the field of view.
    bottom : float
        Bottom coordinate of the field of view.
    top : float
        Top coordinate of the field of view.
    znear : float
        Near coordinate of the field of view.
    zfar : float
        Far coordinate of the field of view.

    Returns
    -------
    View frustum matrix (4x4 array)
    """

    M = np.zeros((4, 4), dtype=float)
    M[0, 0] = +2.0 * znear / (right - left)
    M[1, 1] = +2.0 * znear / (top - bottom)
    M[2, 2] = -(zfar + znear) / (zfar - znear)
    M[0, 2] = (right + left) / (right - left)
    M[2, 1] = (top + bottom) / (top - bottom)
    M[2, 3] = -2.0 * znear * zfar / (zfar - znear)
    M[3, 2] = -1.0
    return M


def perspective(fovy, aspect, znear, zfar):
    """Create perspective projection matrix

    Parameters
    ----------
    fovy : float
        The field of view along the y axis.
    aspect : float
        Aspect ratio of the view.
    znear : float
        Near coordinate of the field of view.
    zfar : float
        Far coordinate of the field of view.

    Returns
    -------
    Perspective projection matrix (4x4 array)
    """

    h = np.tan(0.5*np.radians(fovy)) * znear
    w = h * aspect
    return frustum(-w, w, -h, h, znear, zfar)


def ortho(left, right, bottom, top, znear, zfar):
    """Create orthographic projection matrix

    Parameters
    ----------
    left : float
        Left coordinate of the field of view.
    right : float
        Right coordinate of the field of view.
    bottom : float
        Bottom coordinate of the field of view.
    top : float
        Top coordinate of the field of view.
    znear : float
        Near coordinate of the field of view.
    zfar : float
        Far coordinate of the field of view.

    Returns
    -------
    Orthographic projection matrix (4x4 array)
    """

    M = np.zeros((4, 4), dtype=float)
    M[0, 0] = +2.0 / (right - left)
    M[1, 1] = +2.0 / (top - bottom)
    M[2, 2] = -2.0 / (zfar - znear)
    M[3, 3] = 1.0
    M[0, 2] = -(right + left) / float(right - left)
    M[1, 3] = -(top + bottom) / float(top - bottom)
    M[2, 3] = -(zfar + znear) / float(zfar - znear)
    return M


def scale(x=1, y=None, z=None):
    """Non-uniform scaling along the x, y, and z axes

    Parameters
    ----------
    x : float
        X coordinate of the translation vector.
    y : float | None
        Y coordinate of the translation vector. If None, `x` will be used.
    z : float | None
        Z coordinate of the translation vector. If None, `x` will be used.

    Returns
    -------
    Scaling matrix (4x4 array)
    """

    y = y or x
    z = z or x
    return np.array([[x, 0, 0, 0],
                     [0, y, 0, 0],
                     [0, 0, z, 0],
                     [0, 0, 0, 1]], dtype=float)


def translate(x=0, y=0, z=0):
    """
    Translate by an offset (x, y, z) .

    Parameters
    ----------
    x : float
        X coordinate of a translation vector.
    y : float | None
        Y coordinate of translation vector. If None, `x` will be used.
    z : float | None
        Z coordinate of translation vector. If None, `x` will be used.

    Returns
    -------
    Translation matrix (4x4 array)
    """
    
    return np.array([[1, 0, 0, x],
                     [0, 1, 0, y],
                     [0, 0, 1, z],
                     [0, 0, 0, 1]], dtype=float)


def xrotate(theta=0):
    """Rotation about the X axis

    Parameters
    ----------
    theta : float
        Specifies the angle of rotation, in degrees.

    Returns
    -------
    Rotation matrix (4x4 array)
    """

    t = np.radians(theta)
    c, s = np.cos(t), np.sin(t)
    return np.array([[1, 0,  0, 0],
                     [0, c, -s, 0],
                     [0, s,  c, 0],
                     [0, 0,  0, 1]], dtype=float)

def yrotate(theta=0):
    """Rotation about the Y axis

    Parameters
    ----------
    theta : float
        Specifies the angle of rotation, in degrees.

    Returns
    -------
    Rotation matrix (4x4 array)
    """

    t = np.radians(theta)
    c, s = np.cos(t), np.sin(t)
    return  np.array([[ c, 0, s, 0],
                      [ 0, 1, 0, 0],
                      [-s, 0, c, 0],
                      [ 0, 0, 0, 1]], dtype=float)

def zrotate(theta=0):
    """Rotation about the Z axis

    Parameters
    ----------
    theta : float
        Specifies the angle of rotation, in degrees.

    Returns
    -------
    Rotation matrix (4x4 array)
    """

    t = np.radians(theta)
    c, s = np.cos(t), np.sin(t)
    return np.array([[ c, -s, 0, 0],
                     [ s,  c, 0, 0],
                     [ 0,  0, 1, 0],
                     [ 0,  0, 0, 1]], dtype=float)

def fit_unit_cube(V):
    """ Fit vertices V into the unit cube (in place) """
    
    xmin, xmax = V[:,0].min(), V[:,0].max()
    ymin, ymax = V[:,1].min(), V[:,1].max()
    zmin, zmax = V[:,2].min(), V[:,2].max()
    scale = max([xmax-xmin, ymax-ymin, zmax-zmin])
    V /= scale
    V[:,0] -= (xmax+xmin)/2/scale
    V[:,1] -= (ymax+ymin)/2/scale
    V[:,2] -= (zmax+zmin)/2/scale
    return V

    
def transform(V, mvp, viewport=None):
    """
    Apply transform mvp to vertices V

    Parameters
    ----------
    V : (n,3) array
      Vertices array

    mvp: 4x4 array
      Transform matrix

    viewport: 4x4 array
      Viewport matrix (default is None)

    Returns
    -------
    (n,3) array of transformed vertices
    """
    
    V = np.asarray(V) 
    shape = V.shape
    V = V.reshape(-1,3)
    ones = np.ones(len(V), dtype=float)
    V = np.c_[V.astype(float), ones]      # Homogenous coordinates
    V = V @ mvp.T                         # Transformed coordinates
    if viewport is not None:
        V = V @ viewport.T
    V = V/V[:,3].reshape(-1,1)            # Normalization
    V = V[:,:3]                           # Normalized device coordinates
    return V.reshape(shape)


def frontback(T):
    """
    Sort front and back facing triangles

    Parameters:
    -----------
    T : (n,3) array
       Triangles to sort

    Returns:
    --------
    front and back facing triangles as (n1,3) and (n2,3) arrays (n1+n2=n)
    """
    Z = (T[:,1,0]-T[:,0,0])*(T[:,1,1]+T[:,0,1]) + \
        (T[:,2,0]-T[:,1,0])*(T[:,2,1]+T[:,1,1]) + \
        (T[:,0,0]-T[:,2,0])*(T[:,0,1]+T[:,2,1])
    return Z < 0, Z >= 0


def camera(xrotation=25, yrotation=45, zoom=1, mode="perspective"):
    xrotation = min(max(xrotation, 0), 90)
    yrotation = min(max(yrotation, 0), 90)
    zoom = max(0.1, zoom)
    model = scale(zoom,zoom,zoom) @ xrotate(xrotation) @ yrotate(yrotation) 
    view  = translate(0, 0, -4.5)
    if mode == "ortho":
        proj  = ortho(-1, +1, -1, +1, 1, 100)
    else:
        proj  = perspective(25, 1, 1, 100)
    return proj @ view  @ model                   
