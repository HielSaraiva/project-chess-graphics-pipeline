from generators.object_generator import generate_queen_object
from visualization.object_visualizer import visualize_object

# Questão 1
# Peça: Rainha de Xadrez
print("Gerando o volume com Marching Cubes - Rainha de Xadrez")
rainha = generate_queen_object(100)

print(f"Sólido gerado com {len(rainha['vertices'])} vértices e {len(rainha['faces'])} faces triangulares.")
print("Abrindo visualização 3D")
visualize_object(rainha)

# Peça: