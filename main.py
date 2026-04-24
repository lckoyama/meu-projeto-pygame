import pygame
pygame.init()

#Inicializando o pygame e criando uma janela
screen = pygame.display.set_mode([840,480])
pygame.display.set_caption('Meu Super Jogo')

def draw():
    cor_de_fundo = ([19, 173, 235])
    screen.fill(cor_de_fundo)





gameLoop = True
while gameLoop:
    draw()
    pygame.display.update()