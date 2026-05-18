# Pipeline Gráfico de Xadrez e Dama

## Objetivo do Projeto

Implementar um pipeline gráfico completo (do modelo 3D até a rasterização 2D) para visualizar peças de xadrez e dama com iluminação, projeção perspectiva e renderização em múltiplas resoluções.

---

## Etapas do Pipeline

---

### 1. Modelagem de Sólidos

- **1 peça de dama**
- **4 peças diferentes de xadrez**

Para cada sólido:
- Criar uma malha de polígonos (triângulos) usando algoritmo próprio ou Marching Cubes
- Cada polígono possui normal à superfície apontando para fora do sólido
- Função que retorna: matriz de vértices, arestas, faces e atributos

---

### 2. Composição de Cena no Sistema de Coordenadas do Mundo

- Distribuir sólidos sem sobreposição ou intersecção
- Aplicar transformações: escala, rotação e translação
- **Restrição**: máximo valor absoluto de qualquer componente de vértice = |10|
- Visualizar sólidos em 3D

---

### 3. Sistema de Coordenadas da Câmera

- Definir ponto de origem (eye) para o sistema de coordenadas da câmera
- Computar base vetorial do novo sistema de coordenadas
- Transformar objetos do sistema de coordenadas do mundo para câmera
- Visualizar sólidos em 3D no novo sistema
- Marcar a origem do sistema de coordenadas do mundo
- Permitir variação do ponto eye (gerar nova imagem dinamicamente)

---

### 4. Projeção em Perspectiva (3D → 2D)

- Aplicar transformação de projeção perspectiva
- Projetar polígonos no plano de projeção 2D
- Descartar polígonos não visíveis (back-face culling)
- Cores: mesmo sólido = mesma cor (arestas e faces); sólidos diferentes = cores diferentes
- Apresentar objetos em 2D

---

### 5. Iluminação

Aplicar iluminação Phong nos vértices dos polígonos visíveis:
- Componente ambiente
- Componente difusa
- Componente especular
- Calcular RGB dos vértices

---

### 6. Rasterização

- Rasterizar objetos em **pelo menos 3 resoluções diferentes**
- Eliminar polígonos ocultos (z-buffer/depth test usando normal e eixo z da câmera)
- Algoritmo: rasterização par-ímpar com scan line
- Calcular cores dos pixels rasterizados usando **interpolação baricêntrica**

---

## Equipe

- **Hiel Saraiva**
- **Roberta Alanis**
- **André Lucas**
