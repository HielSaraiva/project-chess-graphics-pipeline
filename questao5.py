import numpy as np

# Importações dos módulos já criados nas questões anteriores
from generators.world_scene_generator import generate_world_scene
from transforms.camera_transforms import compute_view_matrix
from transforms.affine_transforms import apply_transformation
from transforms.projection_transforms import perspective_projection, viewport_transform
from core.rasterizer import draw_line, fill_polygon_scanline
# Substitua o caminho do save_ppm de acordo com sua pasta (ex: utils.projection_io)
from utils.projection_io import save_ppm

# =====================================================
# CONFIGURAÇÕES GERAIS E CONSTANTES
# =====================================================
WIDTH = 800
HEIGHT = 600

# Cores Base dos Objetos (RGB)
COLORS = [
    np.array([255, 0, 0]),      # Rainha
    np.array([0, 255, 0]),      # Bispo
    np.array([0, 0, 255]),      # Dama
    np.array([255, 165, 0]),    # Peão
    np.array([165, 255, 0])     # Torre
]

TARGET = [0, 0, 0]
UP = [0, 0, 1]
EYE = [15, 15, 15]
# EYE = [0, -20, 2]

# Configurações da Luz (World Space)
LIGHT_POS_WORLD = np.array([20.0, -20.0, 30.0])

# Constantes de Iluminação de Phong
Ka = 0.6  # Coeficiente Ambiente
Kd = 0.7  # Coeficiente Difuso
Ks = 0.5  # Coeficiente Especular
SHININESS = 32  # Brilho do ponto de luz

# =====================================================
# FUNÇÕES DE ILUMINAÇÃO (NOVIDADES DA QUESTÃO 5)
# =====================================================
def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def compute_lighting(vertex_cam, normal_cam, light_pos_cam, base_color):
    """
    Calcula o RGB de um vértice utilizando o Modelo de Reflexão de Phong.
    """
    L = normalize(light_pos_cam - vertex_cam)
    N = normalize(normal_cam)
    V = normalize(-vertex_cam) # Câmera está em (0,0,0)

    ambient = Ka * base_color

    dot_nl = np.dot(N, L)
    diffuse = np.array([0.0, 0.0, 0.0])
    if dot_nl > 0:
        diffuse = Kd * dot_nl * base_color

    specular = np.array([0.0, 0.0, 0.0])
    if dot_nl > 0:
        R = normalize(2.0 * dot_nl * N - L)
        dot_rv = np.dot(R, V)
        if dot_rv > 0:
            spec_intensity = (dot_rv ** SHININESS)
            specular = Ks * spec_intensity * np.array([255.0, 255.0, 255.0])

    final_color = ambient + diffuse + specular
    return np.clip(final_color, 0, 255).astype(int)

# =====================================================
# RENDERIZADOR COM SHADING HÍBRIDO
# =====================================================
def render_scene_with_lighting(framebuffer, camera_scene, light_pos_cam, colors, width, height):
    all_faces_to_draw = []

    for solid, base_color in zip(camera_scene, colors):
        projected = perspective_projection(solid['vertices'])
        screen_vertices = viewport_transform(projected, width, height)

        for face in solid['faces']:
            v1_idx, v2_idx, v3_idx = face

            p1_3d = np.array(solid['vertices'][v1_idx])
            p2_3d = np.array(solid['vertices'][v2_idx])
            p3_3d = np.array(solid['vertices'][v3_idx])

            # ==========================================================
            # BACKFACE CULLING CORRIGIDO
            # Como a malha tem as normais voltadas "para dentro",
            # invertemos a lógica. Descartamos (culling) as faces <= 0.
            # ==========================================================
            vec1 = p2_3d - p1_3d
            vec2 = p3_3d - p1_3d
            face_normal = np.cross(vec1, vec2)

            if np.dot(face_normal, p1_3d) <= 0:
                continue

            p1_2d = screen_vertices[v1_idx]
            p2_2d = screen_vertices[v2_idx]
            p3_2d = screen_vertices[v3_idx]

            if p1_2d is None or p2_2d is None or p3_2d is None:
                continue

            # Cálculo de Iluminação nos Vértices (Phong)
            n1_3d = np.array(solid['normals'][v1_idx])
            n2_3d = np.array(solid['normals'][v2_idx])
            n3_3d = np.array(solid['normals'][v3_idx])

            c1 = compute_lighting(p1_3d, n1_3d, light_pos_cam, base_color)
            c2 = compute_lighting(p2_3d, n2_3d, light_pos_cam, base_color)
            c3 = compute_lighting(p3_3d, n3_3d, light_pos_cam, base_color)

            # Shading Híbrido: Média das cores iluminadas
            face_color = ((c1 + c2 + c3) / 3.0).astype(int)
            z_avg = (p1_3d[2] + p2_3d[2] + p3_3d[2]) / 3.0

            all_faces_to_draw.append({
                'z_avg': z_avg,
                'p1': p1_2d, 'p2': p2_2d, 'p3': p3_2d,
                'color': face_color
            })

    # Algoritmo do Pintor Global
    all_faces_to_draw.sort(key=lambda f: f['z_avg'])

    for face in all_faces_to_draw:
        x1, y1 = face['p1']
        x2, y2 = face['p2']
        x3, y3 = face['p3']
        color = face['color']

        vertices_da_face = [face['p1'], face['p2'], face['p3']]

        fill_polygon_scanline(framebuffer, vertices_da_face, color, width, height)
        # O contorno com a mesma cor ajuda a esconder microprestas (Z-fighting)
        draw_line(framebuffer, x1, y1, x2, y2, color, width, height)
        draw_line(framebuffer, x2, y2, x3, y3, color, width, height)
        draw_line(framebuffer, x3, y3, x1, y1, color, width, height)

# =====================================================
# SCRIPT PRINCIPAL
# =====================================================
if __name__ == "__main__":
    print("Iniciando renderização da Questão 5 com Iluminação...")

    world_scene = generate_world_scene()
    view_matrix = compute_view_matrix(EYE, TARGET, UP)
    camera_scene = []

    rotation_matrix = np.array(view_matrix)[:3, :3]

    for solid in world_scene:
        transformed_vertices = apply_transformation(solid['vertices'], view_matrix)

        transformed_normals = []
        for n in solid['normals']:
            n_rot = np.dot(rotation_matrix, n)
            transformed_normals.append(-n_rot)  # Mantemos o sinal negativo para apontar a luz para fora

        cam_solid = {
            'name': solid['name'],
            'vertices': transformed_vertices,
            'edges': solid['edges'],
            'faces': solid['faces'],
            'normals': transformed_normals
        }
        camera_scene.append(cam_solid)

    # Transforma posição da luz
    light_pos_list = np.array([LIGHT_POS_WORLD])
    light_pos_cam = apply_transformation(light_pos_list, view_matrix)[0]
    light_pos_cam = np.array(light_pos_cam)

    framebuffer = [[[255, 255, 255] for _ in range(WIDTH)] for _ in range(HEIGHT)]

    render_scene_with_lighting(framebuffer, camera_scene, light_pos_cam, COLORS, WIDTH, HEIGHT)

    output_filename = "questao5.ppm"
    save_ppm(framebuffer, output_filename, WIDTH, HEIGHT)

    print(f"Sucesso! Arquivo '{output_filename}' gerado com sombras e reflexos.")