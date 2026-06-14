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

def generate_bishop_object(grid_resolution):
    """
    Gera a malha triangular do Bispo utilizando um perfil de revolução definido por uma função implícita.
    """

    axis_x = np.linspace(-1.5, 1.5, grid_resolution)
    axis_y = np.linspace(-1.5, 1.5, grid_resolution)
    axis_z = np.linspace(0.0, 4.0, grid_resolution)

    grid_x, grid_y, grid_z = np.meshgrid(axis_x, axis_y, axis_z, indexing='ij')

    radius_field = np.zeros_like(grid_z)

    # Região 1: Base (Tronco de cone)
    region_base = (grid_z >= 0.0) & (grid_z < 0.3)
    radius_field[region_base] = 0.7 - 0.3 * grid_z[region_base]

    # Região 2: Corpo principal com decaimento exponencial
    region_body = (grid_z >= 0.3) & (grid_z < 2.0)
    t = (grid_z[region_body] - 0.3) / (1.1 - 0.3)
    radius_field[region_body] = (0.20 + 0.45 * np.exp(-2.2 * t))

    # Região 3: Colar (Cilindro de transição)
    region_collar_1 = (grid_z >= 2.0) & (grid_z < 2.15)
    radius_field[region_collar_1] = 0.35

    # Região 4: Corpo superior 
    region_body = (grid_z >= 2.15) & (grid_z < 2.40)
    t = (grid_z[region_body] - 2.15) / 0.04
    radius_field[region_body] = (0.20 + 0.45 * np.exp(-2.2 * t))

    # Região 5: Esfera e Cone
    # PARTE 1: 65% DA ESFERA
    region_esfera = (grid_z >= 2.40) & (grid_z < 2.97)
    centro_z = 2.75
    raio_esfera = 0.4

    # Executa a esfera perfeitamente sem estourar o limite do raio
    inside_sphere = np.clip(raio_esfera**2 - (grid_z[region_esfera] - centro_z)**2, 0, None)
    radius_field[region_esfera] = np.sqrt(inside_sphere)

    # PARTE 2: CONE DE TRANSIÇÃO ENTRE A ESFERA E O TOPO
    region_cone = (grid_z >= 2.97) & (grid_z < 3.82)

    z_norm_cone = (grid_z[region_cone] - 2.97) / (3.82 - 2.97)

    raio_de_encaixe = np.sqrt(0.4**2 - (2.97 - 2.75)**2)

    radius_field[region_cone] = raio_de_encaixe * (1.0 - z_norm_cone)

    # Região 6: Bolinha
    region_top = (grid_z >= 3.79) & (grid_z <= 4.0)
    inside_sphere = np.clip(0.1**2 - (grid_z[region_top] - 3.85)**2, 0, None)
    radius_field[region_top] = np.sqrt(inside_sphere)

    scalar_field = grid_x ** 2 + grid_y ** 2 - radius_field ** 2

    scalar_field[:, :, 0] = 1.0

    vertices, faces, normals, _ = marching_cubes(scalar_field, level=0.0, gradient_direction='ascent')

    vertices = vertices - np.mean(vertices, axis=0)

    max_absolute_coordinate = np.max(np.abs(vertices))
    vertices = (vertices / max_absolute_coordinate) * 4.0

    unique_edges = set()
    for face in faces:
        v1, v2, v3 = face
        unique_edges.add(tuple(sorted((v1, v2))))
        unique_edges.add(tuple(sorted((v2, v3))))
        unique_edges.add(tuple(sorted((v3, v1))))
    edges = np.array(list(unique_edges))

    # 7. Estruturação do Retorno
    object_data = {
        'name': 'Bispo',
        'vertices': vertices,
        'edges': edges,
        'faces': faces,
        'normals': normals
    }

    return object_data

def generate_checker_object(grid_resolution):

    """
    Gera a malha triangular da Dama utilizando um perfil de revolução definido por uma função implícita.
    """

    axis_x = np.linspace(-1.5, 1.5, grid_resolution)
    axis_y = np.linspace(-1.5, 1.5, grid_resolution)
    axis_z = np.linspace(0.0, 4.0, grid_resolution) 

    grid_x, grid_y, grid_z = np.meshgrid(axis_x, axis_y, axis_z, indexing='ij')

    radius_field = np.zeros_like(grid_z)

    # Região 1: Base (Cilindro)
    region_base = (grid_z >= 0.0) & (grid_z < 0.7)
    radius_field[region_base] = 1.5 
    
    scalar_field = grid_x ** 2 + grid_y ** 2 - radius_field ** 2

    scalar_field[:, :, 0] = 1.0
    
    vertices, faces, normals, _ = marching_cubes(scalar_field, level=0.0, gradient_direction='ascent')

    vertices = vertices - np.mean(vertices, axis=0)

    max_absolute_coordinate = np.max(np.abs(vertices))
    vertices = (vertices / max_absolute_coordinate) * 1.5

    # Derivação Topológica (Cálculo das Arestas)
    unique_edges = set()
    for face in faces:
        v1, v2, v3 = face
        unique_edges.add(tuple(sorted((v1, v2))))
        unique_edges.add(tuple(sorted((v2, v3))))
        unique_edges.add(tuple(sorted((v3, v1))))

    edges = np.array(list(unique_edges))

    # Estruturação do Retorno
    object_data = {
        'name': 'Dama',
        'vertices': vertices,
        'edges': edges,
        'faces': faces,
        'normals': normals
    }

    return object_data 

def generate_pawn_object(grid_resolution):

    """
    Gera a malha triangular do Peão utilizando um perfil de revolução definido por uma função implícita.
    """

    axis_x = np.linspace(-1.5, 1.5, grid_resolution)
    axis_y = np.linspace(-1.5, 1.5, grid_resolution)
    axis_z = np.linspace(0.0, 3.0, grid_resolution) 

    grid_x, grid_y, grid_z = np.meshgrid(axis_x, axis_y, axis_z, indexing='ij')

    radius_field = np.zeros_like(grid_z)

    # Região 1: Base (Tronco de cone)
    region_base = (grid_z >= 0.0) & (grid_z < 0.3)
    radius_field[region_base] = 0.7 - 0.3 * grid_z[region_base]

    # Região 2: Corpo principal com decaimento exponencial
    region_body = (grid_z >= 0.3) & (grid_z < 2.0)
    t = (grid_z[region_body] - 0.3) / (1.1 - 0.3)
    radius_field[region_body] = (0.20 + 0.45 * np.exp(-2.2 * t))

    # Região 3: Colar (Cilindro de transição)
    region_collar = (grid_z >= 2.0) & (grid_z < 2.15)
    radius_field[region_collar] = 0.35

    # Região 4: Bolinha
    region_head = (grid_z >= 2.15) & (grid_z <= 3.0)
    centro_z = 2.5
    raio_esfera = 0.4 
    inside_sqrt_sphere = np.clip(raio_esfera**2 - (grid_z[region_head] - centro_z)**2, 0, None)
    radius_field[region_head] = np.sqrt(inside_sqrt_sphere)

    scalar_field = grid_x ** 2 + grid_y ** 2 - radius_field ** 2

    scalar_field[:, :, 0] = 1.0

    vertices, faces, normals, _ = marching_cubes(scalar_field, level=0.0, gradient_direction='ascent')

    vertices = vertices - np.mean(vertices, axis=0)

    max_absolute_coordinate = np.max(np.abs(vertices))
    vertices = (vertices / max_absolute_coordinate) * 3.5

    unique_edges = set()
    for face in faces:
        v1, v2, v3 = face
        unique_edges.add(tuple(sorted((v1, v2))))
        unique_edges.add(tuple(sorted((v2, v3))))
        unique_edges.add(tuple(sorted((v3, v1))))
    edges = np.array(list(unique_edges))

    # Estruturação do Retorno
    object_data = {
        'name': 'Peão',
        'vertices': vertices,
        'edges': edges,
        'faces': faces,
        'normals': normals
    }

    return object_data

def generate_rook_object(grid_resolution):
    """
    Gera a malha triangular da Torre utilizando revolução 
    """
    # 1. Grid
    axis_x = np.linspace(-1.5, 1.5, grid_resolution)
    axis_y = np.linspace(-1.5, 1.5, grid_resolution)
    axis_z = np.linspace(0.0, 3.0, grid_resolution) 

    grid_x, grid_y, grid_z = np.meshgrid(axis_x, axis_y, axis_z, indexing='ij')
    radius_field = np.zeros_like(grid_z)

    # Região 1: Base
    region_base = (grid_z >= 0.0) & (grid_z < 0.3)
    radius_field[region_base] = 0.7 - 0.3 * grid_z[region_base]

    # Região 2: Corpo principal com decaimento exponencial
    region_body = (grid_z >= 0.3) & (grid_z < 2.0)
    t = (grid_z[region_body] - 0.3) / (1.1 - 0.3)
    radius_field[region_body] = (0.20 + 0.45 * np.exp(-2.2 * t))

    # Região 3: Anel/Colar da Torre
    region_collar = (grid_z >= 2.0) & (grid_z < 2.2)
    radius_field[region_collar] = 0.35

    # Região 4: Coroa (O cilindro do topo)
    region_crown = (grid_z >= 2.2) & (grid_z <= 2.5)
    radius_field[region_crown] = 0.4

    scalar_field = grid_x ** 2 + grid_y ** 2 - radius_field ** 2

    # 5. Escavando o miolo (Deixando oco como um copo)
    hole_region = (grid_z >= 2.3) & (grid_z <= 2.5)
    hole_field = 0.3**2 - (grid_x[hole_region]**2 + grid_y[hole_region]**2)
    scalar_field[hole_region] = np.maximum(scalar_field[hole_region], hole_field)

    # 6. Recortando os Dentes do topo
    # Pegamos o ângulo de cada coordenada do espaço (olhando de cima)
    angulo = np.arctan2(grid_y, grid_x)
    regiao_dentes = (grid_z >= 2.35) & (grid_z <= 2.5) & (np.sin(5 * angulo) > 0)
    scalar_field[regiao_dentes] = 1.0 # Vazio

    scalar_field[:, :, 0] = 1.0

    vertices, faces, normals, _ = marching_cubes(scalar_field, level=0.0, gradient_direction='ascent')

    vertices = vertices - np.mean(vertices, axis=0)

    max_absolute_coordinate = np.max(np.abs(vertices))
    vertices = (vertices / max_absolute_coordinate) * 3.5

    unique_edges = set()
    for face in faces:
        v1, v2, v3 = face
        unique_edges.add(tuple(sorted((v1, v2))))
        unique_edges.add(tuple(sorted((v2, v3))))
        unique_edges.add(tuple(sorted((v3, v1))))
    edges = np.array(list(unique_edges))

    object_data = {
        'name': 'Torre',
        'vertices': vertices,
        'edges': edges,
        'faces': faces,
        'normals': normals
    }

    return object_data

def generate_surface_object(grid_resolution):
    """
    Gera a malha triangular de uma Superfície Bicúbica de Bézier com espessura volumétrica.
    """

    axis_x = np.linspace(-1.5, 1.5, grid_resolution)
    axis_y = np.linspace(-1.5, 1.5, grid_resolution)
    axis_z = np.linspace(-1.5, 1.5, grid_resolution) 

    grid_x, grid_y, grid_z = np.meshgrid(axis_x, axis_y, axis_z, indexing='ij')

    # Normalização de X e Y para os parâmetros u e v (de 0.0 a 1.0)
    u_1d = (axis_x - (-1.5)) / 3.0
    v_1d = (axis_y - (-1.5)) / 3.0
    
    # Matrizes de potências para u e v
    U = np.vstack([u_1d**3, u_1d**2, u_1d, np.ones_like(u_1d)]).T
    V = np.vstack([v_1d**3, v_1d**2, v_1d, np.ones_like(v_1d)])

    # Matriz de Base de Bézier
    Mb = np.array([
        [-1,  3, -3,  1],
        [ 3, -6,  3,  0],
        [-3,  3,  0,  0],
        [ 1,  0,  0,  0]
    ], dtype=float)
    
    # Matriz Geométrica Gz (Alturas dos 16 Pontos de Controle)
    Gz = np.array([
        [ 1.0,  0.5, -0.5, -1.0],
        [ 0.5,  0.2, -0.2, -0.5],
        [-0.5, -0.2,  0.2,  0.5],
        [-1.0, -0.5,  0.5,  1.0]
    ], dtype=float)

    # Produto Tensorial: Cálculo da superfície 2D
    U_Mb = U @ Mb
    MbT_V = Mb.T @ V
    Z_surface_2d = U_Mb @ Gz @ MbT_V

    # Transformação Volumétrica (Espessura)
    Z_surface_3d = np.repeat(Z_surface_2d[:, :, np.newaxis], grid_resolution, axis=2)
    espessura = 0.08  
    
    scalar_field = (grid_z - Z_surface_3d)**2 - espessura**2

    # Fechamento das bordas (Garante a criação das paredes laterais)
    scalar_field[0, :, :] = 1.0
    scalar_field[-1, :, :] = 1.0
    scalar_field[:, 0, :] = 1.0
    scalar_field[:, -1, :] = 1.0

    vertices, faces, normals, _ = marching_cubes(scalar_field, level=0.0, gradient_direction='ascent')

    vertices = vertices - np.mean(vertices, axis=0)

    max_absolute_coordinate = np.max(np.abs(vertices))
    vertices = (vertices / max_absolute_coordinate) * 3.0

    unique_edges = set()
    for face in faces:
        v1, v2, v3 = face
        unique_edges.add(tuple(sorted((v1, v2))))
        unique_edges.add(tuple(sorted((v2, v3))))
        unique_edges.add(tuple(sorted((v3, v1))))
    edges = np.array(list(unique_edges))

    # Estruturação do Retorno
    object_data = {
        'name': 'Superfície de Bézier',
        'vertices': vertices,
        'edges': edges,
        'faces': faces,
        'normals': normals
    }

    return object_data