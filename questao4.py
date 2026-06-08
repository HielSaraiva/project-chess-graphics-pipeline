from generators.world_scene_generator import generate_world_scene
from transforms.camera_transforms import compute_view_matrix
from transforms.affine_transforms import apply_transformation
import numpy as np

WIDTH = 800
HEIGHT = 600


def perspective_projection(vertices, d=2.0):

    projected = []

    for v in vertices:

        x = v[0]
        y = v[1]
        z = v[2]

        # descarta pontos atrás da câmera
        if z >= 0:
            projected.append(None)
            continue

        xp = d * x / (-z)
        yp = d * y / (-z)

        projected.append((xp, yp))

    return projected


def viewport_transform(projected_vertices):

    screen_vertices = []

    for p in projected_vertices:

        if p is None:
            screen_vertices.append(None)
            continue

        x, y = p

        sx = int((x + 1.0) * WIDTH / 2)
        sy = int((1.0 - y) * HEIGHT / 2)

        screen_vertices.append((sx, sy))

    return screen_vertices


def draw_line(framebuffer, x1, y1, x2, y2, color):

    # Algoritmo de Bresenham
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    err = dx - dy

    while True:

        if 0 <= x1 < WIDTH and 0 <= y1 < HEIGHT:
            framebuffer[y1][x1] = color

        if x1 == x2 and y1 == y2:
            break

        e2 = 2 * err

        if e2 > -dy:
            err -= dy
            x1 += sx

        if e2 < dx:
            err += dx
            y1 += sy


def fill_polygon_scanline(framebuffer, screen_vertices, color):
    """
    Preenche um polígono (triângulo) utilizando o algoritmo de Scanline (Regra Par-Ímpar).
    """
    # Encontra a bounding box (caixa delimitadora) do triângulo no eixo Y
    min_y = int(min(v[1] for v in screen_vertices))
    max_y = int(max(v[1] for v in screen_vertices))

    # Corta (clipping) para garantir que não vamos tentar pintar fora da tela
    min_y = max(0, min_y)
    max_y = min(HEIGHT - 1, max_y)

    # Para cada linha horizontal (scanline) dentro do triângulo
    for y in range(min_y, max_y + 1):
        intersections = []

        # Testa a interseção da linha 'y' atual com as 3 arestas do triângulo
        for i in range(3):
            p1 = screen_vertices[i]
            p2 = screen_vertices[(i + 1) % 3]

            # Garante que p1 é o ponto mais baixo da aresta (menor Y) para facilitar a matemática
            if p1[1] > p2[1]:
                p1, p2 = p2, p1

            # Verifica se a scanline 'y' corta esta aresta
            if p1[1] <= y < p2[1]:
                # Interpolação linear para achar o valor exato de X onde a scanline cruza a aresta
                if p1[1] != p2[1]:  # Prevenção de divisão por zero
                    x_int = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])
                    intersections.append(int(x_int))

        # Ordena as interseções no eixo X da esquerda para a direita
        intersections.sort()

        # Regra Par-Ímpar (Odd-Even): pinta entre os pares de interseções
        for i in range(0, len(intersections) - 1, 2):
            x_start = max(0, intersections[i])
            x_end = min(WIDTH - 1, intersections[i + 1])

            # Preenche os pixels entre a borda esquerda (Par) e a borda direita (Ímpar)
            for x in range(x_start, x_end + 1):
                framebuffer[y][x] = color


def draw_object(framebuffer, solid, color):
    projected = perspective_projection(solid['vertices'])
    screen_vertices = viewport_transform(projected)

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
        fill_polygon_scanline(framebuffer, vertices_da_face, color)

        # Depois, desenha as arestas por cima para garantir que não haja "buracos" de arredondamento
        # nas bordas dos polígonos. Cumprindo 100%: "arestas e faces com mesma cor"
        draw_line(framebuffer, x1, y1, x2, y2, color)
        draw_line(framebuffer, x2, y2, x3, y3, color)
        draw_line(framebuffer, x3, y3, x1, y1, color)


def save_ppm(framebuffer, filename):

    with open(filename, "w") as file:

        file.write(f"P3\n{WIDTH} {HEIGHT}\n255\n")

        for row in framebuffer:

            for pixel in row:

                r, g, b = pixel

                file.write(
                    f"{r} {g} {b} "
                )

            file.write("\n")


# =====================================================
# CENA
# =====================================================

world_scene = generate_world_scene()

target = [0, 0, 0]
up = [0, 0, 1]

# mesma câmera da Questão 3
# eye = [0, -20, 2]
# eye = [15, 15, 15]
eye = [15, 15, 15]



view_matrix = compute_view_matrix(
    eye,
    target,
    up
)

camera_scene = []

for solid in world_scene:

    transformed_vertices = apply_transformation(
        solid['vertices'],
        view_matrix
    )

    cam_solid = {
        'name': solid['name'],
        'vertices': transformed_vertices,
        'edges': solid['edges'],
        'faces': solid['faces'],
        'normals': solid['normals']
    }

    camera_scene.append(cam_solid)

# =====================================================
# FRAMEBUFFER
# =====================================================

framebuffer = [
    [[255, 255, 255] for _ in range(WIDTH)]
    for _ in range(HEIGHT)
]

colors = [
    [255, 0, 0],      # Rainha
    [0, 255, 0],      # Bispo
    [0, 0, 255],      # Dama
    [255, 165, 0]     # Peão
]

for solid, color in zip(camera_scene, colors):

    draw_object(
        framebuffer,
        solid,
        color
    )

save_ppm(
    framebuffer,
    "questao4.ppm"
)

print("Arquivo questao4.ppm gerado.")