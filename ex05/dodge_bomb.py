import pygame as pg
import random
import sys
import os

MAX_SHOTS = 2
main_dir = os.path.split(os.path.abspath(__file__))[0]

# ゲーム音
def load_sound(file):
    if not pg.mixer:
        return None
    file = os.path.join(main_dir, "data", file)
    try:
        sound = pg.mixer.Sound(file)
        return sound
    except pg.error:
        print("Warning, unable to load, %s" % file)
    return None

# 弾丸や爆発の画像
def load_image(file):
    file = os.path.join(main_dir, "data", file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pg.get_error()))
    return surface


class Screen:
    def __init__(self, title, wh, img_path):
        pg.display.set_caption(title) 
        self.image = pg.display.set_mode(wh)
        self.rect = self.image.get_rect()
        self.bgi_sfc = pg.image.load(img_path)
        self.bgi_rct = self.bgi_sfc.get_rect() 

    def blit(self):
        self.image.blit(self.bgi_sfc, self.bgi_rct) 


class Bird(pg.sprite.Sprite):
    key_delta = {
        pg.K_UP:    [0, -1],
        pg.K_DOWN:  [0, +1],
        pg.K_LEFT:  [-1, 0],
        pg.K_RIGHT: [+1, 0],
    }

    gun_offset = -11

    def __init__(self, img_path, ratio, xy):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(img_path)
        self.image = pg.transform.rotozoom(self.image, 0, ratio)
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.facing = -1
    

    def gunpos(self):
        pos = self.facing * self.gun_offset + self.rect.centerx
        return pos, self.rect.top

    def blit(self, scr:Screen):
        scr.image.blit(self.image, self.rect)

    def update(self, scr:Screen):
        key_dct = pg.key.get_pressed()
        for key, delta in Bird.key_delta.items():
            if key_dct[key]:
                self.rect.centerx += delta[0]
                self.rect.centery += delta[1]  
            if check_bound(self.rect, scr.rect) != (+1, +1):
                self.rect.centerx -= delta[0]
                self.rect.centery -= delta[1]
        self.blit(scr)                    


class Bomb(pg.sprite.Sprite):
    def __init__(self, color, rad, vxy, scr:Screen):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((2*rad, 2*rad)) # 正方形の空のSurface
        self.image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.image, color, (rad, rad), rad)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, scr.rect.width)
        self.rect.centery = random.randint(0, scr.rect.height)
        self.vx, self.vy = vxy

    def blit(self, scr:Screen):
        scr.image.blit(self.image, self.rect)

    def update(self, scr:Screen):
        self.rect.move_ip(self.vx, self.vy)
        yoko, tate = check_bound(self.rect, scr.rect)
        self.vx *= yoko
        self.vy *= tate
        self.blit(scr)

# 爆弾を撃つ
class Shot(pg.sprite.Sprite):
    speed = -11
    images = []

    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=pos)

    def update(self, scr:Screen):
        self.rect.move_ip(0, self.speed)
        if self.rect.top <= 0:
            self.kill()

# 爆発
class Explosion(pg.sprite.Sprite):
    defaultlife = 12
    animcycle = 3
    images = []

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        # self.image = self.images[0]
        self.image = pg.image.load("ex05/data/bomb.gif")
        self.rect = self.image.get_rect()
        self.rect.center = (100, 100)
        self.life = self.defaultlife

    def update(self, scr:Screen):
        self.life = self.life - 1
        # self.image = self.images[self.life // self.animcycle % 2]
        # if self.life <= 0:
        #     self.kill()
        # self.blit(scr) 

    def blit(self, scr:Screen):
        scr.image.blit(self.image, self.rect)


def check_bound(obj_rct, scr_rct):
    """
    第1引数：こうかとんrectまたは爆弾rect
    第2引数：スクリーンrect
    範囲内：+1／範囲外：-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1
    return yoko, tate


def main():
    clock =pg.time.Clock()
    Shot.images = [load_image("shot.gif")]

    # 練習１
    scr = Screen("負けるな！こうかとん", (1600,900), "fig/pg_bg.jpg")

    # 練習３
    # kkt = Bird("fig/6.png", 2.0, (900,400))
    

    # 練習５
    # bkd = Bomb((255, 0, 0), 10, (+1, +1), scr)
    
    # bkd = []
    colors = ["red", "green", "blue", "yellow"] # 色付きの爆弾
    # for i in range(4):
    #     color = colors[i]
    #     vx = random.choice([-1, +1]) # 一つ一つの爆弾をランダムに指定
    #     vy = random.choice([-1, +1])
    #     bkd.append(Bomb(color, 10, (vx, vy), scr))

    Explosion.containers = all
    boom_sound = load_sound("boom.wav")
    Shot.images = [load_image("shot.gif")]
    shots = pg.sprite.Group()
    Shot.containers = shots, all
    shoot_sound = load_sound("car_door.wav")

    kkt = pg.sprite.Group()
    kkt.add(Bird("fig/6.png", 2.0, (900,400)))
    bkd = pg.sprite.Group()
    for i in range(4):
        color = colors[i]
        vx = random.choice([-1, +1]) # 一つ一つの爆弾をランダムに指定
        vy = random.choice([-1, +1])
        bkd.add(Bomb(color, 10, (vx, vy), scr))
    kkt.update(scr)
    bkd.update(scr)
    exp = pg.sprite.Group()
    exp.add(Explosion())


    # 練習２
    while True:        
        scr.blit()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        kkt.update(scr)
        bkd.update(scr)
        exp.update(scr)
        # それぞれの爆弾に当たり判定を付ける
        # for bomb in bkd:
        #     bomb.update(scr)
        #     if kkt.rect.colliderect(bomb.rect):
        #         return

        # 爆弾にぶつかったとき爆発する
        # for bomb in pg.sprite.spritecollide(kkt, bkd, 1):

        if len(pg.sprite.groupcollide(kkt, bkd, False, True)) != 0:
            if pg.mixer:
                boom_sound.play()
                exp.draw(scr.image)
                # Explosion(kkt)
                # Explosion(bkd)
                # kkt.kill()

        
        keystate = pg.key.get_pressed()
        firing = keystate[pg.K_SPACE]
        if firing:
            Shot(kkt.gunpos())
            if pg.mixer:
                shoot_sound.play()
        
        

        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()