from generators.object_generator import generate_queen_object
from generators.object_generator import generate_bishop_object
from generators.object_generator import generate_checker_object
from generators.object_generator import generate_pawn_object
from generators.object_generator import generate_rook_object
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

# Peça: Dama
print("Gerando o volume com Marching Cubes - Dama")
dama = generate_checker_object(100)

print(f"Sólido gerado com {len(dama['vertices'])} vértices e {len(dama['faces'])} faces triangulares.")
print("Abrindo visualização 3D")
visualize_object(dama)

# Peça: Peão
print("Gerando o volume com Marching Cubes - Peão")
peao = generate_pawn_object(100)

print(f"Sólido gerado com {len(peao['vertices'])} vértices e {len(peao['faces'])} faces triangulares.")
print("Abrindo visualização 3D")
visualize_object(peao)

# Peça: Torre
print("Gerando o volume com Marching Cubes - Torre")
torre = generate_rook_object(100)

print(f"Sólido gerado com {len(torre['vertices'])} vértices e {len(torre['faces'])} faces triangulares.")
print("Abrindo visualização 3D")
visualize_object(torre)