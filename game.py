import pygame
import math
import heapq

# inicializacao
pygame.init()

# configuracoes
largura, altura = 600, 600
linhas, colunas = 20, 20
tamanho_quadrado = largura // colunas

# cores
cores = {
    "branco": (255, 255, 255),
    "preto": (0, 0, 0),
    "vermelho": (255, 0, 0),
    "azul": (0, 0, 255),
    "amarelo": (255, 255, 0),
    "verde": (0, 255, 0),
    "cinza": (128, 128, 128)
}

# tela
tela = pygame.display.set_mode((largura, altura))

# posicoes
inicio = (0, 0)
objetivo = (colunas-1, linhas-1)
barreiras = [
    (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5),
    (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6),
]
frutas_poder = [(4, 2)]
posicao_inimigo = [8, 8]

# heuristica
def distancia_euclidiana(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

# algoritmo
def a_estrela(inicio, objetivo, barreiras, frutas_poder, tem_fruta_poder):
    def heuristica(ponto):
        return distancia_euclidiana(ponto, objetivo)
    
    def caminho_ate_fruta(ponto_inicial, frutas_poder):
        caminhos = []
        for fruta in frutas_poder:
            caminho = a_estrela(ponto_inicial, fruta, barreiras, [], tem_fruta_poder)
            if caminho:
                caminhos.append((len(caminho), caminho, fruta))
        caminhos.sort(key=lambda x: x[0])
        return caminhos[0] if caminhos else (float('inf'), [], None)
    
    if not tem_fruta_poder:
        distancia, caminho, fruta_proxima = caminho_ate_fruta(inicio, frutas_poder)
        if caminho:
            return caminho
    
    lista_aberta = []
    heapq.heappush(lista_aberta, (0, inicio))
    veio_de = {}
    pontuacao_g = {inicio: 0}
    pontuacao_f = {inicio: heuristica(inicio)}

    while lista_aberta:
        _, atual = heapq.heappop(lista_aberta)

        if atual == objetivo:
            caminho = []
            while atual in veio_de:
                caminho.append(atual)
                atual = veio_de[atual]
            caminho.append(inicio)
            return caminho[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
            vizinho = (atual[0] + dx, atual[1] + dy)
            if 0 <= vizinho[0] < colunas and 0 <= vizinho[1] < linhas:
                if vizinho in barreiras and not tem_fruta_poder:
                    continue

                pontuacao_g_tentativa = pontuacao_g[atual] + distancia_euclidiana(atual, vizinho)
                if vizinho in frutas_poder:
                    tem_fruta_poder = True

                if vizinho not in pontuacao_g or pontuacao_g_tentativa < pontuacao_g[vizinho]:
                    veio_de[vizinho] = atual
                    pontuacao_g[vizinho] = pontuacao_g_tentativa
                    pontuacao_f[vizinho] = pontuacao_g_tentativa + heuristica(vizinho)
                    heapq.heappush(lista_aberta, (pontuacao_f[vizinho], vizinho))

    return []

# grade
def desenhar_grade():
    for x in range(0, largura, tamanho_quadrado):
        for y in range(0, altura, tamanho_quadrado):
            retangulo = pygame.Rect(x, y, tamanho_quadrado, tamanho_quadrado)
            pygame.draw.rect(tela, cores["preto"], retangulo, 1)

# elementos
def desenhar_elementos():
    for barreira in barreiras:
        retangulo = pygame.Rect(barreira[0] * tamanho_quadrado, barreira[1] * tamanho_quadrado, tamanho_quadrado, tamanho_quadrado)
        pygame.draw.rect(tela, cores["vermelho"], retangulo)

    for fruta in frutas_poder:
        retangulo = pygame.Rect(fruta[0] * tamanho_quadrado, fruta[1] * tamanho_quadrado, tamanho_quadrado, tamanho_quadrado)
        pygame.draw.rect(tela, cores["amarelo"], retangulo)

    pygame.draw.rect(tela, cores["azul"], (inicio[0] * tamanho_quadrado, inicio[1] * tamanho_quadrado, tamanho_quadrado, tamanho_quadrado))
    pygame.draw.rect(tela, cores["verde"], (objetivo[0] * tamanho_quadrado, objetivo[1] * tamanho_quadrado, tamanho_quadrado, tamanho_quadrado))
    pygame.draw.rect(tela, cores["cinza"], (posicao_inimigo[0] * tamanho_quadrado, posicao_inimigo[1] * tamanho_quadrado, tamanho_quadrado, tamanho_quadrado))

# inimigo
def atualizar_posicao_inimigo():
    global posicao_inimigo
    if posicao_inimigo[1] % 2 == 0:
        posicao_inimigo[1] = (posicao_inimigo[1] + 1) % linhas
    else:
        posicao_inimigo[1] = (posicao_inimigo[1] - 1) % linhas

# principal
def principal():
    rodando = True
    tem_fruta_poder = False
    caminho = a_estrela(inicio, objetivo, barreiras, frutas_poder, tem_fruta_poder)
    indice_caminho = 0

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        atualizar_posicao_inimigo()

        if indice_caminho < len(caminho):
            posicao_atual = caminho[indice_caminho]
            if posicao_atual in frutas_poder:
                tem_fruta_poder = True
                caminho = a_estrela(posicao_atual, objetivo, barreiras, frutas_poder, tem_fruta_poder)
                indice_caminho = 0
            indice_caminho += 1

        if not caminho:
            print("Nenhum caminho encontrado!")
            rodando = False
            continue

        tela.fill(cores["branco"])
        desenhar_grade()
        desenhar_elementos()

        if indice_caminho < len(caminho):
            pygame.draw.rect(tela, cores["azul"], (caminho[indice_caminho][0] * tamanho_quadrado, caminho[indice_caminho][1] * tamanho_quadrado, tamanho_quadrado, tamanho_quadrado))
        
        pygame.display.flip()
        pygame.time.delay(500)

    pygame.quit()

if __name__ == "__main__":
    principal()
