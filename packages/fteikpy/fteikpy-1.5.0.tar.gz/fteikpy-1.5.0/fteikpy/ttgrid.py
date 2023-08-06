# -*- coding: utf-8 -*-

"""
Author: Keurfon Luu <keurfon.luu@mines-paristech.fr>
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from ._fteik2d import fteik2d
from ._fteik3d import fteik3d
from .ray import Ray
try:
    import cPickle as pickle
except ImportError:
    import pickle

__all__ = [ "TTGrid" ]


class TTGrid:
    """
    Traveltime grid.

    Parameters
    ----------
    grid : ndarray of shape (nz, nx[, ny]) or None, default None
        Traveltime grid.
    grid_size : tuple (dz, dx[, dy]) or None, default None
        Grid size in meters.
    source : ndarray or None, default None
        Source coordinates (Z, X[, Y]).
    zmin : int or float, default 0.
        Z axis first coordinate.
    xmin : int or float, default 0.
        X axis first coordinate.
    ymin : int or float, default 0.
        Y axis first coordinate. Only used if grid's shape is 3.
    """

    def __init__(self, grid = None, grid_size = None, source = None,
                 zmin = 0., xmin = 0., ymin = 0.):
        if grid is not None and not isinstance(grid, np.ndarray) \
            and not grid.ndim in [ 2, 3 ]:
            raise ValueError("grid must be a 2-D or 3-D ndarray")
        if grid is not None and np.any(grid < 0.):
            raise ValueError("grid must be positive")
        else:
            self._grid = grid
            if grid is not None:
                self._grid_shape = grid.shape
                self._n_dim = grid.ndim
        if grid_size is not None and len(grid_size) != len(self._grid_shape):
            raise ValueError("grid_size should be of length %d, got %d" \
                             % (len(self._grid_shape), len(grid_size)))
        if grid_size is not None and np.any(np.array(grid_size) <= 0.):
            raise ValueError("grid_size must be positive")
        else:
            self._grid_size = grid_size
        if grid is not None and len(source) != len(self._grid_shape):
            raise ValueError("source should have %d coordinates, got %d" \
                             % (len(self._grid_shape), len(source)))
        else:
            self._source = source
        if not isinstance(zmin, (int, float)):
            raise ValueError("zmin must be an integer or float")
        else:
            self._zmin = zmin
        if not isinstance(xmin, (int, float)):
            raise ValueError("xmin must be an integer or float")
        else:
            self._xmin = xmin
        if not isinstance(ymin, (int, float)):
            raise ValueError("ymin must be an integer or float")
        else:
            self._ymin = ymin
        if grid is not None and grid_size is not None:
            self._zaxis = zmin + grid_size[0] * np.arange(self._grid_shape[0])
            self._xaxis = xmin + grid_size[1] * np.arange(self._grid_shape[1])
            if grid.ndim == 3:
                self._yaxis = ymin + grid_size[2] * np.arange(self._grid_shape[2])
            else:
                self._yaxis = None
        else:
            self._zaxis = None
            self._xaxis = None
            self._yaxis = None
        return

    def get(self, zq, xq, yq = None, check = True):
        """
        Get the traveltime value given grid point coordinate.

        Parameters
        ----------
        zq : scalar
            Z coordinate of the grid point.
        xq : scalar
            X coordinate of the grid point.
        yq : scalar or None, default None
            Y coordinate of the grid point. yq should be None if grid is
            a 2-D array.
        check : bool
            Check inputs zq, xq and yq to avoid crashes when interpolating
            outside the grid (as Fortran interpolation code will try to access
            inexistent values). Disable checking if you need to call 'get'
            method a lot of times for better performance.

        Returns
        -------
        tq : scalar or ndarray
            Traveltime value(s).

        Notes
        -----
        The method uses velocity interpolation to estimate more accurate
        traveltimes (should be exact in a homogenous velocity model).
        """
        if check:
            if not isinstance(zq, (int, float)):
                raise ValueError("zq must be a scalar")
            if not isinstance(xq, (int, float)):
                raise ValueError("xq must be a scalar")
            if not self._zaxis[0] <= zq <= self._zaxis[-1]:
                raise ValueError("zq out of bounds")
            if not self._xaxis[0] <= xq <= self._xaxis[-1]:
                raise ValueError("xq out of bounds")
            if yq is not None:
                if not isinstance(yq, (int, float)):
                    raise ValueError("yq must be a scalar")
                if not self._yaxis[0] <= yq <= self._yaxis[-1]:
                    raise ValueError("yq out of bounds")

        if self._n_dim == 2:
            tq = fteik2d.interp2(self._zaxis, self._xaxis, self._grid, zq, xq)
        elif self._n_dim == 3:
            tq = fteik3d.interp3(self._zaxis, self._xaxis, self._yaxis, self._grid,
                                 zq, xq, yq)
        return tq

    def raytracer(self, receivers, ray_step = 1., max_ray = 10000, n_threads = 1):
        """
        A posteriori ray tracer.

        Parameters
        ----------
        receivers : list or ndarray
            Receivers coordinates (Z, X).
        ray_step : scalar, default 1.
            Ray stepsize (normalized).
        max_ray : int, default 1e4
            Maximum number of points to trace the ray.
        n_threads : int, default 1
            Number of threads to pass to OpenMP.

        Returns
        -------
        rays : list of Ray
            Rays from receivers to source.

        Note
        ----
        Currently only available in 2-D.
        """
        # Check inputs
        if self._n_dim == 3:
            raise ValueError("ray tracing not yet available in 3-D")
        if not isinstance(receivers, (list, tuple, np.ndarray)):
            raise ValueError("receiverss must be a list, tuple or ndarray")
        if isinstance(receivers, np.ndarray) and receivers.ndim not in [ 1, 2 ]:
            raise ValueError("receivers must be 1-D or 2-D ndarray")
        if isinstance(receivers, (list, tuple)) and len(receivers) != self._n_dim:
            raise ValueError("receivers should have %d coordinates, got %d" \
                             % (self._n_dim, len(receivers)))
        elif isinstance(receivers, np.ndarray) and receivers.ndim == 1 and len(receivers) != self._n_dim:
            raise ValueError("receivers should have %d coordinates, got %d" \
                             % (self._n_dim, len(receivers)))
        elif isinstance(receivers, np.ndarray) and receivers.ndim == 2 and receivers.shape[1] != self._n_dim:
            raise ValueError("receivers should have %d coordinates, got %d" \
                             % (self._n_dim, receivers.shape[1]))
        if not isinstance(ray_step, (int, float)) or ray_step < 0:
            raise ValueError("ray_step must be positive, got %f" % ray_step)
        if not isinstance(max_ray, int) or max_ray < 3:
            raise ValueError("max_ray must be an integer greater than 2, got %d" % max_ray)
        if not isinstance(n_threads, int) or n_threads < 1:
            raise ValueError("n_threads must be atleast 1, got %s" % n_threads)

        # Call ray tracer
        if self._n_dim == 2:
            zsrc, xsrc = self._shift(self._source)
            zrcv, xrcv = self._shift(receivers).transpose()
            dz, dx = self._grid_size
            
            if isinstance(receivers, (list, tuple)) or receivers.ndim == 1:
                self._check_2d(zsrc, xsrc)
                ray, npts = fteik2d.ray2d(self._grid, zsrc, xsrc, zrcv, xrcv,
                                          dz, dx, ray_step, max_ray)
                return Ray(z = ray[:npts,0] + self._zmin, x = ray[:npts,1] + self._xmin)
            else:
                for z, x in zip(zrcv, xrcv):
                    self._check_2d(z, x)
                rays, npts = fteik2d.raytracer2d(self._grid, zsrc, xsrc, zrcv, xrcv,
                                                 dz, dx, ray_step, max_ray, n_threads = n_threads)
                return [ Ray(z = ray[:n,0] + self._zmin, x = ray[:n,1] + self._xmin) for ray, n in zip(rays, npts) ]

    def plot(self, n_levels = 100, axes = None, figsize = (10, 8), cont_kws = {}):
        """
        Plot the traveltime grid.

        Parameters
        ----------
        n_levels : int, default 100
            Number of levels for contour.
        axes : matplotlib axes or None, default None
            Axes used for plot.
        figsize : tuple, default (8, 8)
            Figure width and height if axes is None.
        cont_kws : dict
            Keyworded arguments passed to contour plot.

        Returns
        -------
        cax : matplotlib contour
            Contour plot.
        """
        if not isinstance(n_levels, int) or n_levels < 1:
            raise ValueError("n_levels must be a positive integer")
        if axes is not None and not isinstance(axes, Axes):
            raise ValueError("axes must be Axes")
        if not isinstance(figsize, (list, tuple)) or len(figsize) != 2:
            raise ValueError("figsize must be a tuple with 2 elements")
        if not isinstance(cont_kws, dict):
            raise ValueError("cont_kws must be a dictionary")

        if self._n_dim == 2:
            if axes is None:
                fig = plt.figure(figsize = figsize, facecolor = "white")
                ax1 = fig.add_subplot(1, 1, 1)
            else:
                ax1 = axes
            cax = ax1.contour(self._xaxis, self._zaxis, self._grid, n_levels, **cont_kws)
            return cax
        else:
            raise ValueError("plot unavailable for 3-D grid")

    def save(self, filename):
        """
        Pickle the traveltime grid to a file.

        Parameters
        ----------
        filename : str
            Pickle filename.
        """
        with open(filename, "wb") as f:
            pickle.dump(self, f, protocol = pickle.HIGHEST_PROTOCOL)

    def load(self, filename):
        """
        Unpickle a traveltime grid from a file.

        Parameters
        ----------
        filename : str
            Pickle filename.
        """
        with open(filename, "rb") as f:
            tmp = pickle.load(f)
        if tmp.n_dim == 2:
            self.__init__(grid = tmp.grid,
                          grid_size = tmp.grid_size,
                          source = tmp.source,
                          zmin = tmp.zmin,
                          xmin = tmp.xmin)
        elif tmp.n_dim == 3:
            self.__init__(grid = tmp.grid,
                          grid_size = tmp.grid_size,
                          source = tmp.source,
                          zmin = tmp.zmin,
                          xmin = tmp.xmin,
                          ymin = tmp.ymin)

    def _shift(self, coord):
        if self._n_dim == 2:
            return np.array(coord) - np.array([ self._zmin, self._xmin ])
        elif self._n_dim == 3:
            return np.array(coord) - np.array([ self._zmin, self._xmin, self._ymin ])

    def _check_2d(self, z, x):
        if np.logical_or(np.any(z < self._zaxis[0]), np.any(z > self._zaxis[-1])):
            raise ValueError("z out of bounds")
        if np.logical_or(np.any(x < self._xaxis[0]), np.any(x > self._xaxis[-1])):
            raise ValueError("x out of bounds")
            
    def _check_3d(self, z, x, y):
        self._check_2d(z, x)
        if np.logical_or(np.any(y < self._yaxis[0]), np.any(y > self._yaxis[-1])):
            raise ValueError("y out of bounds")

    @property
    def grid(self):
        """
        ndarray of shape (nz, nx[, ny])
        Traveltime grid.
        """
        return self._grid

    @grid.setter
    def grid(self, value):
        self._grid = value

    @property
    def grid_shape(self):
        """
        tuple (nz, nx[, ny])
        Traveltime grid's shape.
        """
        return self._grid_shape

    @grid_shape.setter
    def grid_shape(self, value):
        self._grid_shape = value

    @property
    def grid_size(self):
        """
        tuple (dz, dx[, dy])
        Grid size in meters.
        """
        return self._grid_size

    @grid_size.setter
    def grid_size(self, value):
        self._grid_size = value

    @property
    def n_dim(self):
        """
        int (2 or 3)
        Traveltime grid's dimension.
        """
        return self._n_dim

    @n_dim.setter
    def n_dim(self, value):
        self._n_dim = value

    @property
    def source(self):
        """
        tuple of size n_dim
        Source coordinates (Z, X[, Y]).
        """
        return self._source

    @source.setter
    def source(self, value):
        self._source = value

    @property
    def zmin(self):
        """
        int or float, default 0.
        Z axis first coordinate.
        """
        return self._zmin

    @zmin.setter
    def zmin(self, value):
        self._zmin = value

    @property
    def xmin(self):
        """
        int or float, default 0.
        X axis first coordinate.
        """
        return self._xmin

    @xmin.setter
    def xmin(self, value):
        self._xmin = value

    @property
    def ymin(self):
        """
        int or float, default 0.
        Y axis first coordinate.
        """
        return self._ymin

    @ymin.setter
    def ymin(self, value):
        self._ymin = value

    @property
    def zaxis(self):
        """
        ndarray of size nz
        Z coordinates of the grid.
        """
        return self._zaxis

    @zaxis.setter
    def zaxis(self, value):
        self._zaxis = value

    @property
    def xaxis(self):
        """
        ndarray of size nx
        X coordinates of the grid.
        """
        return self._xaxis

    @xaxis.setter
    def xaxis(self, value):
        self._xaxis = value

    @property
    def yaxis(self):
        """
        ndarray of size ny
        Y coordinates of the grid.
        """
        return self._yaxis

    @yaxis.setter
    def yaxis(self, value):
        self._yaxis = value
