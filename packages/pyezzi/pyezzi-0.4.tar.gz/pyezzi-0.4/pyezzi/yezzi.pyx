import numpy as np
cimport numpy as np
cimport cython
from cython.parallel import prange
from libc.math cimport fabs

ctypedef np.float64_t DTYPE_FLOAT
ctypedef np.int_t DTYPE_INT

# dirty fix to get rid of annoying warnings
np.seterr(divide='ignore', invalid='ignore')

@cython.boundscheck(False)
@cython.wraparound(False)
cdef bint has_converged(np.ndarray[DTYPE_FLOAT, ndim=1] errors,
                        DTYPE_INT n,
                        DTYPE_FLOAT tolerance):
    cdef bint res = True
    cdef DTYPE_INT i
    for i in prange(n, nogil=True):  # is prange useful here ?
        if errors[i] > tolerance:
            res = False
            break
    return res

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def iterative_relaxation_3D(np.ndarray[DTYPE_INT, ndim=1] wall_idx_i,
                            np.ndarray[DTYPE_INT, ndim=1] wall_idx_j,
                            np.ndarray[DTYPE_INT, ndim=1] wall_idx_k,
                            np.ndarray[DTYPE_FLOAT, ndim=4] vectors,
                            DTYPE_FLOAT tolerance,
                            DTYPE_INT max_iterations,
                            np.ndarray[DTYPE_FLOAT, ndim=1] spacing,
                            tuple shape):
    cdef DTYPE_FLOAT hi, hj, hk
    hi, hj, hk = spacing

    cdef np.ndarray[DTYPE_FLOAT, ndim=4] abs_vectors = np.abs(vectors)
    cdef np.ndarray[DTYPE_FLOAT, ndim=3] sum_abs_vectors = (
            abs_vectors[0] / hi
            + abs_vectors[1] / hj
            + abs_vectors[2] / hk)

    # Points of interest
    cdef DTYPE_INT n_points = len(wall_idx_i)
    cdef DTYPE_INT n_points2 = n_points * 2

    cdef np.ndarray[DTYPE_FLOAT, ndim=3] L0 = np.zeros(shape)
    cdef np.ndarray[DTYPE_FLOAT, ndim=3] L1 = np.zeros(shape)

    cdef np.ndarray[DTYPE_FLOAT, ndim=1] errors = np.zeros(n_points2,
                                                           np.float64)

    cdef bint convergence = False

    cdef DTYPE_FLOAT error = 0
    cdef DTYPE_FLOAT max_error = 1
    cdef DTYPE_INT iteration = 0

    cdef DTYPE_INT i, j, k, n, n2
    cdef DTYPE_FLOAT L0_i, L0_j, L0_k, L1_i, L1_j, L1_k, prev_L0, prev_L1
    cdef DTYPE_FLOAT L0_value, L1_value, sum_abs_vector

    while not convergence and iteration < max_iterations:
        iteration += 1
        for n in prange(n_points, nogil=True):
            i = wall_idx_i[n]
            j = wall_idx_j[n]
            k = wall_idx_k[n]
            if vectors[0, i, j, k] > 0:
                L0_i = abs_vectors[0, i, j, k] * L0[i - 1, j, k]
                L1_i = abs_vectors[0, i, j, k] * L1[i + 1, j, k]
            else:
                L0_i = abs_vectors[0, i, j, k] * L0[i + 1, j, k]
                L1_i = abs_vectors[0, i, j, k] * L1[i - 1, j, k]
            if vectors[1, i, j, k] > 0:
                L0_j = abs_vectors[1, i, j, k] * L0[i, j - 1, k]
                L1_j = abs_vectors[1, i, j, k] * L1[i, j + 1, k]
            else:
                L0_j = abs_vectors[1, i, j, k] * L0[i, j + 1, k]
                L1_j = abs_vectors[1, i, j, k] * L1[i, j - 1, k]
            if vectors[2, i, j, k] > 0:
                L0_k = abs_vectors[2, i, j, k] * L0[i, j, k - 1]
                L1_k = abs_vectors[2, i, j, k] * L1[i, j, k + 1]
            else:
                L0_k = abs_vectors[2, i, j, k] * L0[i, j, k + 1]
                L1_k = abs_vectors[2, i, j, k] * L1[i, j, k - 1]
            sum_abs_vector = sum_abs_vectors[i, j, k]
            prev_L0 = L0[i, j, k]
            prev_L1 = L1[i, j, k]
            L0_value = ((L0_i / hi
                         + L0_j / hj
                         + L0_k / hk
                         + 1)
                        / sum_abs_vector)
            L1_value = ((L1_i / hi
                         + L1_j / hj
                         + L1_k / hk
                         + 1)
                        / sum_abs_vector)
            if prev_L0 == 0:
                errors[n] = 1
            else:
                errors[n] = fabs((prev_L0 - L0_value) / prev_L0)
            n2 = n + n_points
            if prev_L1 == 0:
                errors[n2] = 1
            else:
                errors[n2] = fabs((prev_L1 - L1_value) / prev_L1)
            L0[i, j, k] = L0_value
            L1[i, j, k] = L1_value
        if iteration == 1:
            convergence = False
        else:
            convergence = has_converged(errors, n_points2, tolerance)

    return L0, L1, iteration, np.nanmax(errors)

# @cython.boundscheck(False)
# @cython.wraparound(False)
# def ordered_traversal_3D(np.ndarray wall,
#                          np.ndarray epi,
#                          np.ndarray endo,
#                          np.ndarray[DTYPE_FLOAT, ndim=3] laplace_grid,
#                          int max_iterations=-1):
#     """
#     This function should not be used for now. The implementation is slower
#     and does not allow anisotropic masks.
#
#     :param wall: A boolean 3D ndarray representing the wall that we want to
#                  maesure. Beware: wall cannot touch borders!
#     :param laplace_grid: The solution of the Laplacian equation, as returned
#                          by laplace.solve()
#     :param tolerance:
#     :param max_iterations:
#     :return:
#     """
#
#     # Boundaries
#     cdef np.ndarray inner_boundary = np.logical_and(
#         np.logical_xor(binary_dilation(endo), endo), wall)
#     cdef np.ndarray outer_boundary = np.logical_and(
#         np.logical_xor(binary_erosion(epi), epi), wall)
#     cdef np.ndarray points_to_visit = np.copy(
#         inner_boundary)
#
#     # Laplacian
#     cdef np.ndarray[DTYPE_FLOAT, ndim=4] vectors = np.array(
#         np.gradient(laplace_grid))
#     vectors /= np.sqrt(vectors[0] ** 2 + vectors[1] ** 2 + vectors[2] ** 2)
#     cdef np.ndarray[DTYPE_FLOAT, ndim=4] abs_vectors = np.abs(vectors)
#     cdef np.ndarray[DTYPE_FLOAT, ndim=3] sum_abs_vectors = abs_vectors[0] + \
#                                                            abs_vectors[1] + \
#                                                            abs_vectors[2]
#
#     # Indices
#     cdef np.ndarray[DTYPE_INT, ndim=2] wall_idx = np.argwhere(wall)
#     cdef np.ndarray[DTYPE_INT, ndim=1] wall_idx_i = wall_idx[:, 0]
#     cdef np.ndarray[DTYPE_INT, ndim=1] wall_idx_j = wall_idx[:, 1]
#     cdef np.ndarray[DTYPE_INT, ndim=1] wall_idx_k = wall_idx[:, 2]
#     cdef np.ndarray[DTYPE_INT, ndim=2] idx_to_visit
#     cdef np.ndarray[DTYPE_INT, ndim=1] idx_to_visit_i
#     cdef np.ndarray[DTYPE_INT, ndim=1] idx_to_visit_j
#     cdef np.ndarray[DTYPE_INT, ndim=1] idx_to_visit_k
#     cdef DTYPE_INT n_points = len(wall_idx)
#
#     # Visited and solved
#     cdef np.ndarray visited = np.zeros_like(
#         inner_boundary)
#     cdef np.ndarray solved = np.zeros_like(visited)
#     cdef np.ndarray neighbors = np.zeros_like(visited)
#     cdef np.ndarray unsolved_neighbors = np.zeros_like(visited)
#     cdef np.ndarray new_solved = np.zeros_like(visited)
#
#     cdef np.ndarray[DTYPE_FLOAT, ndim=3] L0 = np.zeros_like(wall, float)
#     cdef np.ndarray[DTYPE_FLOAT, ndim=3] L1 = np.zeros_like(L0)
#
#     cdef DTYPE_FLOAT L0_i, L0_j, L0_k, L1_i, L1_j, L1_k, value
#     cdef DTYPE_FLOAT min_value = float("Inf")
#     cdef DTYPE_INT i, j, k, min_i, min_j, min_k, max_iter, min_n
#
#     all_points_visited = False
#
#     if max_iterations != - 1:
#         max_iter = max_iterations
#     else:
#         max_iter = n_points
#
#     # L0
#     for _ in range(max_iter):
#         idx_to_visit = np.argwhere(points_to_visit)
#         idx_to_visit_i = idx_to_visit[:, 0]
#         idx_to_visit_j = idx_to_visit[:, 1]
#         idx_to_visit_k = idx_to_visit[:, 2]
#         for n in range(len(idx_to_visit)):
#             i = idx_to_visit_i[n]
#             j = idx_to_visit_j[n]
#             k = idx_to_visit_k[n]
#             if vectors[0, i, j, k] > 0:
#                 L0_i = abs_vectors[0, i, j, k] * L0[i - 1, j, k]
#             else:
#                 L0_i = abs_vectors[0, i, j, k] * L0[i + 1, j, k]
#             if vectors[1, i, j, k] > 0:
#                 L0_j = abs_vectors[1, i, j, k] * L0[i, j - 1, k]
#             else:
#                 L0_j = abs_vectors[1, i, j, k] * L0[i, j + 1, k]
#             if vectors[2, i, j, k] > 0:
#                 L0_k = abs_vectors[2, i, j, k] * L0[i, j, k - 1]
#             else:
#                 L0_k = abs_vectors[2, i, j, k] * L0[i, j, k + 1]
#             value = (L0_i + L0_j + L0_k + 1) / sum_abs_vectors[i, j, k]
#             L0[i, j, k] = value
#             if value < min_value:
#                 min_value = value
#                 min_n = n
#                 min_i = i
#                 min_j = j
#                 min_k = k
#         visited[idx_to_visit_i, idx_to_visit_j, idx_to_visit_k] = True
#         # STEP 3
#         solved[min_i, min_j, min_k] = True
#         # STEP 4
#         if not all_points_visited:
#             neighbors = np.logical_and(binary_dilation(visited), wall)
#             unsolved_neighbors = np.logical_and(neighbors,
#                                                 np.logical_not(solved))
#             if neighbors.sum() == n_points:
#                 all_points_visited = True
#         else:
#             unsolved_neighbors[min_i, min_j, min_k] = False
#         points_to_visit = unsolved_neighbors
#
#     # L1
#     points_to_visit = outer_boundary
#     all_points_visited = False
#     neighbors = np.zeros_like(neighbors)
#     visited = np.zeros_like(neighbors)
#     solved = np.zeros_like(neighbors)
#     min_value = float("Inf")
#     for _ in range(max_iter):
#         idx_to_visit = np.argwhere(points_to_visit)
#         idx_to_visit_i = idx_to_visit[:, 0]
#         idx_to_visit_j = idx_to_visit[:, 1]
#         idx_to_visit_k = idx_to_visit[:, 2]
#         for n in range(len(idx_to_visit)):
#             i = idx_to_visit_i[n]
#             j = idx_to_visit_j[n]
#             k = idx_to_visit_k[n]
#             if vectors[0, i, j, k] < 0:
#                 L1_i = abs_vectors[0, i, j, k] * L1[i - 1, j, k]
#             else:
#                 L1_i = abs_vectors[0, i, j, k] * L1[i + 1, j, k]
#             if vectors[1, i, j, k] < 0:
#                 L1_j = abs_vectors[1, i, j, k] * L1[i, j - 1, k]
#             else:
#                 L1_j = abs_vectors[1, i, j, k] * L1[i, j + 1, k]
#             if vectors[2, i, j, k] < 0:
#                 L1_k = abs_vectors[2, i, j, k] * L1[i, j, k - 1]
#             else:
#                 L1_k = abs_vectors[2, i, j, k] * L1[i, j, k + 1]
#             value = (L1_i + L1_j + L1_k + 1) / sum_abs_vectors[i, j, k]
#             L1[i, j, k] = value
#             if value < min_value:
#                 min_value = value
#                 min_i = i
#                 min_j = j
#                 min_k = k
#         visited[idx_to_visit_i, idx_to_visit_j, idx_to_visit_k] = True
#         # STEP 3
#         solved[min_i, min_j, min_k] = True
#         # STEP 4
#         if not all_points_visited:
#             neighbors = np.logical_and(binary_dilation(visited), wall)
#             unsolved_neighbors = np.logical_and(neighbors,
#                                                 np.logical_not(solved))
#             if neighbors.sum() == n_points:
#                 all_points_visited = True
#         else:
#             unsolved_neighbors[min_i, min_j, min_k] = False
#         points_to_visit = unsolved_neighbors
#
#     return L0, L1
