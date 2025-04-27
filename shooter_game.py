#Создай собственный Шутер!

from pygame import *
from random import randint
from time import *


window = display.set_mode((1000, 500))
display.set_caption('шутер')
galaxy = transform.scale(image.load("galaxy.jpg"),(1000, 500))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg ')

game = True
#clock = time.Clock()
FPS = 60

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Rocket(GameSprite):      
    def move(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 20:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 950:
            self.rect.x += self.speed
        # if keys[K_UP] and self.rect.x > 0:
        #     self.rect.y -= self.speed
        # if keys[K_DOWN] and self.rect.y < 690:
        #     self.rect.y += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15)
        bullets.add(bullet)

monsters = sprite.Group()

bullets = sprite.Group()

health = 3

lost = 0



class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        global health
        if self.rect.y >= 500:
            self.rect.x = randint(0, 900)
            self.rect.y = 0
            lost = lost + 1
            if lost == 4 or lost == 8 or lost == 12:
                health -= 1

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(image.load(player_image), (65, 65))
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
        


    


        
for i in range(5):
    enemy = Enemy('ufo.png', randint(100, 900), 0, 0.5)
    monsters.add(enemy)
            

player = Rocket('rocket.png', 500, 420, 10)
#enemy = Enemy('ufo.png', randint(100, 900), 0, 2)

score = 0


finish = False

font.init()
font1 = font.Font(None, 36)
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()
    if not finish:
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for c in sprites_list:
            score = score + 1
            enemy = Enemy('ufo.png', randint(100, 900), 0, 0.5)
            monsters.add(enemy)
        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        text_win = font1.render('Убито: ' + str(score), 1, (255, 255,255))
        text_health = font1.render('Жизней: ' + str(health), 1, (255, 255,255))
        if lost >= 12:                                                                         
                galaxy = transform.scale(image.load("lose.jpg"),(1000, 500))
                
                finish = True
                for i in monsters:
                    i.kill()
                player.kill()
                for i in bullets:
                    i.kill()
                sleep(5)
        if score >= 100:
            galaxy = transform.scale(image.load("images(2).jpg"),(1000, 500))
            finish = True
            for i in monsters:
                i.kill()
                player.kill()
            for i in bullets:
                i.kill()
            sleep(5)
        if health == 0:
            finish = True
            galaxy = transform.scale(image.load("lose.jpg"),(1000, 500))
            sleep(5)

        window.blit(galaxy,(0,0))
        player.reset()
        player.move()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window )
        window.blit(text_lose, (100, 100))
        window.blit(text_win, (100, 60))
        window.blit(text_health, (100, 20))
        display.update()
        #clock.tick(FPS)
    