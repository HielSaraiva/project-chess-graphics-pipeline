import numpy as np

from generators.object_generator import generate_queen_object
from transforms.affine_transforms import apply_transformation, translation_matrix


def generate_world_scene():
    """
    Função auxiliar para montar o mundo da Questão 2 rapidamente.
    """
    print("Gerando o Mundo.")
    world = []

    # PEÇA 1: Rainha (0, 0)
    print("Gerando a geometria da Rainha.")
    queen = generate_queen_object(100)

    min_z = np.min(queen['vertices'][:, 2])
    translation_matrix_z = translation_matrix(0, 0, -min_z)
    queen['vertices'] = apply_transformation(queen['vertices'], translation_matrix_z)
    world.append(queen)

    # Adicionar as Peças 2, 3, 4 e 5 nas coordenadas (5, 5), (-5, 5), (-5, -5) e (5, -5)

    return world
