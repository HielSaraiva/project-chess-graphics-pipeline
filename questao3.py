from generators.world_scene_generator import generate_world_scene
from transforms.camera_transforms import render_camera_view

# Questão 3
world_scene = generate_world_scene()

target_point = [0, 0, 0]
up_vector = [0, 0, 1]

# Câmera 1: Olhando de cima e na diagonal (Visão Isométrica)
eye_1 = [15, 15, 15]
render_camera_view(world_scene, eye_1, target_point, up_vector, "Visão Diagonal")

# Câmera 2: Olhando bem de baixo, quase no nível do chão do eixo Y
eye_2 = [0, -20, 2]
render_camera_view(world_scene, eye_2, target_point, up_vector, "Visão do Chão")