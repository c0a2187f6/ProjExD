import pygame as pg
import random
import sys


def check_bound(obj_rct, scr_rct):
    # 第1引数：こうかとんrectまたは爆弾rect
    # 第2引数：スクリーンrect
    # 範囲内：+1／範囲外：-1
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1
    return yoko, tate


def main():
    clock =pg.time.Clock()
    # 練習１
    pg.display.set_caption("逃げろ！こうかとん")
    scrn_sfc = pg.display.set_mode((1600, 900))
    scrn_rct = scrn_sfc.get_rect()
    pgbg_sfc = pg.image.load("fig/pg_bg.jpg")
    pgbg_rct = pgbg_sfc.get_rect()

    # 練習３
    tori_sfc = pg.image.load("fig/6.png")
    tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.center = 900, 400
    # scrn_sfcにtori_rctに従って，tori_sfcを貼り付ける
    scrn_sfc.blit(tori_sfc, tori_rct) 

    # 練習５
    bomb_sfc = pg.Surface((20, 20)) # 正方形の空のSurface
    bomb_sfc.set_colorkey((0, 0, 0))
    pg.draw.circle(bomb_sfc, (255, 0, 0), (10, 10), 10) # 爆弾っぽいデザイン
    pg.draw.circle(bomb_sfc, (191, 0, 0), (10, 10), 8)
    pg.draw.circle(bomb_sfc, (127, 0, 0), (10, 10), 6)
    pg.draw.circle(bomb_sfc, (63, 0, 0), (10, 10), 4)
    pg.draw.circle(bomb_sfc, (0, 0, 0), (10, 10), 2)
    bomb_rct = bomb_sfc.get_rect()
    bomb_rct.centerx = random.randint(0, scrn_rct.width)
    bomb_rct.centery = random.randint(0, scrn_rct.height)
    scrn_sfc.blit(bomb_sfc, bomb_rct)  
    vx, vy = +1, +1

    hit = False
    fonto = pg.font.Font(None, 80)
    hpnum = 3
    hp = fonto.render((f"LIFE: {hpnum}"), True, (255, 0, 0)) # 残り体力の表示
    gmov = fonto.render("Game Over", True, (255, 0, 0)) # ゲームオーバーの表示(時間不足で未実装)
    muteki = 0 # 無敵時間

    # 練習２
    while True:
        scrn_sfc.blit(pgbg_sfc, pgbg_rct) 
        scrn_sfc.blit(hp, (300, 200))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        # 練習4
        key_dct = pg.key.get_pressed()
        if key_dct[pg.K_UP]:
            tori_rct.centery -= 1
        if key_dct[pg.K_DOWN]:
            tori_rct.centery += 1
        if key_dct[pg.K_LEFT]:
            tori_rct.centerx -= 1
        if key_dct[pg.K_RIGHT]:
            tori_rct.centerx += 1
        if check_bound(tori_rct, scrn_rct) != (+1, +1):
            # はみ出ていたら
            if key_dct[pg.K_UP]:
                tori_rct.centery += 1
            if key_dct[pg.K_DOWN]:
                tori_rct.centery -= 1
            if key_dct[pg.K_LEFT]:
                tori_rct.centerx += 1
            if key_dct[pg.K_RIGHT]:
                tori_rct.centerx -= 1            
        scrn_sfc.blit(tori_sfc, tori_rct) 

        # 練習６
        bomb_rct.move_ip(vx, vy)
        scrn_sfc.blit(bomb_sfc, bomb_rct) 
        yoko, tate = check_bound(bomb_rct, scrn_rct)
        vx *= yoko
        vy *= tate

        
        if pg.time.get_ticks() > muteki: # 現在の時間が無敵時間より大きい
          hit = False 
        # 練習８
        if tori_rct.colliderect(bomb_rct):
          if not hit: # 無敵状態
            hpnum -= 1
            hit = True
            muteki = pg.time.get_ticks() + 1000
          hp = fonto.render((f"LIFE: {hpnum}"), True, (255, 0, 0))
          hit = True
          scrn_sfc.blit(hp, (300, 200))
          pg.display.update()
          if hpnum < 1:
            scrn_sfc.blit(gmov, (300, 200))
            return  

        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()

    pg.quit()
    sys.exit()
