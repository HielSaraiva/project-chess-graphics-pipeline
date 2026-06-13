import numpy as np

def draw_line(framebuffer, x1, y1, x2, y2, color, width, height):
    """
    Algoritmo de Bresenham que rasteriza arestas usando apenas aritmética de inteiros.
    """
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    err = dx - dy

    while True:

        if 0 <= x1 < width and 0 <= y1 < height:
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

def compute_barycentric(x, y, p1, p2, p3):
    """Calcula os pesos baricêntricos (alpha, beta, gamma) de um pixel no triângulo."""
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    x3, y3 = p3[0], p3[1]
    
    det = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
    if det == 0:
        return 0.333, 0.333, 0.333
        
    alpha = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / det
    beta  = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / det
    gamma = 1.0 - alpha - beta
    return alpha, beta, gamma

def fill_polygon_scanline(framebuffer, screen_vertices, color, width, height, is_barycentric):
    """
    Preenche um polígono (triângulo) utilizando o algoritmo de Scanline (Regra Par-Ímpar).
    """
    
    if is_barycentric:
        c1, c2, c3 = color
        v1, v2, v3 = screen_vertices

    # Encontra a bounding box (caixa delimitadora) do triângulo no eixo Y
    min_y = int(min(v[1] for v in screen_vertices))
    max_y = int(max(v[1] for v in screen_vertices))

    # Corta (clipping) para garantir que não vamos tentar pintar fora da tela
    min_y = max(0, min_y)
    max_y = min(height - 1, max_y)

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
            x_end = min(width - 1, intersections[i + 1])

            # Preenche os pixels entre a borda esquerda (Par) e a borda direita (Ímpar)
            for x in range(x_start, x_end + 1):
                
                if is_barycentric:
                    alpha, beta, gamma = compute_barycentric(x, y, v1, v2, v3)
                    
                    final_color = (alpha * c1 + beta * c2 + gamma * c3).astype(int)
                    final_color = np.clip(final_color, 0, 255).astype(int)
                    framebuffer[y][x] = final_color
                else:
                    framebuffer[y][x] = color