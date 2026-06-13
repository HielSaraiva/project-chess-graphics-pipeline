import numpy as np
from generators.world_scene_generator import generate_world_scene
from transforms.camera_transforms import compute_view_matrix
from transforms.affine_transforms import apply_transformation
from core.renderer import render_scene_phong
from utils.projection_io import save_ppm

COLORS = [
    np.array([255, 0, 0]),    # Rainha
    np.array([0, 255, 0]),    # Bispo
    np.array([0, 0, 255]),    # Dama 
    np.array([255, 165, 0]),  # Peão
    np.array([165, 255, 0]),  # Torre
    np.array([0, 255, 255])   # Superfície
]

TARGET = [0, 0, 0]
UP = [0, 0, 1]
EYE = [15, 15, 15]
LIGHT_POS_WORLD = np.array([20.0, -20.0, 30.0])

LIGHT_PARAMS = {
    'Ka': 0.6, 'Kd': 0.7, 'Ks': 0.5, 'shininess': 32
}

print("Iniciando Questão 6 - Interpolação Baricêntrica e Multi-Resolução...")

# Setup da Cena
world_scene = generate_world_scene()
view_matrix = compute_view_matrix(EYE, TARGET, UP)
rotation_matrix = np.array(view_matrix)[:3, :3]
camera_scene = []

for solid in world_scene:
    transformed_vertices = apply_transformation(solid['vertices'], view_matrix)
    transformed_normals = []
    for n in solid['normals']:
        n_rot = np.dot(rotation_matrix, n)
        transformed_normals.append(-n_rot)

    cam_solid = {
        'name': solid['name'],
        'vertices': transformed_vertices,
        'edges': solid['edges'],
        'faces': solid['faces'],
        'normals': transformed_normals
    }
    camera_scene.append(cam_solid)

light_pos_cam = np.array(apply_transformation(np.array([LIGHT_POS_WORLD]), view_matrix)[0])

# ==========================================
# TESTANDO AS 3 RESOLUÇÕES
# ==========================================
resolutions = [
    (400, 300, "baixa"),
    (800, 600, "media"),
    (1600, 1200, "alta")
]

for width, height, res_name in resolutions:
    print(f"\nRenderizando resolução {res_name.upper()} ({width}x{height})...")
    
    framebuffer = [[[255, 255, 255] for _ in range(width)] for _ in range(height)]
    
    render_scene_phong(
        framebuffer=framebuffer,
        camera_scene=camera_scene,
        light_pos_cam=light_pos_cam,
        colors=COLORS,
        width=width,
        height=height,
        light_params=LIGHT_PARAMS,
        use_barycentric=True
    )
    
    filename = f"questao6_resolucao_{res_name}.ppm"
    save_ppm(framebuffer, filename, width, height)
    print(f"Salvo: {filename}")

print("\nPipeline Gráfico finalizado com sucesso!")