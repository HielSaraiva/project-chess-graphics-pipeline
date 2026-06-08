from generators.world_scene_generator import generate_world_scene
from transforms.camera_transforms import compute_view_matrix
from transforms.affine_transforms import apply_transformation
from core.renderer import render_solid
from utils.projection_io import save_ppm


WIDTH = 800
HEIGHT = 600

# Cores dos objetos (Rainha, Bispo, Dama, Peão)
COLORS = [
    [255, 0, 0],
    [0, 255, 0],
    [0, 0, 255],
    [255, 165, 0]
]

# Configurações de Câmera
TARGET = [0, 0, 0]
UP = [0, 0, 1]
EYE = [15, 15, 15]
# EYE = [0, -20, 2]

print("Iniciando renderização da Questão 4...")

# 1. Geração da Cena no Espaço do Mundo
world_scene = generate_world_scene()

# 2. Transformação de Câmera (World Space -> Camera Space)
view_matrix = compute_view_matrix(EYE, TARGET, UP)
camera_scene = []

for solid in world_scene:
    transformed_vertices = apply_transformation(solid['vertices'], view_matrix)

    cam_solid = {
        'name': solid['name'],
        'vertices': transformed_vertices,
        'edges': solid['edges'],
        'faces': solid['faces'],
        'normals': solid['normals']
    }
    camera_scene.append(cam_solid)

# 3. Criação do Framebuffer (Fundo Branco)
framebuffer = [
    [[255, 255, 255] for _ in range(WIDTH)]
    for _ in range(HEIGHT)
]

# 4. Renderização (Projeção, Rasterização e Preenchimento)
for solid, color in zip(camera_scene, COLORS):
    render_solid(framebuffer, solid, color, WIDTH, HEIGHT)

# 5. Saída de Dados
output_filename = "questao4.ppm"
save_ppm(framebuffer, output_filename, WIDTH, HEIGHT)

print(f"Sucesso! Arquivo '{output_filename}' gerado.")