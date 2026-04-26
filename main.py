import pygame as pg

class MeuGame:
    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode((840, 480))
        pg.display.set_caption("Meu Jogo")
        self.clock = pg.time.Clock()

        # ---------------- MAPA ----------------
        self.map = [["" for _ in range(20)] for _ in range(7)] + [["1"] * 14 + [""] * 6]
        
        # music
        pg.mixer.music.load("data/8bit_bossa.mp3")
        pg.mixer.music.play(-1)
        
        # som de passo
        self.walk_sound = pg.mixer.Sound("data/passos.wav")
        self.walk_channel = pg.mixer.Channel(1) 
       
        # física
        self.gravity = 1

        # player
        self.player_animation = 0 
        self.player_animation_frame = 0
        self.player_pos = [50, 50]
        self.player_jump_force = -16
        self.player_vertical_speed = 0

      
        self.idle_r = [pg.transform.scale(pg.image.load(f"data/idle_right_{i}.png"), (64, 64)) for i in [1, 2]]
        self.idle_l = [pg.transform.scale(pg.image.load(f"data/idle_left_{i}.png"), (64, 64)) for i in [1, 2]]
        self.walk_r = [pg.transform.scale(pg.image.load(f"data/walk_right_{i}.png"), (64, 64)) for i in range(1, 5)]
        self.walk_l = [pg.transform.scale(pg.image.load(f"data/walk_left_{i}.png"), (64, 64)) for i in range(1, 5)]

        self.background = pg.transform.scale(pg.image.load("data/background1.png"), (840, 540))
        self.ground = pg.transform.scale(pg.image.load("data/pedra.png"), (64, 64))

    def player_collider(self):
        left_foot = self.player_pos[0] + 15
        right_foot = self.player_pos[0] + 49
        foot_y = self.player_pos[1] + 53 

        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                if self.map[y][x] != "":
                    tile_rect = pg.Rect(x * 64, y * 64, 64, 64)
                    if tile_rect.collidepoint(left_foot, foot_y) or tile_rect.collidepoint(right_foot, foot_y):
                        return True
        return False

    def move(self, keys):
        moving = False
        on_ground = self.player_vertical_speed == 0 

        if keys[pg.K_a]:
            self.player_pos[0] -= 5
            if self.player_collider(): self.player_pos[0] += 5
            else:
                self.player_animation = 3
                moving = True
        elif keys[pg.K_d]:
            self.player_pos[0] += 5
            if self.player_collider(): self.player_pos[0] -= 5
            else:
                self.player_animation = 2  
                moving = True

        
        if moving and on_ground:
          
            if not self.walk_channel.get_busy():
                self.walk_channel.play(self.walk_sound, loops=-1)
        else:
            
            self.walk_channel.stop()

        # pulo
        if keys[pg.K_SPACE] and self.player_vertical_speed == 0:
            self.player_vertical_speed = self.player_jump_force
            self.walk_channel.stop()

        # idle logic
        if not moving:
            if self.player_animation == 2: self.player_animation = 0
            elif self.player_animation == 3: self.player_animation = 1

    def player(self):
        # Gravidade
        self.player_vertical_speed += self.gravity
        self.player_pos[1] += self.player_vertical_speed

        if self.player_collider():
            self.player_pos[1] -= self.player_vertical_speed
            self.player_vertical_speed = 0

        # --- LÓGICA DE ANIMAÇÃO ---
        self.player_animation_frame += 0.05
        
        if self.player_animation == 0: 
            img_list = self.idle_r
        elif self.player_animation == 1: 
            img_list = self.idle_l
        elif self.player_animation == 2:
            img_list = self.walk_r
        elif self.player_animation == 3:
            img_list = self.walk_l

        if self.player_animation_frame >= len(img_list):
            self.player_animation_frame = 0

        self.window.blit(img_list[int(self.player_animation_frame)], self.player_pos)

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
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                exit()
        
    keys = pg.key.get_pressed()
    jogo.move(keys)

    jogo.window.blit(jogo.background, (0, 0))
    jogo.draw_map()
    jogo.player()

    pg.display.update()
    jogo.clock.tick(60)