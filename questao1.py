from generators.object_generator import generate_queen_object
from generators.object_generator import generate_bishop_object
from visualization.object_visualizer import visualize_object

# Questão 1
# Peça: Rainha de Xadrez
print("Gerando o volume com Marching Cubes - Rainha de Xadrez")
rainha = generate_queen_object(100)

print(f"Sólido gerado com {len(rainha['vertices'])} vértices e {len(rainha['faces'])} faces triangulares.")
print("Abrindo visualização 3D")
visualize_object(rainha)

# Peça: Bispo de Xadrez
print("Gerando o volume com Marching Cubes - Bispo de Xadrez")
bispo = generate_bishop_object(100)

print(f"Sólido gerado com {len(bispo['vertices'])} vértices e {len(bispo['faces'])} faces triangulares.")
print("Abrindo visualização 3D")
visualize_object(bispo)