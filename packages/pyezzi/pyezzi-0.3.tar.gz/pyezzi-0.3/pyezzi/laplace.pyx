import numpy as np
cimport numpy as np
cimport cython

ctypedef np.float64_t DTYPE_FLOAT
ctypedef np.int_t DTYPE_INT

# dirty fix to get rid of annoying warnings
np.seterr(divide='ignore', invalid='ignore')

@cython.boundscheck(False)
@cython.wraparound(False)
def solve_3D(np.ndarray[DTYPE_INT, ndim=1] domain_idx_i,
             np.ndarray[DTYPE_INT, ndim=1] domain_idx_j,
             np.ndarray[DTYPE_INT, ndim=1] domain_idx_k,
             np.ndarray[DTYPE_FLOAT, ndim=3] init,
             DTYPE_FLOAT tolerance,
             DTYPE_INT max_iterations,
             np.ndarray[DTYPE_FLOAT, ndim=1] spacing):
    cdef np.ndarray[DTYPE_FLOAT, ndim=3] laplace_grid = np.copy(init)
    cdef np.ndarray[DTYPE_FLOAT, ndim=3] prev_laplace_grid = np.copy(
        laplace_grid)
    cdef DTYPE_INT iteration = 0
    cdef DTYPE_FLOAT max_error = 1.0
    cdef DTYPE_INT n_points = len(domain_idx_i)
    cdef DTYPE_INT i, j, k, n
    cdef DTYPE_FLOAT error
    cdef DTYPE_FLOAT value
    cdef DTYPE_FLOAT hi, hj, hk, hi2, hj2, hk2, factor

    hi, hj, hk = spacing
    hi2, hj2, hk2 = spacing ** 2

    factor = (hi2 * hj2 * hk2) / (2 * (hi2 * hj2 + hi2 * hk2 + hj2 * hk2))

    while max_error > tolerance and iteration < max_iterations:
        iteration += 1
        prev_laplace_grid[:] = laplace_grid
        for n in range(n_points):
            i = domain_idx_i[n]
            j = domain_idx_j[n]
            k = domain_idx_k[n]
            value = ((laplace_grid[i + 1, j, k] +
                      laplace_grid[i - 1, j, k]) / hi2 +
                     (laplace_grid[i, j + 1, k] +
                      laplace_grid[i, j - 1, k]) / hj2 +
                     (laplace_grid[i, j, k - 1] +
                      laplace_grid[i, j, k + 1]) / hk2) * factor
            laplace_grid[i, j, k] = value
        max_error = np.nanmax(
            np.abs(
                (prev_laplace_grid[domain_idx_i, domain_idx_j, domain_idx_k] -
                 laplace_grid[domain_idx_i, domain_idx_j, domain_idx_k]) /
                prev_laplace_grid[domain_idx_i, domain_idx_j, domain_idx_k]))
    return laplace_grid, iteration, max_error
