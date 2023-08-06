# distutils: language = c++

from libcpp.vector cimport vector
from libcpp.string cimport string
from libc.stdint cimport intptr_t
import numpy as np
cimport numpy as np
import ctypes
import os, sys
PYTHON_VERSION = sys.version_info[0]

if PYTHON_VERSION == 2:
    from exceptions import NotImplementedError, RuntimeError

from Exceptions.runtime import UnsupportedError

from os.path import abspath
from os.path import join as pjoin

# Metadata
__version__ = "0.0.1"
__author__ = "Disa Mhembere"
__maintainer__ = "Disa Mhembere <disa@jhu.edu>"
__package__ = "knor"

cdef extern from "kmeans_types.hpp" namespace "kpmeans::base":
    cdef cppclass kmeans_t:
        kmeans_t()
        kmeans_t(const size_t, const size_t, const size_t,
                 const size_t, const unsigned*,
                 const size_t*, const vector[double]&)
        const void write(const string dirname) const
        void set_params(const size_t nrow, const size_t ncol,
                const size_t iters, const size_t k)
        size_t nrow
        size_t ncol
        size_t iters
        size_t k
        vector[unsigned] assignments
        vector[size_t] assignment_count
        vector[double] centroids

cdef class knor_t:
    cdef kmeans_t c_kmeans_t      # hold a C++ instance which we're wrapping
    def __cinit__(self, const size_t nrow, const size_t ncol, const size_t iters,
             const size_t k, vector[unsigned]& assignments_buf,
             const vector[size_t]& assignment_count_buf,
             const vector[double]& centroids):
        self.c_kmeans_t = kmeans_t(nrow, ncol, iters, k, assignments_buf.data(),
                assignment_count_buf.data(), centroids)

    def __repr__(self):
        s = "Iterations: {}\nk: {}\nSizes:\n{}\nCentroids:\n{}\nCluster:\n{}\n"
        return s.format(self.get_iters(), self.get_k(),
                        self.get_sizes(), self.get_centroids(),
                        self.get_clusters())

    def write(self, const string dirname):
        return self.c_kmeans_t.write(dirname)

    def get_nrow(self):
        return self.c_kmeans_t.nrow

    def get_k(self):
        return self.c_kmeans_t.k

    def get_iters(self):
        return self.c_kmeans_t.iters

    def get_ncol(self):
        return self.c_kmeans_t.ncol

    def get_clusters(self):
        return np.array(self.c_kmeans_t.assignments)

    def get_sizes(self):
        return np.array(self.c_kmeans_t.assignment_count)

    def get_centroids(self):
        centroids = np.array(self.c_kmeans_t.centroids)
        return centroids.reshape(self.get_k(), self.get_ncol())

    def __richcmp__(self, other, int op):
        if op == 2: # 2 is __eq__
            if isinstance(other, self.__class__):
                return np.array_equal(self.get_clusters(),
                        other.get_clusters()) and\
                    np.array_equal(self.get_sizes(), other.get_sizes()) and\
                    np.array_equal(self.get_centroids(),
                            other.get_centroids()) and\
                    np.array_equal(self.get_iters(), other.get_iters())
            else:
                return False

    def set_params(self, const size_t nrow, const size_t ncol,
            const size_t iters, const size_t k):
        return self.c_kmeans_t.set_params(nrow, ncol, iters, k)

cdef extern from "util.hpp" namespace "kpmeans::base":
    cpdef int get_num_omp_threads()
    cpdef unsigned get_num_nodes()

cdef extern from "knori.hpp" namespace "kpmeans::base":
    kmeans_t kmeans(double* data, const size_t nrow,
        const size_t ncol, const unsigned k, size_t max_iters,
        unsigned nnodes, unsigned nthread,
        double* p_centers, string init,
        double tolerance, string dist_type,
        bint omp, bint numa_opt)

    kmeans_t kmeans(const string datafn, const size_t nrow,
        const size_t ncol, const unsigned k,
        size_t max_iters, unsigned nnodes,
        unsigned nthread, double* p_centers, string init,
        double tolerance, string dist_type, bint omp)

# Help
def build_defaults(kwargs):
    DEFAULT_ARGS = {
        "max_iters": sys.maxsize, "nnodes": get_num_nodes(),
        "nthread": get_num_omp_threads(), "p_centers": None,
        "init": "kmeanspp", "tolerance": -1, "dist_type": "eucl",
        "omp": False, "numa_opt": False, "nrow": 0, "ncol": 0}

    for k in DEFAULT_ARGS.iterkeys():
        if k not in kwargs:
            kwargs[k] = DEFAULT_ARGS[k]

def none():
    if PYTHON_VERSION == 2:
        return "none"
    else:
        return bytearray("none", "utf8")

def Kmeans(data, centers, **kwargs):
    """
    Run the k-means algorithm for data on the local file system.
    K-means provides *k* disjoint sets for a dataset using a parallel
    and fast NUMA optimized version of Lloyd's algorithm. The details
    of which are found in this paper https://arxiv.org/pdf/1606.08905.pdf.

    **Positional Arguments:**

        data:
            - Either the path to a file containing a binary row-major
            double floating point precision numpy "matrix".
        centers:
            - Either (i) The number of centers (i.e., k), or (ii) an
            In-memory data matrix (numpy.ndarray)

    **Keyword Arguments:**
        nrow:
            - The number of rows in the data
        ncol:
            - The number of columns in the data
        max_iters:
            - The maximum number of iteration of k-means to perform
            (Default: System Max)
        nthread:
            - The number of parallel thread to run (Default: # Phys Cores)
        init:
            - The type of initialization to use "kmeanspp", "random",
                "forgy", "none" (Default: "kmeanspp")
        tolerance:
            - The convergence tolerance (Default: 0)
        dist_type: What dissimilarity metric to use "eucl", "cos" (Default:
        "eucl")
        omp:
            - Use (slower) OpenMP threads rather than pthreads` for
            parallelizations.
        numa_opt:
            - When passing `data` as an in-memory data matrix you can
            optimize memory placement for Linux NUMA machines. *NOTE:*
            performance may degrade with very large data & it
            requires 2*memory of that without this.
    """

    cdef np.ndarray ndarr
    cdef kmeans_t ret
    cdef vector[double] c_centers
    cdef intptr_t addr

    build_defaults(kwargs)
    max_iters = kwargs["max_iters"]
    nnodes = kwargs["nnodes"]
    nthread = kwargs["nthread"]
    tolerance = kwargs["tolerance"]
    omp = kwargs["omp"]
    numa_opt = kwargs["numa_opt"]

    if PYTHON_VERSION == 2:
        init = kwargs["init"]
        dist_type = kwargs["dist_type"]
    else:
        init = bytearray(kwargs["init"], "utf8")
        dist_type = bytearray(kwargs["dist_type"], "utf8")

    if isinstance(data, str):
        nrow = kwargs["nrow"]
        ncol = kwargs["ncol"]

        if PYTHON_VERSION == 2:
            data = abspath(data)
        else:
            data = bytearray(abspath(data), "utf8")

        if not nrow or not ncol:
            raise RuntimeError("Data dim cannot be 0: `nrow` or `ncol`")

        # Centers computed
        if isinstance(centers, int) or isinstance(centers, long):
            ret = kmeans(data, nrow, ncol,
                    centers, max_iters, nnodes, nthread, NULL,
                    init, tolerance, dist_type, omp)

        # Centers in-memory
        elif isinstance(centers, np.ndarray):
            if np.isfortran(centers):
                centers = centers.transpose()

            for item in centers.flatten():
                c_centers.push_back(item)

            ret = kmeans(data, nrow, ncol, centers.shape[0], max_iters,
                    nnodes, nthread, &c_centers[0],
                    none(), tolerance, dist_type, omp)
        else:
            raise UnsupportedError("centers must be of type `long/int` or " +\
                "`numpy.ndarray`\n")

    elif isinstance(data, np.ndarray) and data.ndim == 2:
        # C order only
        if np.isfortran(data):
            ndarr = data.transpose()
        else:
            ndarr = data

        nrow, ncol = data.shape
        addr = ctypes.c_void_p(ndarr.ctypes.data).value

        # Centers computed
        if isinstance(centers, int) or isinstance(centers, long):
            ret = kmeans(<double*>(addr), nrow, ncol,
                    centers, max_iters, nnodes, nthread, NULL,
                    init, tolerance, dist_type, omp, numa_opt)

        # Centers in-memory
        elif isinstance(centers, np.ndarray):
            if np.isfortran(centers):
                centers = centers.transpose()

            for item in centers.flatten():
                c_centers.push_back(item)

            ret = kmeans(<double*>(addr), nrow, ncol, centers.shape[0], max_iters,
                    nnodes, nthread, &c_centers[0],
                    none(), tolerance, dist_type, omp, numa_opt)
        else:
            raise UnsupportedError("centers must be of type `long/int` or " +\
                "`numpy.ndarray`\n")
    elif isinstance(data, np.ndarray) and data.ndim != 2:
        raise RuntimeError("`data` must have 2 dimensions!")
    else:
        raise UnsupportedError("Cannot handle data of type {}".format(type(data)))

    return knor_t(ret.nrow, ret.ncol, ret.iters, ret.k, ret.assignments,
            ret.assignment_count, ret.centroids)
