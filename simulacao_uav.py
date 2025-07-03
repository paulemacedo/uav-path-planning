import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import time

# --------------------------
# Configurações
# --------------------------

# Mapa de obstáculos 2D (0 = livre, 1 = obstáculo absoluto)
mapa_2d = np.array([
    [0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0]
])

# Mapa de alturas para o 3D (0 = livre, outros = altura do obstáculo)
mapa_3d = np.array([
    [0, 0, 0, 0, 0],
    [0, 7, 2, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 2, 4, 6],
    [0, 0, 0, 0, 0]
])

# Configurações do drone
configuracoes = {
    'altura': 6,  
    'velocidade': 2,  
    'pausa_passos': 0.5,  
    'capacidade_bateria': 100
}

inicio = (0, 0)  # Ponto de partida
fim = (4, 4)  # Ponto de chegada

def calcular_consumo_bateria(distancia, altura, velocidade):
    tempo_voo = distancia / velocidade  # tempo de voo em segundos
    fator_altura = 1 + (altura / 100) * 0.3  # penalidade por altura
    consumo_percentual = tempo_voo * fator_altura * 2.5  # consumo em % por segundo
    return consumo_percentual

def calcular_metricas_voo(caminho, altura_drone, velocidade):
    distancia = len(caminho) - 1
    tempo = distancia / velocidade
    consumo = calcular_consumo_bateria(distancia, altura_drone, velocidade)

    return {
        'distancia': distancia,
        'tempo': tempo,
        'consumo_bateria': consumo,
        'caminho': caminho
    }
    

# --------------------------
# Funções para geração dos grafos
# --------------------------

def gerar_grafo_2d(mapa):
    G = nx.Graph()
    linhas, colunas = mapa.shape

    for i in range(linhas):
        for j in range(colunas):
            if mapa[i, j] == 0:
                G.add_node((i, j))

    # Conectar nós adjacentes
    for i in range(linhas):
        for j in range(colunas):
            if mapa[i, j] == 0:
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < linhas and 0 <= nj < colunas:
                        if mapa[ni, nj] == 0:
                            G.add_edge((i, j), (ni, nj), weight=1)
    return G

def gerar_grafo_3d(mapa, altura_drone):
    G = nx.Graph()
    linhas, colunas = mapa.shape

    for i in range(linhas):
        for j in range(colunas):
            if mapa[i, j] < altura_drone:
                G.add_node((i, j))


    # Conectar nós adjacentes considerando a altura
    for i in range(linhas):
        for j in range(colunas):
            if mapa[i, j] < altura_drone:
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < linhas and 0 <= nj < colunas:
                        if mapa[ni, nj] < altura_drone:
                            G.add_edge((i, j), (ni, nj), weight=1)
    return G

# --------------------------
# Função de simulação
# --------------------------

def simular_voo(grafo, mapa_visual, altura_drone, titulo, ax):
    ax.set_xlim(-0.5, mapa_visual.shape[1] - 0.5)
    ax.set_ylim(-mapa_visual.shape[0] + 0.6, 0.6)
    ax.set_aspect('equal')  # Mantém a proporção 1:1 dos eixos

    try:
        caminho = nx.shortest_path(grafo, source=inicio, target=fim, weight='weight')
    except nx.NetworkXNoPath:
        ax.set_title(titulo + " - Sem caminho possível")
        return

    distancia_total = len(caminho) - 1  # cada passo = 1 metro
    consumo_bateria = calcular_consumo_bateria(distancia_total, altura_drone, configuracoes['velocidade'])
    tempo_estimado = distancia_total / configuracoes['velocidade']

    metricas = calcular_metricas_voo(caminho, altura_drone, configuracoes['velocidade'])

    print(f"\n===== {titulo} =====")
    print(f"Distância total: {distancia_total}m")
    print(f"Consumo estimado de bateria: {consumo_bateria:.2f} unidades")
    print(f"Tempo estimado de voo: {tempo_estimado:.2f} segundos")
    print("Caminho percorrido:", " -> ".join(str(p) for p in caminho))

    pos = { (i,j): (j, -i) for i in range(mapa_visual.shape[0]) for j in range(mapa_visual.shape[1]) }
    nx.draw(grafo, pos, with_labels=False, node_color='lightblue', node_size=500, ax=ax)

    visualizar_obstaculos(mapa_visual, altura_drone, titulo, ax)

    # Início e fim
    ax.scatter(inicio[1], -inicio[0], color='green', s=800, marker='o', label='Início', edgecolor='darkgreen', linewidth=2, zorder=3)
    ax.scatter(fim[1], -fim[0], color='red', s=800, marker='o', label='Destino', edgecolor='darkred', linewidth=2, zorder=3)

    ax.set_title(titulo, fontsize=12, fontweight='bold')

 

    # Simulação passo a passo
    for idx in range(len(caminho)-1):
        ni, nj = caminho[idx]
        pi, pj = caminho[idx+1]
        ax.plot([nj, pj], [-ni, -pi], color='darkblue', linewidth=3, zorder=1)
        plt.pause(configuracoes['pausa_passos'])


   # Informações no gráfico (mostrar só ao final da animação)
    linhas, colunas = mapa_visual.shape

    # Garante que toda a caixa de texto fique visível


    plt.subplots_adjust(left=0.13, bottom=0.18)

    x_text = 0.1
    y_text = -mapa_visual.shape[0] + 0.6  # Ajuste para ficar dentro do grid


    # Exibir informações após a animação
    info_text = (
        f"Distância: {distancia_total} m\n"
        f"Bateria: {consumo_bateria:.2f} %\n"
        f"Tempo: {tempo_estimado:.2f} s\n"
        f"Passos: {len(caminho)}\n"
        f"Velocidade: {configuracoes['velocidade']} m/s"
    )
    if titulo == "3D - Considerando Altura":
        info_text += f"\nAltura: {altura_drone} m"

    ax.text(
        x_text, y_text, info_text,
        fontsize=9,  # Fonte menor
        bbox=dict(facecolor='#f0f8ff', edgecolor="#8c46b4", boxstyle='round,pad=0.6', alpha=0.95),
        ha='left', va='top', fontweight='bold', family='monospace',
        wrap=True  # Quebra automática de linha (matplotlib >=3.4)
    )

    return metricas


def visualizar_obstaculos(mapa, altura_drone, titulo, ax):
    for i in range(mapa.shape[0]):
        for j in range(mapa.shape[1]):
            valor = mapa[i, j]
            x, y = j, -i

            if titulo == "3D - Considerando Altura":
                if valor > 0 and valor < altura_drone:
                    ax.scatter(x, y, color='gray', s=600, marker='s', alpha=0.7)
                elif valor == 0:
                    ax.scatter(x, y, color='white', s=600)
                else:
                    ax.scatter(x, y, color='black', s=600, marker='s' )

                
                if valor > 0:
                    ax.text(x, y, f"{int(valor)}", color='white', ha='center', va='center', fontsize=9, fontweight='bold')
            else:  # Mapa 2D
                if valor == 1:
                    ax.scatter(x, y, color='black', s=600, marker='s')

def comparar_resultados(resultado_2d, resultado_3d):
    print("=" * 50)
    print("Analise comparativa dos resultados")
    print("=" * 50)

    if resultado_2d and resultado_3d:
        #calculos de melhoria
        reducao_distancia = (resultado_2d['distancia'] - resultado_3d['distancia']) / resultado_2d['distancia'] * 100
        reducao_tempo = (resultado_2d['tempo'] - resultado_3d['tempo']) / resultado_2d['tempo'] * 100
        diferenca_bateria = (resultado_2d['consumo_bateria'] - resultado_3d['consumo_bateria']) / resultado_2d['consumo_bateria'] * 100
        
        print(f"2D - Distância: {resultado_2d['distancia']}m | Tempo: {resultado_2d['tempo']:.2f}s | Bateria: {resultado_2d['consumo_bateria']:.2f}%")
        print(f"3D - Distância: {resultado_3d['distancia']}m | Tempo: {resultado_3d['tempo']:.2f}s | Bateria: {resultado_3d['consumo_bateria']:.2f}%")

        print(f"\nVantagem da navegação 3D:")
        print(f"  Redução de distância: {reducao_distancia:.2f}%")
        print(f"  Redução de tempo: {reducao_tempo:.2f}%")
        print(f"  Economia de bateria: {diferenca_bateria:.2f}%")

        if reducao_distancia > 0:
            print(f"\nA navegação 3D é mais eficiente neste cenário!")
        else:
            print(f"\nA navegação 2D foi mais eficiente neste caso.")
    else:
        print("Não foi possível comparar os resultados, pois um dos cenários não possui caminho viável.")
# --------------------------
# Execução
# --------------------------

def main():

    print("Simulação de planejamento de trajetória para UAV")
    print("Algoritmo: Dijkstra | Comparação 2D vs 3D")
    print("="*60)
    
    print(f"\nConfigurações do Drone:")
    print(f"• Altura de voo: {configuracoes['altura']}m")
    print(f"• Velocidade: {configuracoes['velocidade']}m/s")
    print(f"• Capacidade da bateria: {configuracoes['capacidade_bateria']}%")
    
    print("\n===== MAPA 2D (0=livre, 1=obstáculo) =====")
    print(mapa_2d)
    
    print("\n===== MAPA 3D - Alturas dos obstáculos =====")
    print(mapa_3d)


    grafo_2d = gerar_grafo_2d(mapa_2d)
    grafo_3d = gerar_grafo_3d(mapa_3d, configuracoes['altura'])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle("Simulação de Trajetória UAV: 2D vs 3D", fontsize=14, fontweight='bold')

    # Simulação e exibição dos resultados
    resultado_2d = simular_voo(grafo_2d, mapa_2d, 0, "2D - Obstáculos Absolutos", ax1)
    resultado_3d = simular_voo(grafo_3d, mapa_3d, configuracoes['altura'], "3D - Considerando Altura", ax2)

    comparar_resultados(resultado_2d, resultado_3d)

    plt.show()


if __name__ == "__main__":
    main()