import numpy as np

from transforms.projection_transforms import viewport_transform, perspective_projection
from core.rasterizer import fill_polygon_scanline, draw_line


def render_solid(framebuffer, solid, color, width, height):
    """
    Orquestra o pipeline, fazendo backface culling, ordenando faces pelo
    Algoritmo do Pintor e as rasteriza.
    """
    projected = perspective_projection(solid['vertices'])
    screen_vertices = viewport_transform(projected, width, height)

    faces_to_draw = []

    # 1. Avaliar faces, descartar ocultas e calcular profundidade
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

        if np.dot(normal, view_vector) >= 0:
            continue

        p1 = screen_vertices[v1_idx]
        p2 = screen_vertices[v2_idx]
        p3 = screen_vertices[v3_idx]

        if p1 is None or p2 is None or p3 is None:
            continue

        # Calcula a profundidade média da face (Z) no espaço da câmera
        # Z negativo significa na frente da câmera. Quanto menor o valor, mais distante.
        z_avg = (p1_3d[2] + p2_3d[2] + p3_3d[2]) / 3.0

        # Guarda a face visível com seu Z médio
        faces_to_draw.append({
            'z_avg': z_avg,
            'p1': p1, 'p2': p2, 'p3': p3
        })

    # 2. ALGORITMO DO PINTOR (Ordenar faces de trás para frente)
    # Ordena as faces para desenhar as com Z menor (mais distantes) primeiro
    faces_to_draw.sort(key=lambda f: f['z_avg'])

    # 3. Desenhar e preencher as faces visíveis na ordem correta
    for face in faces_to_draw:
        x1, y1 = face['p1']
        x2, y2 = face['p2']
        x3, y3 = face['p3']

        vertices_da_face = [face['p1'], face['p2'], face['p3']]

        # Primeiro, pinta o interior da face usando o Scanline (Regra Par-Ímpar)
        fill_polygon_scanline(framebuffer, vertices_da_face, color, width, height)

        # Depois, desenha as arestas por cima para garantir que não haja "buracos" de arredondamento
        # nas bordas dos polígonos. Cumprindo 100%: "arestas e faces com mesma cor"
        draw_line(framebuffer, x1, y1, x2, y2, color, width, height)
        draw_line(framebuffer, x2, y2, x3, y3, color, width, height)
        draw_line(framebuffer, x3, y3, x1, y1, color, width, height)