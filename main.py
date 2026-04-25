import pygame
pygame.init()

# Inicializando o pygame e criando uma janela
screen = pygame.display.set_mode([840, 480])
pygame.display.set_caption('Meu Super Jogo')


drawGroup = pygame.sprite.Group()

background = pygame.sprite.Sprite(drawGroup)
background.image = pygame.image.load("data/imagem_de_fundo.png")
background.image = pygame.transform.scale(background.image, [840,480])
background.rect = background.image.get_rect()


#personagem
urso = pygame.sprite.Sprite(drawGroup)
urso.image = pygame.image.load("data/senhor_urso.png")
urso.image = pygame.transform.scale(urso.image, [50,50])
urso.rect = urso.image.get_rect()
urso.rect.center = (420, 240)

#music
pygame.mixer.music.load("data/8bit_bossa.mp3")
pygame.mixer.music.play(-1)

#draw
def draw():
    cor_de_fundo = [19, 173, 235]
    screen.fill(cor_de_fundo)
    drawGroup.draw(screen)


#sounds
walk = pygame.mixer.Sound("data/passos.wav")
walking = False

gameLoop = True
clock = pygame.time.Clock()

while gameLoop:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameLoop = False

        elif event.type == pygame.KEYDOWN:
         if event.key in (pygame.K_d, pygame.K_a):
            if not walking:
                walk.play(-1)  # loop infinito
                walking = True

        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_d, pygame.K_a):
                walk.stop()
                walking = False


    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        urso.rect.x -= 1
    
    elif keys[pygame.K_d]:
        urso.rect.x += 1
    

    draw()
    pygame.display.update()
