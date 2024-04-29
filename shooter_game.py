from pygame import *
from random import *

window = display.set_mode((700, 500))
display.set_caption('Shooter Game')

clock = time.Clock()
FPS = 30

background = transform.scale(image.load("galaxy.jpg"), (700, 500))


class GameSprite(sprite.Sprite):
   def __init__(self, player_image, player_x, player_y, player_speed, sizeX, sizeY):
       super().__init__()
       self.image = transform.scale(image.load(player_image), (sizeX, sizeY))
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y

   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

bullets = sprite.Group()

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d] and self.rect.x < 620:
            self.rect.x += 5
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= 5
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 15, 20)
        bullets.add(bullet)


figure_score = 0
figure_skipped = 0    

monsters = sprite.Group()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global figure_skipped
        if self.rect.y >= 490:
            self.rect.y = -50
            self.rect.x = randint(20, 600)
            self.speed = randint(1, 3)
            figure_skipped +=1


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')

font.init()
font = font.SysFont("Arial", 30)



rocket = Player('rocket.png', 5, 400, 5, 80, 100)

win = font.render('Ты всё таки победил..', True, (0, 255, 0))
lose = font.render('КАПЕЦ ):(', True, (255, 0, 0))

for i in range(5):
    monster = Enemy('ufo.png', randint(20, 600), -50, randint(1, 3), 80, 50)
    monsters.add(monster)

finish = False
game = True
while game:  
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire.play()
                rocket.fire()

    rocket_monsters_list = sprite.spritecollide(rocket, monsters, False)
    bullets_monsters_list = sprite.groupcollide(bullets, monsters, True, True)

    if not finish:
        window.blit(background, (0, 0))
        if rocket_monsters_list or figure_skipped >= 3: 
            window.blit(lose, (200, 200))
            finish = True

        if bullets_monsters_list:
            figure_score += 1
            monster = Enemy('ufo.png', randint(20, 600), -50, randint(1, 3), 80, 50)
            monsters.add(monster)
        
        if figure_score >= 10:
            window.blit(win, (200, 200))
            finish = True


        score = font.render('Счёт: ' + str(figure_score), True, (255, 255, 255))
        skipped = font.render('Пропущено: ' +  str(figure_skipped), True, (255, 255, 255))

        window.blit(score, (10, 10))
        window.blit(skipped, (10, 30)) 
        
        monsters.draw(window)
        monsters.update()

        bullets.update()
        bullets.draw(window)
        
        rocket.reset()
        rocket.update()

        display.update()

    clock.tick(FPS)

