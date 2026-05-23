import numpy as np

from transforms.affine_transforms import apply_transformation, translation_matrix
from generators.object_generator import generate_queen_object
from visualization.world_visualizer import visualize_world

# Questão 2

world = []

# PEÇA 1: Rainha (0, 0)
print("Gerando a geometria da Rainha.")
queen = generate_queen_object(100)

min_z = np.min(queen['vertices'][:, 2])
translation_matrix_z = translation_matrix(0, 0, -min_z)
queen['vertices'] = apply_transformation(queen['vertices'], translation_matrix_z)
world.append(queen)

# Adicionar as Peças 2, 3, 4 e 5 nas coordenadas (5, 5), (-5, 5), (-5, -5) e (5, -5)

print(f"Desenhando cena com {len(world)} sólidos.")
visualize_world(world)