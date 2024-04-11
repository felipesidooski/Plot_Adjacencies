import matplotlib.pyplot as plt
import networkx as nx
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import mpld3

def draw_network_graph(conexoes, router_image):
    # Criar um grafo direcionado
    G = nx.DiGraph()

    # Adicionar roteador R1
    G.add_node('R1')

    # Adicionar os outros roteadores e as conexões com R1
    for conexao in conexoes:
        hl4_hostname = conexao[0]
        hl3_hostname = conexao[2]  # Nome do roteador conectado a R1
        porta_hl4 = conexao[1]  # Porta do roteador R1
        porta_hl3 = conexao[3]  # Porta do roteador conectado a R1
        G.add_node(hl3_hostname)
        G.add_edge(hl4_hostname, hl3_hostname, porta_hl3=porta_hl3, porta_hl4=porta_hl4)

    # Definir posições dos nós (para melhor visualização)
    pos = nx.spring_layout(G)

    # Carregar a imagem do roteador
    router_img = Image.open(router_image)

    # Desenhar os nós (roteadores)
    for node, (x, y) in pos.items():
        imagebox = OffsetImage(router_img, zoom=0.02)
        ab = AnnotationBbox(imagebox, (x, y), xycoords='data', frameon=False, pad=0.3)
        plt.gca().add_artist(ab)
        
        # Adicionar hostname abaixo da figura
        plt.text(x, y - 0.1, node, va='center', ha='center', fontsize=10, fontweight='bold')

    # Desenhar as arestas (conexões entre roteadores) e adicionar portas
    for u, v, d in G.edges(data=True):
        porta_hl3 = d['porta_hl3']
        porta_hl4 = d['porta_hl4']
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        plt.plot([x1, x2], [y1, y2], 'k-', lw=2)  # Desenhar linha de conexão
        
        # Calcular posição para exibir o texto das portas ao longo da linha de conexão
        text_x = (x1 + x2) / 2
        text_y = (y1 + y2) / 2
        
        # Calcular posição para exibir as portas mais próximas das imagens dos roteadores
        delta_x = 0.1 * (x2 - x1)
        delta_y = 0.1 * (y2 - y1)
        
        # Adicionar texto da porta acima e abaixo da linha de interconexão, próximo ao roteador de origem
        plt.text(text_x + delta_x, text_y + delta_y, f"{porta_hl3}", ha='center', va='center', fontsize=8)
        plt.text(text_x - delta_x, text_y - delta_y, f"{porta_hl4}", ha='center', va='center', fontsize=8)

    plt.title("Topologia")
    plt.axis('off')  # Desativar os eixos

    # Converter o gráfico matplotlib em HTML usando mpld3
    html = mpld3.fig_to_html(plt.gcf())

    # Salvar o HTML em um arquivo
    with open('topologia.html', 'w') as f:
        f.write(html)

# Lista de conexões (substitua isso com seus dados reais)
conexoes = [
    ['i-br-pr-cta-vm-hl4-01', 'GigabitEthernet0/0/0', 'i-br-pr-cta-vm-hl3-01', 'GigabitEthernet0/1/0'],
    ['i-br-pr-cta-vm-hl4-01', 'GigabitEthernet0/1/0', 'i-br-pr-cta-vm-hl4-02', 'GigabitEthernet0/0/0']
]

# Caminho para a imagem do roteador
router_image = "router.png"

# Desenhar o gráfico da rede e salvar como HTML
draw_network_graph(conexoes, router_image)
