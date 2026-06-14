from generators.world_scene_generator import generate_world_scene
from visualization.world_visualizer import visualize_world

# Questão 2
world = generate_world_scene()

print(f"Desenhando cena com {len(world)} sólidos.")
visualize_world(world)