# 🛩️ **Planejamento de Trajetória para UAV - Comparação 2D vs 3D com Dijkstra**

Este projeto simula o planejamento de rotas para **drones (UAVs)** em ambientes com obstáculos, utilizando o **Algoritmo de Dijkstra**. O sistema permite comparar o trajeto encontrado em um ambiente 2D tradicional, onde os obstáculos são absolutos, com um ambiente 3D simplificado, onde os obstáculos possuem altura e o drone pode sobrevoá-los dependendo da sua configuração de voo.

---

## 🔧 **Funcionalidades**

✅ Modelagem do ambiente 2D com obstáculos absolutos <br> 
✅ Modelagem do ambiente 3D com alturas dos obstáculos <br>
✅ Geração automática dos grafos para ambos os cenários <br>
✅ Algoritmo de Dijkstra aplicado em 2D e 3D para encontrar o menor caminho possível <br>
✅ Simulação visual lado a lado do trajeto percorrido nos dois cenários <br>
✅ Cálculo de métricas realistas: <br>
&nbsp;&nbsp;&nbsp;&nbsp;✅ Distância percorrida <br>
&nbsp;&nbsp;&nbsp;&nbsp;✅ Consumo de bateria proporcional ao tempo e à altura do voo <br>
&nbsp;&nbsp;&nbsp;&nbsp;✅ Tempo estimado de voo <br>
✅ Comparação automática dos resultados entre 2D e 3D <br>
✅ Visualização intuitiva dos obstáculos e altura no ambiente 3D <br>

---

## 🗺️ **Descrição dos Cenários**

* **Planejamento 2D:**

  * Obstáculos são considerados muros intransponíveis (valor 1 no mapa).
  * Drone precisa desviar lateralmente.
  * Simula ambientes bidimensionais tradicionais.

* **Planejamento 3D simplificado:**

  * Cada obstáculo possui uma altura definida.
  * O drone pode sobrevoar obstáculos mais baixos que sua altura de voo.
  * O trajeto pode ser otimizado em relação ao 2D, mas o voo mais alto consome mais bateria.

---

## ⚙️ **Parâmetros Configuráveis**

Os parâmetros estão centralizados no dicionário `configuracoes` no código:

```python
configuracoes = {
    'altura': 6,  # Altura do voo do drone em metros
    'velocidade': 2,  # Velocidade do drone em m/s
    'pausa_passos': 0.5,  # Pausa entre os passos na simulação
    'capacidade_bateria': 100  # Bateria inicial do drone (%)
}
```

---

## 🧑‍💻 **Tecnologias Utilizadas**

* Python 3.x
* [NetworkX](https://networkx.org/) - Manipulação de grafos
* [Matplotlib](https://matplotlib.org/) - Visualização gráfica
* [NumPy](https://numpy.org/) - Manipulação de matrizes

---

## 🚀 **Como Executar**

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/uav-path-planning.git
cd uav-path-planning
```

2. Instale as dependências:

```bash
pip install networkx matplotlib numpy
```

3. Execute a simulação:

```bash
python simulacao_uav.py
```

---

## 📊 **Exemplo de Saída Esperada**

* Visualização lado a lado dos ambientes 2D e 3D
* Animação passo a passo do trajeto percorrido
* Exibição de informações no terminal:

  * Distância total
  * Consumo estimado de bateria
  * Tempo estimado de voo
  * Caminho percorrido
* Comparação dos resultados 2D vs 3D:

  * Redução de distância
  * Economia de bateria
  * Ganho de tempo

---

## 🎯 **Possíveis Melhorias Futuras**

* Integração com algoritmos heurísticos (ex: A\*)
* Simulação de ambientes maiores e mais complexos
* Implementação de obstáculos dinâmicos ou ambientes em tempo real
* Cálculo detalhado de consumo energético baseado em física de voo realista

---

## 📚 **Referências**

* DHULKEFL, E.J.; DURDU, A.; TERZİOĞLU, H. *Dijkstra Algorithm Using UAV Path Planning*. Konya Journal of Engineering Sciences, 2020.
* CORMEN, T. et al. *Introduction to Algorithms*. MIT Press, 2009.