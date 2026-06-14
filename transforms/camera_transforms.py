import copy

import numpy as np

from transforms.affine_transforms import apply_transformation
from visualization.camera_visualizer import visualize_camera_view


def compute_view_matrix(eye, target, up):
    """
    Computa a base vetorial da câmera e retorna a View Matrix 4x4.
    """
    eye = np.array(eye, dtype=float)
    target = np.array(target, dtype=float)
    up = np.array(up, dtype=float)

    n = eye - target
    n = n / np.linalg.norm(n)

    u = np.cross(up, n)
    u = u / np.linalg.norm(u)

    v = np.cross(n, u)

    # Matriz RT (Rotação + Translação)
    view_matrix = np.array([
        [u[0], u[1], u[2], -np.dot(u, eye)],
        [v[0], v[1], v[2], -np.dot(v, eye)],
        [n[0], n[1], n[2], -np.dot(n, eye)],
        [0.0,  0.0,  0.0,  1.0]
    ])
    return view_matrix

def render_camera_view(world_solids, eye, target, up, camera_name):
    """
    Executa a transformação e visualização para uma câmera específica.
    """
    print(f"\nCalculando a Matriz de Visão para a {camera_name} (eye={eye})")

    view_mat = compute_view_matrix(eye, target, up)

    # Transformar os objetos para o sistema de coordenadas da câmera
    camera_solids = []
    for solid in world_solids:
        cam_solid = copy.deepcopy(solid)
        cam_solid['vertices'] = apply_transformation(cam_solid['vertices'], view_mat)
        camera_solids.append(cam_solid)

    # Transformar a Origem do Mundo (0,0,0)
    world_origin = np.array([[0.0, 0.0, 0.0]])
    camera_origin = apply_transformation(world_origin, view_mat)[0]

    print(f"Desenhando cena")
    visualize_camera_view(camera_solids, camera_origin, title=f"Sistema da Câmera - {camera_name}")