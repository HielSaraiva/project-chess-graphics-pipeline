from matplotlib import pyplot as plt


def visualize_world(solids_list):
    """
    Renderiza múltiplos sólidos no mesmo sistema de coordenadas do Mundo.
    Garante que os limites máximos não ultrapassem 10.
    """
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    colors = ['white', 'lightgray', 'silver', 'darkgray', 'gray']

    for i, solid in enumerate(solids_list):
        verts = solid['vertices']
        faces = solid['faces']

        color_face = colors[i % len(colors)]

        ax.plot_trisurf(
            verts[:, 0], verts[:, 1], verts[:, 2],
            triangles=faces, edgecolor='black', facecolor=color_face,
            alpha=0.8, linewidth=0.2
        )

    limit = 10.0
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_zlim(0, limit)
    ax.set_box_aspect((1, 1, 0.5))

    ax.set_title("Sistema de Coordenadas do Mundo (max|V| = 10)")
    ax.set_xlabel('Eixo X')
    ax.set_ylabel('Eixo Y')
    ax.set_zlabel('Eixo Z')

    plt.tight_layout()
    plt.show()
