def perspective_projection(vertices, d=2.0):
    """
    Projeta coordenadas 3D no plano 2D usando divisão por -z para criar
    efeito de profundidade.
    """

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

def viewport_transform(projected_vertices, width, height):
    """
    Mapeia coordenadas normalizadas [-1, 1] para a grade de pixels da tela.
    """

    screen_vertices = []

    for p in projected_vertices:

        if p is None:
            screen_vertices.append(None)
            continue

        x, y = p

        sx = int((x + 1.0) * width / 2)
        sy = int((1.0 - y) * height / 2)

        screen_vertices.append((sx, sy))

    return screen_vertices