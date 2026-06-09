import numpy as np

from generators.world_scene_generator import generate_world_scene
from transforms.camera_transforms import compute_view_matrix
from transforms.affine_transforms import apply_transformation
from core.renderer import render_scene_phong
from utils.projection_io import save_ppm


WIDTH = 800
HEIGHT = 600

COLORS = [
    np.array([255, 0, 0]),  # Rainha
    np.array([0, 255, 0]),  # Bispo
    np.array([0, 0, 255]),  # Dama (Base)
    np.array([255, 165, 0]),  # Peão
    np.array([165, 255, 0])  # Torre
]

TARGET = [0, 0, 0]
UP = [0, 0, 1]
EYE = [15, 15, 15]

LIGHT_POS_WORLD = np.array([20.0, -20.0, 30.0])

# Dicionário de parâmetros do material repassado ao pipeline
LIGHT_PARAMS = {
    'Ka': 0.6,
    'Kd': 0.7,
    'Ks': 0.5,
    'shininess': 32
}

print("Iniciando renderização da Questão 5 com Iluminação...")

# 1. Geração e setup da câmera
world_scene = generate_world_scene()
view_matrix = compute_view_matrix(EYE, TARGET, UP)
rotation_matrix = np.array(view_matrix)[:3, :3]

camera_scene = []

# 2. Transformação de Mundo para Câmera (Vértices e Normais)
for solid in world_scene:
    transformed_vertices = apply_transformation(solid['vertices'], view_matrix)

    transformed_normals = []
    for n in solid['normals']:
        n_rot = np.dot(rotation_matrix, n)
        transformed_normals.append(-n_rot)  # Ajuste direcional da normal do Marching Cubes

    cam_solid = {
        'name': solid['name'],
        'vertices': transformed_vertices,
        'edges': solid['edges'],
        'faces': solid['faces'],
        'normals': transformed_normals
    }
    camera_scene.append(cam_solid)

# 3. Transformação da posição da Luz para o Camera Space
light_pos_cam = apply_transformation(np.array([LIGHT_POS_WORLD]), view_matrix)[0]
light_pos_cam = np.array(light_pos_cam)

# 4. Inicialização do Framebuffer
framebuffer = [[[255, 255, 255] for _ in range(WIDTH)] for _ in range(HEIGHT)]

# 5. Execução do Pipeline de Renderização
render_scene_phong(
    framebuffer=framebuffer,
    camera_scene=camera_scene,
    light_pos_cam=light_pos_cam,
    colors=COLORS,
    width=WIDTH,
    height=HEIGHT,
    light_params=LIGHT_PARAMS
)

# 6. Salvar saída
output_filename = "questao5.ppm"
save_ppm(framebuffer, output_filename, WIDTH, HEIGHT)
print(f"Sucesso! Arquivo '{output_filename}' gerado com sombras e reflexos.")


