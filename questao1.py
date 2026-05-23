from generators.mesh_generator import generate_queen_mesh
from visualization.mesh_visualizer import visualize_solid

# Questão 1
# Peça: Rainha de Xadrez
print("Gerando o volume com Marching Cubes - Rainha de Xadrez")
rainha = generate_queen_mesh(100)

print(f"Sólido gerado com {len(rainha['vertices'])} vértices e {len(rainha['faces'])} faces triangulares.")
print("Abrindo visualização 3D")
visualize_solid(rainha)

# Peça: