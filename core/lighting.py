import numpy as np

def normalize(v):
    """Retorna o vetor normalizado. Se a magnitude for 0, retorna o próprio vetor."""
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def compute_phong_lighting(vertex_cam, normal_cam, light_pos_cam, base_color, light_params):
    """
    Calcula o RGB de um vértice utilizando o Modelo de Reflexão de Phong.
    """
    Ka = light_params.get('Ka', 0.6)
    Kd = light_params.get('Kd', 0.7)
    Ks = light_params.get('Ks', 0.5)
    shininess = light_params.get('shininess', 32)

    L = normalize(light_pos_cam - vertex_cam)
    N = normalize(normal_cam)
    V = normalize(-vertex_cam) # Câmera está na origem (0,0,0) no Camera Space

    # Componente Ambiente
    ambient = Ka * base_color

    # Componente Difusa
    dot_nl = np.dot(N, L)
    diffuse = np.array([0.0, 0.0, 0.0])
    if dot_nl > 0:
        diffuse = Kd * dot_nl * base_color

    # Componente Especular
    specular = np.array([0.0, 0.0, 0.0])
    if dot_nl > 0:
        R = normalize(2.0 * dot_nl * N - L)
        dot_rv = np.dot(R, V)
        if dot_rv > 0:
            spec_intensity = (dot_rv ** shininess)
            specular = Ks * spec_intensity * np.array([255.0, 255.0, 255.0])

    final_color = ambient + diffuse + specular
    return np.clip(final_color, 0, 255).astype(int)