import numpy as np


def apply_transformation(vertices, matrix):
    """
    Aplica uma matriz de transformação 4x4 a um conjunto de vértices 3D.
    Utiliza coordenadas homogêneas [x, y, z, 1].
    """
    ones = np.ones((vertices.shape[0], 1))
    v_homo = np.hstack((vertices, ones))

    v_transformed = v_homo @ matrix.T

    return v_transformed[:, :3]


def translation_matrix(tx, ty, tz):
    """Retorna a matriz de Translação 4x4"""
    return np.array([
        [1.0, 0.0, 0.0, tx],
        [0.0, 1.0, 0.0, ty],
        [0.0, 0.0, 1.0, tz],
        [0.0, 0.0, 0.0, 1.0]
    ])


def rotation_z_matrix(angle_degrees):
    """Retorna a matriz de Rotação 4x4 no eixo Z"""
    theta = np.radians(angle_degrees)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    return np.array([
        [cos_t, -sin_t, 0.0, 0.0],
        [sin_t, cos_t, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ])