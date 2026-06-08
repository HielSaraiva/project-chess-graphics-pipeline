import numpy as np

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