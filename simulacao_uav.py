import networkx as nx
import matplotlib.pyplot as plt

# Mapa base: 0 = espaço livre, 1 = obstáculo intransponível
mapa_2d = [
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
]

# Mapa 3D: 0 = espaço livre, 
mapa_3d = [
    [0, 0, 0, 0, 0],
    [0, 5, 10, 0, 0],
    [0, 0, 0, 7, 0],
    [0, 8, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

altura_drone = 6 # Altura do drone em relação ao mapa 3D
