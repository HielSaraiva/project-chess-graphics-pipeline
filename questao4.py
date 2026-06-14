from generators.world_scene_generator import generate_world_scene
from transforms.camera_transforms import compute_view_matrix
from transforms.affine_transforms import apply_transformation
from core.renderer import render_scene  # <-- Mudou aqui
from utils.projection_io import save_ppm

WIDTH = 800
HEIGHT = 600

# Cores dos objetos (Rainha, Bispo, Dama, Peão, Torre, Superfície)
COLORS = [
    [255, 0, 0],
    [0, 255, 0],
    [0, 0, 255],
    [255, 165, 0],
    [165, 165, 0],
    [0, 255, 255]
]

TARGET = [0, 0, 0]
UP = [0, 0, 1]
EYE = [15, 15, 15]
# EYE = [0, -20, 2]

print("Iniciando renderização da Questão 4...")

world_scene = generate_world_scene()
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

framebuffer = [
    [[255, 255, 255] for _ in range(WIDTH)]
    for _ in range(HEIGHT)
]

# 4. Renderização Global (Chama a função única passando a cena toda)
render_scene(framebuffer, camera_scene, COLORS, WIDTH, HEIGHT)

output_filename = "questao4.ppm"
save_ppm(framebuffer, output_filename, WIDTH, HEIGHT)

print(f"Sucesso! Arquivo '{output_filename}' gerado.")