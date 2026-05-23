import numpy as np
import matplotlib.pyplot as plt


def visualize_solid(solid):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    verts = solid['vertices']
    faces = solid['faces']

    x = verts[:, 0]
    y = verts[:, 1]
    z = verts[:, 2]

    # Renderiza a malha triangular
    ax.plot_trisurf(x, y, z, triangles=faces, edgecolor='black', facecolor='white', alpha=0.8, linewidth=0.2)

    # AJUSTE DE PROPORÇÃO (ASPECT RATIO)
    # O matplotlib tende a distorcer eixos 3D. Esse cálculo garante que a peça
    # não pareça "esmagada" ou "esticada", forçando o mesmo scale em X, Y e Z.
    max_range = np.array([x.max() - x.min(), y.max() - y.min(), z.max() - z.min()]).max() / 2.0
    mid_x = (x.max() + x.min()) * 0.5
    mid_y = (y.max() + y.min()) * 0.5
    mid_z = (z.max() + z.min()) * 0.5

    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    ax.set_title(f"Sólido: {solid['name']}")
    ax.set_xlabel('Eixo X')
    ax.set_ylabel('Eixo Y')
    ax.set_zlabel('Eixo Z')

    plt.tight_layout()
    plt.show()
