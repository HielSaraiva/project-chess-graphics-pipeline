from generators.world_scene_generator import generate_world_scene
from transforms.camera_transforms import compute_view_matrix
from transforms.affine_transforms import apply_transformation


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


def draw_object(framebuffer, solid, color):

    projected = perspective_projection(
        solid['vertices']
    )

    screen_vertices = viewport_transform(
        projected
    )

    for edge in solid['edges']:

        v1, v2 = edge

        p1 = screen_vertices[v1]
        p2 = screen_vertices[v2]

        if p1 is None or p2 is None:
            continue

        x1, y1 = p1
        x2, y2 = p2

        draw_line(
            framebuffer,
            x1, y1,
            x2, y2,
            color
        )


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
eye = [0, -20, 2]

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