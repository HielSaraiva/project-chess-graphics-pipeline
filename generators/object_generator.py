import numpy as np
from skimage.measure import marching_cubes


def generate_queen_object(grid_resolution):
    """
    Gera a malha triangular da Rainha utilizando um perfil de revolução definido por uma função implícita.
    """

    # 1. Definição do Espaço Discreto (Grid 3D)
    # Criamos os vetores unidimensionais para cada eixo delimitando a "caixa" de modelagem.
    axis_x = np.linspace(-1.5, 1.5, grid_resolution)
    axis_y = np.linspace(-1.5, 1.5, grid_resolution)
    axis_z = np.linspace(0.0, 5.0, grid_resolution)

    # Expandimos os vetores 1D em matrizes 3D para avaliar equações em todo o espaço
    grid_x, grid_y, grid_z = np.meshgrid(axis_x, axis_y, axis_z, indexing='ij')

    # 2. Construção do Perfil de Revolução
    # radius_field armazenará o raio exato da peça para cada coordenada de altura (Z)
    radius_field = np.zeros_like(grid_z)

    # Região 1: Base (Tronco de cone)
    region_base = (grid_z >= 0.0) & (grid_z < 0.6)
    radius_field[region_base] = 0.8 - 0.3 * grid_z[region_base]

    # Região 2: Corpo principal com decaimento exponencial
    region_body = (grid_z >= 0.6) & (grid_z < 3.0)
    t = (grid_z[region_body] - 0.6) / (2.0 - 0.6)
    radius_field[region_body] = (0.20 + 0.45 * np.exp(-2.2 * t))

    # Região 3: Colar (Cilindro de transição)
    region_collar = (grid_z >= 3.0) & (grid_z < 3.2)
    radius_field[region_collar] = 0.4

    # Região 4: Coroa Inferior (Cone invertido)
    region_crown = (grid_z >= 3.2) & (grid_z < 4.2)
    radius_field[region_crown] = 0.13 + 0.3 * (grid_z[region_crown] - 2.7)

    # Região 5: Topo da coroa (Cone)
    region_dome = (grid_z >= 4.2) & (grid_z < 4.5)
    radius_field[region_dome] = (0.43 * (1 - (grid_z[region_dome] - 4.2) / (4.5 - 4.2)))

    # Região 6: Bolinha
    region_sphere = (grid_z >= 4.5) & (grid_z <= 4.8)
    inside_sqrt_sphere = np.clip(0.15 ** 2 - (grid_z[region_sphere] - 4.65) ** 2, 0, None)
    radius_field[region_sphere] = np.sqrt(inside_sqrt_sphere)

    # 3. Geração do Campo Escalar (Função Implícita)
    # Avaliamos a função F(x, y, z) = x^2 + y^2 - R(z)^2 para todos os pontos do grid.
    # Valores < 0 representam o interior da peça. Valores > 0 representam o exterior.
    scalar_field = grid_x ** 2 + grid_y ** 2 - radius_field ** 2

    # Fechamento geométrico da malha inferior (evita que a base fique oca)
    # Forçamos o valor do campo escalar na cota z=0 para um valor positivo (exterior)
    scalar_field[:, :, 0] = 1.0

    # 4. Extração da Malha de Triângulos
    # O algoritmo encontra a superfície exata onde o campo escalar cruza o zero (level=0.0)
    # Utilizamos o sublinhado '_' para ignorar o retorno 'values' que não é utilizado
    vertices, faces, normals, _ = marching_cubes(scalar_field, level=0.0, gradient_direction='ascent')

    # 5. Transformações Iniciais (Normalização Espacial)
    # Centralizamos a peça subtraindo a média das coordenadas para que a origem seja o centro de massa
    vertices = vertices - np.mean(vertices, axis=0)

    # Escalamos a peça para respeitar os limites espaciais definidos pelo projeto
    max_absolute_coordinate = np.max(np.abs(vertices))
    vertices = (vertices / max_absolute_coordinate) * 4.0

    # 6. Derivação Topológica (Cálculo das Arestas)
    # Extraímos as arestas únicas a partir das faces triangulares geradas pelo marching_cubes
    unique_edges = set()
    for face in faces:
        v1, v2, v3 = face
        unique_edges.add(tuple(sorted((v1, v2))))
        unique_edges.add(tuple(sorted((v2, v3))))
        unique_edges.add(tuple(sorted((v3, v1))))
    edges = np.array(list(unique_edges))

    # 7. Estruturação do Retorno
    object_data = {
        'name': 'Rainha',
        'vertices': vertices,
        'edges': edges,
        'faces': faces,
        'normals': normals
    }

    return object_data
