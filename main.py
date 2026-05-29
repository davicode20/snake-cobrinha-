import pygame
import random
import sys

# Inicialização do pygame
pygame.init()

# =========================
# CONFIGURAÇÕES
# =========================
LARGURA = 600
ALTURA = 600
TAMANHO_BLOCO = 30
FPS = 10

# =========================
# CORES
# =========================
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERDE_ESCURO = (0, 180, 0)
BRANCO = (255, 255, 255)
CINZA = (40, 40, 40)

# =========================
# TELA
# =========================
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Snake do Professor KKKKK")

# Relógio
clock = pygame.time.Clock()

# Fonte
fonte = pygame.font.SysFont("Arial", 28)

# =========================
# IMAGENS
# =========================

# Cabeça da cobra
rosto_professor = pygame.image.load("professor.png").convert_alpha()

rosto_professor = pygame.transform.scale(
    rosto_professor,
    (TAMANHO_BLOCO + 30, TAMANHO_BLOCO + 30)
)

# Comida Python
comida_python = pygame.image.load("python_food.png").convert_alpha()

comida_python = pygame.transform.scale(
    comida_python,
    (TAMANHO_BLOCO + 20, TAMANHO_BLOCO + 20)
)

# =========================
# FUNÇÕES
# =========================
def desenhar_grade():
    for x in range(0, LARGURA, TAMANHO_BLOCO):
        pygame.draw.line(screen, CINZA, (x, 0), (x, ALTURA))

    for y in range(0, ALTURA, TAMANHO_BLOCO):
        pygame.draw.line(screen, CINZA, (0, y), (LARGURA, y))


def gerar_comida(cobra):
    while True:
        comida_x = random.randrange(0, LARGURA, TAMANHO_BLOCO)
        comida_y = random.randrange(0, ALTURA, TAMANHO_BLOCO)

        if (comida_x, comida_y) not in cobra:
            return comida_x, comida_y


def desenhar_comida(x, y):
    screen.blit(
        comida_python,
        (x - 10, y - 10)
    )


def desenhar_cobra(cobra, direcao_x, direcao_y):
    for i, segmento in enumerate(cobra):
        x, y = segmento

        # =========================
        # CABEÇA DO PROFESSOR
        # =========================
        if i == 0:

            rosto_rotacionado = rosto_professor

            # Direita
            if direcao_x > 0:
                rosto_rotacionado = rosto_professor

            # Esquerda
            elif direcao_x < 0:
                rosto_rotacionado = pygame.transform.flip(
                    rosto_professor,
                    True,
                    False
                )

            # Cima
            elif direcao_y < 0:
                rosto_rotacionado = pygame.transform.rotate(
                    rosto_professor,
                    90
                )

            # Baixo
            elif direcao_y > 0:
                rosto_rotacionado = pygame.transform.rotate(
                    rosto_professor,
                    -90
                )

            screen.blit(
                rosto_rotacionado,
                (x - 15, y - 15)
            )

        # =========================
        # CORPO
        # =========================
        else:
            pygame.draw.rect(
                screen,
                VERDE_ESCURO,
                (x + 2, y + 2, TAMANHO_BLOCO - 4, TAMANHO_BLOCO - 4),
                border_radius=5,
            )


def mostrar_texto(texto, cor, y_offset=0):
    superficie = fonte.render(texto, True, cor)
    rect = superficie.get_rect(center=(LARGURA // 2, ALTURA // 2 + y_offset))
    screen.blit(superficie, rect)


def tela_game_over(pontuacao):
    while True:
        screen.fill(PRETO)

        mostrar_texto("GAME OVER", BRANCO, -40)
        mostrar_texto(f"Pontuação: {pontuacao}", BRANCO, 10)
        mostrar_texto("ENTER = Jogar novamente", BRANCO, 60)
        mostrar_texto("ESC = Sair", BRANCO, 100)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    jogo()

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def jogo():

    # Cobra
    cobra = [(300, 300)]

    # Direção inicial
    direcao_x = TAMANHO_BLOCO
    direcao_y = 0

    # Comida
    comida_x, comida_y = gerar_comida(cobra)

    # Pontuação
    pontuacao = 0

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # Movimento
                if event.key == pygame.K_UP and direcao_y == 0:
                    direcao_x = 0
                    direcao_y = -TAMANHO_BLOCO

                elif event.key == pygame.K_DOWN and direcao_y == 0:
                    direcao_x = 0
                    direcao_y = TAMANHO_BLOCO

                elif event.key == pygame.K_LEFT and direcao_x == 0:
                    direcao_x = -TAMANHO_BLOCO
                    direcao_y = 0

                elif event.key == pygame.K_RIGHT and direcao_x == 0:
                    direcao_x = TAMANHO_BLOCO
                    direcao_y = 0

        # Nova posição
        head_x = cobra[0][0] + direcao_x
        head_y = cobra[0][1] + direcao_y

        nova_cabeca = (head_x, head_y)

        # Colisão parede
        if (
            head_x < 0
            or head_x >= LARGURA
            or head_y < 0
            or head_y >= ALTURA
        ):
            tela_game_over(pontuacao)

        # Colisão corpo
        if nova_cabeca in cobra:
            tela_game_over(pontuacao)

        # Adiciona cabeça
        cobra.insert(0, nova_cabeca)

        # Comer comida
        if head_x == comida_x and head_y == comida_y:
            pontuacao += 1
            comida_x, comida_y = gerar_comida(cobra)

        else:
            cobra.pop()

        # =========================
        # DESENHAR
        # =========================
        screen.fill(PRETO)

        desenhar_grade()

        # Comida
        desenhar_comida(comida_x, comida_y)

        # Cobra
        desenhar_cobra(cobra, direcao_x, direcao_y)

        # Pontuação
        texto_pontos = fonte.render(
            f"Pontos: {pontuacao}",
            True,
            BRANCO
        )

        screen.blit(texto_pontos, (10, 10))

        pygame.display.update()


# =========================
# INICIAR
# =========================
jogo()