import pygame as pg

class MeuGame:
    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode((840, 480))
        pg.display.set_caption("Meu Jogo")

        self.clock = pg.time.Clock()

        # ---------------- MAPA (FORMA EXPLÍCITA) ----------------
        self.map = [
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "", "", "", "", "", ""],]
        
        
        # física
        self.gravity = 1

        # player
        self.player_animation = 0
        self.player_animation_frame = 0.1
        self.player_pos = [50, 50]
        self.player_jump_force = -12
        self.player_vertical_speed = 0
        self.player_box_colider = [46, 54]

        # direita
        self.player_idle_1 = pg.transform.scale(pg.image.load("data/senhor_urso.png"), (64, 64))
        self.player_idle_2 = pg.transform.scale(pg.image.load("data/respiracao.png"), (64, 64))
        self.player_idle_3 = pg.transform.scale(pg.image.load("data/corrida.png"), (64, 64))

        # esquerda
        self.player_idle_left_1 = pg.transform.scale(pg.image.load("data/virado_esquerda.png"), (64, 64))
        self.player_idle_left_2 = pg.transform.scale(pg.image.load("data/respiracao_left.png"), (64, 64))
        self.player_idle_left_3 = pg.transform.scale(pg.image.load("data/run_left.png"), (64, 64))

        # background
        self.background = pg.transform.scale(pg.image.load("data/background.jpeg"), (840, 480))

        # chão
        self.ground = pg.transform.scale(pg.image.load("data/pedra.png"), (64, 64))

    # ---------------- COLLISÃO ----------------
    def player_collider(self):
    # pés do player
        left_foot = self.player_pos[0] + 10
        right_foot = self.player_pos[0] + 54
        foot_y = self.player_pos[1] + 64  # base do sprite

        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                if self.map[y][x] != "":
                    tile_x = x * 64
                    tile_y = y * 64

                    if (tile_x <= left_foot <= tile_x + 64 or
                        tile_x <= right_foot <= tile_x + 64):

                        if tile_y <= foot_y <= tile_y + 20:
                            return True
        return False
        # ---------------- MOVIMENTO ----------------
    def move(self, keys):
        moving = False

        # esquerda
        if keys[pg.K_a]:
            self.player_pos[0] -= 5
            if self.player_collider():
                self.player_pos[0] += 5
            else:
                self.player_animation = 3
                moving = True

        # direita
        if keys[pg.K_d]:
            self.player_pos[0] += 5
            if self.player_collider():
                self.player_pos[0] -= 5
            else:
                self.player_animation = 2
                moving = True

        # pulo
        if keys[pg.K_SPACE] and self.player_vertical_speed == 0:
            self.player_vertical_speed = self.player_jump_force

        # idle
        if not moving:
            if self.player_animation == 2:
                self.player_animation = 0
            elif self.player_animation == 3:
                self.player_animation = 1

    # ---------------- PLAYER ----------------
    def player(self):
        self.player_vertical_speed += self.gravity
        self.player_pos[1] += self.player_vertical_speed

        if self.player_collider():
            self.player_pos[1] -= self.player_vertical_speed
            self.player_vertical_speed = 0

        # animação
        self.player_animation_frame += 1
        if self.player_animation_frame > 20:
            self.player_animation_frame = 0

        # direita
        if self.player_animation == 0:
            if self.player_animation_frame < 10:
                self.window.blit(self.player_idle_1, self.player_pos)
            else:
                self.window.blit(self.player_idle_2, self.player_pos)

        elif self.player_animation == 2:
            self.window.blit(self.player_idle_3, self.player_pos)

        # esquerda
        elif self.player_animation == 1:
            if self.player_animation_frame < 10:
                self.window.blit(self.player_idle_left_1, self.player_pos)
            else:
                self.window.blit(self.player_idle_left_2, self.player_pos)

        elif self.player_animation == 3:
            self.window.blit(self.player_idle_left_3, self.player_pos)

    # ---------------- MAPA ----------------
    def draw_map(self):
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                if self.map[y][x] != "":
                    self.window.blit(self.ground, (x * 64, y * 64))


# ---------------- LOOP ----------------
jogo = MeuGame()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    if event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
            pg.quit()
            quit()
        
    keys = pg.key.get_pressed()
    jogo.move(keys)

    jogo.clock.tick(60)

    jogo.window.blit(jogo.background, (0, 0))
    jogo.draw_map()
    jogo.player()

    pg.display.update()