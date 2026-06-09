import numpy as np

from core.lighting import compute_phong_lighting
from transforms.projection_transforms import viewport_transform, perspective_projection
from core.rasterizer import fill_polygon_scanline, draw_line


def render_scene(framebuffer, camera_scene, colors, width, height):
    """
    Orquestra o pipeline, fazendo backface culling, ordenando faces pelo
    Algoritmo do Pintor e as rasteriza.
    """
    all_faces_to_draw = []

    # 1. Iterar sobre TODOS os sólidos e coletar suas faces visíveis
    for solid, color in zip(camera_scene, colors):
        projected = perspective_projection(solid['vertices'])
        screen_vertices = viewport_transform(projected, width, height)

        for face in solid['faces']:
            v1_idx, v2_idx, v3_idx = face

            p1_3d = np.array(solid['vertices'][v1_idx])
            p2_3d = np.array(solid['vertices'][v2_idx])
            p3_3d = np.array(solid['vertices'][v3_idx])

            # BACKFACE CULLING
            vec1 = p2_3d - p1_3d
            vec2 = p3_3d - p1_3d
            normal = np.cross(vec1, vec2)
            view_vector = p1_3d

            if np.dot(normal, view_vector) <= 0:
                continue

            p1 = screen_vertices[v1_idx]
            p2 = screen_vertices[v2_idx]
            p3 = screen_vertices[v3_idx]

            if p1 is None or p2 is None or p3 is None:
                continue

            # Calcula profundidade
            z_avg = (p1_3d[2] + p2_3d[2] + p3_3d[2]) / 3.0

            # Guarda a face COM SUA RESPECTIVA COR na lista global
            all_faces_to_draw.append({
                'z_avg': z_avg,
                'p1': p1, 'p2': p2, 'p3': p3,
                'color': color  # Importante: salvar a cor desta face!
            })

    # 2. ALGORITMO DO PINTOR GLOBAL
    # Ordena TODAS as faces da cena da mais distante (menor Z) para a mais próxima
    all_faces_to_draw.sort(key=lambda f: f['z_avg'])

    # 3. Desenhar e preencher as faces visíveis na ordem correta
    for face in all_faces_to_draw:
        x1, y1 = face['p1']
        x2, y2 = face['p2']
        x3, y3 = face['p3']
        color = face['color']  # Recupera a cor da peça a que essa face pertence

        vertices_da_face = [face['p1'], face['p2'], face['p3']]

        fill_polygon_scanline(framebuffer, vertices_da_face, color, width, height)

        draw_line(framebuffer, x1, y1, x2, y2, color, width, height)
        draw_line(framebuffer, x2, y2, x3, y3, color, width, height)
        draw_line(framebuffer, x3, y3, x1, y1, color, width, height)

def render_scene_phong(framebuffer, camera_scene, light_pos_cam, colors, width, height, light_params):
    """
    Orquestra o pipeline com iluminação Phong nos vértices, Backface Culling
    e o Algoritmo do Pintor.
    """
    all_faces_to_draw = []

    # 1. Iterar sobre os sólidos e projetar
    for solid, base_color in zip(camera_scene, colors):
        projected = perspective_projection(solid['vertices'])
        screen_vertices = viewport_transform(projected, width, height)

        # 2. Processar cada face
        for face in solid['faces']:
            v1_idx, v2_idx, v3_idx = face

            p1_3d = np.array(solid['vertices'][v1_idx])
            p2_3d = np.array(solid['vertices'][v2_idx])
            p3_3d = np.array(solid['vertices'][v3_idx])

            # Backface Culling (Normal apontando para fora da câmera descartada)
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

            c1 = compute_phong_lighting(p1_3d, n1_3d, light_pos_cam, base_color, light_params)
            c2 = compute_phong_lighting(p2_3d, n2_3d, light_pos_cam, base_color, light_params)
            c3 = compute_phong_lighting(p3_3d, n3_3d, light_pos_cam, base_color, light_params)

            # Shading Híbrido: Média das cores
            face_color = ((c1 + c2 + c3) / 3.0).astype(int)
            z_avg = (p1_3d[2] + p2_3d[2] + p3_3d[2]) / 3.0

            all_faces_to_draw.append({
                'z_avg': z_avg,
                'p1': p1_2d, 'p2': p2_2d, 'p3': p3_2d,
                'color': face_color
            })

    # 3. Algoritmo do Pintor (ordenar por Z do menor para o maior)
    all_faces_to_draw.sort(key=lambda f: f['z_avg'])

    # 4. Rasterizar
    for face in all_faces_to_draw:
        x1, y1 = face['p1']
        x2, y2 = face['p2']
        x3, y3 = face['p3']
        color = face['color']

        vertices_da_face = [face['p1'], face['p2'], face['p3']]

        fill_polygon_scanline(framebuffer, vertices_da_face, color, width, height)
        # Contorno para mitigar buracos de rasterização (Z-fighting intrapolígono)
        draw_line(framebuffer, x1, y1, x2, y2, color, width, height)
        draw_line(framebuffer, x2, y2, x3, y3, color, width, height)
        draw_line(framebuffer, x3, y3, x1, y1, color, width, height)