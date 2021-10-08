import pygame
from pygame import mixer
import time
pygame.init()
mixer.init()
import sys
from pygame.locals import *

### 画面初期化
surface = pygame.display.set_mode((960, 320))

### キーリピート設定
pygame.key.set_repeat(100,100)

### フォントリスト取得
list = []
for x in pygame.font.get_fonts():
    list.append(x)

### リスト位置初期化
i = 0

### 無限ループ
while True:

    ### 背景色設定
    surface.fill((0,0,0))

    ### フォント設定
    font = pygame.font.SysFont(list[i], 30)

    ### 表示文字設定
    name = font.render("{}".format(list[i]), True, (255,255,255))
    numb = font.render("1234567890", True, (255,255,255))
    asci = font.render("ABCDEFGHIJKLMNOPQRSTUVWXYZ", True, (255,255,255))
    japn = font.render("あいうえおアイウエオ山田太郎鈴木花子", True, (255,255,255))

    ### 画面表示位置
    surface.blit(name, [20,20])
    surface.blit(numb, [20,70])
    surface.blit(asci, [20,120])
    surface.blit(japn, [20,170])

    ### 画面更新
    pygame.display.update()

    ### イベント取得
    for event in pygame.event.get():

        ### 終了処理
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            ### フォント変更
            if event.key == K_UP   and i > 0:
                i -= 1
            if event.key == K_DOWN and i < len(list)-1:
                i += 1
"""
running = True
screen = pygame.display.set_mode((360,640)) #画面サイズの設定
pygame.mixer.music.load("./mypj3/sound/normal_BGM.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1)
time.sleep(5)
pygame.mixer.Channel(0).play(pygame.mixer.Sound("./mypj3/sound/attacked.mp3"))

while running == True:
    screen.fill((0, 0, 0)) 
    for event in pygame.event.get():
            if event.type == pygame.QUIT: #上の×ボタンで閉じる
                running = False
"""
# algerian ローマ字と数字
# bizudminchomediumbizudpminchomediumtruetype 日本語
