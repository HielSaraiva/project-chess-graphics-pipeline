import numpy as np
from matplotlib import pyplot as plt


def visualize_camera_view(camera_solids, world_origin_cam, title="Visão da Câmera"):
    """
    Renderiza a cena garantindo proporção geométrica perfeita e exibindo a origem.
    """
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    colors = ['white', 'lightgray', 'silver', 'darkgray', 'gray']

    # Listas para guardar TODAS as coordenadas (para calcular os limites da tela)
    # Já começamos colocando as coordenadas do Ponto Vermelho (Origem do Mundo)
    all_x = [world_origin_cam[0]]
    all_y = [world_origin_cam[1]]
    all_z = [world_origin_cam[2]]

    for i, solid in enumerate(camera_solids):
        verts = solid['vertices']
        faces = solid['faces']
        color_face = colors[i % len(colors)]

        x, y, z = verts[:, 0], verts[:, 1], verts[:, 2]

        # Adicionamos os vértices à nossa lista de limites
        all_x.extend(x)
        all_y.extend(y)
        all_z.extend(z)

        ax.plot_trisurf(
            x, y, z,
            triangles=faces, edgecolor='black', facecolor=color_face,
            alpha=0.2, linewidth=0.1
        )

    # Colocando um ponto informando a origem do sistema do mundo
    ax.scatter(world_origin_cam[0], world_origin_cam[1], world_origin_cam[2],
               color='red', s=200, label='Origem do Mundo (0,0,0)', zorder=5)

    all_x = np.array(all_x)
    all_y = np.array(all_y)
    all_z = np.array(all_z)

    # Descobrimos o centro exato entre as peças e a origem, e a maior distância
    max_range = np.array([all_x.max() - all_x.min(), all_y.max() - all_y.min(), all_z.max() - all_z.min()]).max() / 2.0
    mid_x = (all_x.max() + all_x.min()) * 0.5
    mid_y = (all_y.max() + all_y.min()) * 0.5
    mid_z = (all_z.max() + all_z.min()) * 0.5

    # Forçamos o gráfico a criar uma caixa cúbica que abrace TUDO
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    # Restaura a proporção base 1:1:1
    ax.set_box_aspect((1, 1, 1))

    ax.set_title(title)
    ax.set_xlabel('Eixo U (Direita)')
    ax.set_ylabel('Eixo V (Cima)')
    ax.set_zlabel('Eixo N (Profundidade)')
    ax.legend()

    plt.tight_layout()
    plt.show()