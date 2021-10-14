import pygame
from pygame import mixer
import time
pygame.init()
mixer.init()
import sys
from pygame.locals import *
import random

### 画面初期化
surface = pygame.display.set_mode((360, 640))
clock = pygame.time.Clock()
FPS = 72
surface.fill((0,0,0))
color_list = [(175,238,238),(238,130,238),(212,175,55)]
color = color_list[random.randint(0, 2)]
ball_img = pygame.image.load("./mypj3/img/ball.png")
j=0
"""
### キーリピート設定
pygame.key.set_repeat(100,100)

### フォントリスト取得
list = []
for x in pygame.font.get_fonts():
    list.append(x)

### リスト位置初期化
i = 0
"""
### 無限ループ
while True:
    """
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



    for i in range(144):
        surface.fill((0,0,0))
        if i > 47 and i < 72:
            pygame.draw.circle(surface, (240,248,255) ,(180,320),i-47,0)
        if i >= 72:
            surface.blit(ball_img,Rect(155,295,50,50))
        pygame.draw.circle(surface, color,(180,320),5+i,3)
        if i > 10:
            pygame.draw.circle(surface, color,(50,240),i-10,3)
        if i > 15:
            pygame.draw.circle(surface, color,(300,400),i-15,3)
        if i > 20:
            pygame.draw.circle(surface, color,(240,300),i-20,3)
        if i > 23:
            pygame.draw.circle(surface,color,(120,350),i-23,3)
        if i > 25:
            pygame.draw.circle(surface, color,(220,150),i-25,3)
            pygame.draw.circle(surface,color,(130,450),i-25,3)
        if i >= 108:
            pygame.draw.circle(surface, (240,248,255) ,(180,320),25+(i-108)*15,0)
        pygame.display.update()
        clock.tick(FPS)
"""
    
    surface.fill((0,0,0))
    for i in range(108):
        font = pygame.font.SysFont("bizudminchomediumbizudpminchomediumtruetype",25)
        line_1 = font.render("この世界ではみんな",True, (255*i/108,255*i/108,255*i/108))
        line_2 = font.render("秘密のマークを持っています",True,  (255*i/108,255*i/108,255*i/108))
        surface.blit(line_1, (10,10))
        surface.blit(line_2, (10,40))
        pygame.display.update()
        clock.tick(FPS) 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                if Rect(0,0,360,640).collidepoint(event.pos):
                    j = 1 # 画面を押せば飛ばせるようにしたほうがいいかも
        if j == 1:
            line_1 = font.render("この世界ではみんな",True, (255,255,255))
            line_2 = font.render("秘密のマークを持っています",True,  (255,255,255))
            surface.blit(line_1, (10,10))
            surface.blit(line_2, (10,40))
            pygame.display.update()
            break
    if j == 0:
        time.sleep(1)

    for i in range(108):
        font = pygame.font.SysFont("bizudminchomediumbizudpminchomediumtruetype",25)
        line_1 = font.render("この秘密のマークは",True, (255*i/108,255*i/108,255*i/108))
        line_2 = font.render("持ち主を守る",True,  (255*i/108,255*i/108,255*i/108))
        line_3 = font.render("不思議な力の鍵です",True,  (255*i/108,255*i/108,255*i/108))
        surface.blit(line_1, (10,90))
        surface.blit(line_2, (10,120))
        surface.blit(line_3, (10,150))
        pygame.display.update()
        clock.tick(FPS) 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                if Rect(0,0,360,640).collidepoint(event.pos):
                    j = 1 # 画面を押せば飛ばせるようにしたほうがいいかも
        
        if j == 1:
            line_1 = font.render("この秘密のマークは",True, (255,255,255))
            line_2 = font.render("持ち主を守る",True,  (255,255,255))
            line_3 = font.render("不思議な力の鍵です",True,  (255,255,255))
            surface.blit(line_1, (10,90))
            surface.blit(line_2, (10,120))
            surface.blit(line_3, (10,150))
            pygame.display.update()
            break
    if j == 0:
        time.sleep(1)
    
    for i in range(108):
        font = pygame.font.SysFont("bizudminchomediumbizudpminchomediumtruetype",25)
        line_1 = font.render("冒険者はモンスターの",True, (255*i/108,255*i/108,255*i/108))
        line_2 = font.render("秘密のマークを解いて倒します",True,  (255*i/108,255*i/108,255*i/108))
        surface.blit(line_1, (10,200))
        surface.blit(line_2, (10,230))
        pygame.display.update()
        clock.tick(FPS) 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                if Rect(0,0,360,640).collidepoint(event.pos):
                    j = 1 # 画面を押せば飛ばせるようにしたほうがいいかも
        if j == 1:
            line_1 = font.render("冒険者はモンスターの",True, (255,255,255))
            line_2 = font.render("秘密のマークを解いて倒します",True,  (255,255,255))
            surface.blit(line_1, (10,200))
            surface.blit(line_2, (10,230))
            pygame.display.update()
            break
    if j == 0:
        time.sleep(1)

    for i in range(108):
        font = pygame.font.SysFont("bizudminchomediumbizudpminchomediumtruetype",25)
        line_1 = font.render("しかし知能の高いボスには",True, (255*i/108,255*i/108,255*i/108))
        line_2 = font.render("気を付けなくてはいけません",True,  (255*i/108,255*i/108,255*i/108))
        surface.blit(line_1, (10,280))
        surface.blit(line_2, (10,310))
        pygame.display.update()
        clock.tick(FPS) 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                if Rect(0,0,360,640).collidepoint(event.pos):
                    j = 1 # 画面を押せば飛ばせるようにしたほうがいいかも
        if j == 1:
            line_1 = font.render("しかし知能の高いボスには",True, (255,255,255))
            line_2 = font.render("気を付けなくてはいけません",True,  (255,255,255))
            surface.blit(line_1, (10,280))
            surface.blit(line_2, (10,310))
            pygame.display.update()
            break
    if j == 0:
        time.sleep(1)

    for i in range(108):
        font = pygame.font.SysFont("bizudminchomediumbizudpminchomediumtruetype",25)
        line_1 = font.render("ボスは冒険者の秘密のマークを",True, (255*i/108,255*i/108,255*i/108))
        line_2 = font.render("解いてしまうのです",True,  (255*i/108,255*i/108,255*i/108))
        surface.blit(line_1, (10,360))
        surface.blit(line_2, (10,390))
        pygame.display.update()
        clock.tick(FPS) 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                if Rect(0,0,360,640).collidepoint(event.pos):
                    j = 1 # 画面を押せば飛ばせるようにしたほうがいいかも
        if j == 1:
            line_1 = font.render("ボスは冒険者の秘密のマークを",True, (255,255,255))
            line_2 = font.render("解いてしまうのです",True,  (255,255,255))
            surface.blit(line_1, (10,360))
            surface.blit(line_2, (10,390))
            pygame.display.update()
            break
    if j == 0:
        time.sleep(1)

    for i in range(108):
        font = pygame.font.SysFont("bizudminchomediumbizudpminchomediumtruetype",25)
        line_1 = font.render("ボスよりも早く",True, (255*i/108,255*i/108,255*i/108))
        line_2 = font.render("秘密のマークを解きましょう",True,  (255*i/108,255*i/108,255*i/108))
        surface.blit(line_1, (10,440))
        surface.blit(line_2, (10,470))
        pygame.display.update()
        clock.tick(FPS) 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                if Rect(0,0,360,640).collidepoint(event.pos):
                    j = 1 # 画面を押せば飛ばせるようにしたほうがいいかも
        if j == 1:
            line_1 = font.render("ボスよりも早く",True, (255,255,255))
            line_2 = font.render("秘密のマークを解きましょう",True,  (255,255,255))
            surface.blit(line_1, (10,440))
            surface.blit(line_2, (10,470))
            pygame.display.update()
            break
    if j == 0:
        time.sleep(1)

    for i in range(108):
        font = pygame.font.SysFont("bizudminchomediumbizudpminchomediumtruetype",25)
        line_1 = font.render("あなたの冒険に祝福を",True, (255*i/108,255*i/108,255*i/108))
        surface.blit(line_1, (100,550))
        pygame.display.update()
        clock.tick(FPS) 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                if Rect(0,0,360,640).collidepoint(event.pos):
                    j = 1 # 画面を押せば飛ばせるようにしたほうがいいかも
        if j == 1:
            line_1 = font.render("あなたの冒険に祝福を",True, (255,255,255))
            surface.blit(line_1, (100,550))
            pygame.display.update()
            break

    time.sleep(2)

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

