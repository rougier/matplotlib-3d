# Experimental 3d axis for matplotlib

This experimental project is an attempt at providing a better and more
versatile 3d axis for [Matplotlib](https://matplotlib.org). The heart of the
code is explained in this blog post: [Custom 3D engine in
Matplotlib](https://matplotlib.org/matplotblog/posts/custom-3d-engine/).

> <img src="https://img.shields.io/badge/-_Warning-orange.svg?style=flat-square"/>
> 
> Note that we cannot have a full 3d engine because we do not have a proper
> [zbuffer](https://en.wikipedia.org/wiki/Z-buffering) that allows to test
> individual pixels. This means we need to sort our points/lines/triangles in
> order to draw them from back to front. Most of the time, this does the trick
> but there exist some situations where it is impossible to avoid
> problems. For example, consider two triangles that intersect each other. In
> in such a case, we have to decide arbitrarily which triangle will be drawn on
> top of the other.

[Read the documentation](doc/README.md)

![](doc/bunnies.png)

# Install

You can install by pip command.

`pip install git+https://github.com/rougier/matplotlib-3d`
