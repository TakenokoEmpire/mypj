import pygame
from pygame import Surface, mixer
from pygame.locals import *

pygame.init()
lv = 1
num = [0,1,2,3,4]
guess_list = []
turn = 1
hp = 100
error = 0
history = 0

#windowの表示
screen = pygame.display.set_mode((360,640)) #画面サイズの設定
screen.fill((0, 0, 0)) #画面のカラーをRGBで指定
pygame.display.set_caption("Hit, Blow and Dragons") #タイトルの変更

# キャラ立ち絵の設定
img = pygame.image.load("./mypj3/img/player.png")
X = 118
Y = 50


#マークの設定
b_moon_img = pygame.image.load("./mypj3/img/b_moon.png")
b_snow_img = pygame.image.load("./mypj3/img/b_snow.png")
b_star_img = pygame.image.load("./mypj3/img/b_star.png")
b_sun_img = pygame.image.load("./mypj3/img/b_sun.png")
g_moon_img = pygame.image.load("./mypj3/img/g_moon.png")
g_snow_img = pygame.image.load("./mypj3/img/g_snow.png")
g_star_img = pygame.image.load("./mypj3/img/g_star.png")
g_sun_img = pygame.image.load("./mypj3/img/g_sun.png")
p_moon_img = pygame.image.load("./mypj3/img/p_moon.png")
p_snow_img = pygame.image.load("./mypj3/img/p_snow.png")
p_star_img = pygame.image.load("./mypj3/img/p_star.png")
p_sun_img = pygame.image.load("./mypj3/img/p_sun.png")
y_moon_img = pygame.image.load("./mypj3/img/y_moon.png")
y_snow_img = pygame.image.load("./mypj3/img/y_snow.png")
y_star_img = pygame.image.load("./mypj3/img/y_star.png")
y_sun_img = pygame.image.load("./mypj3/img/y_sun.png")
marks = {0:b_moon_img, 1:b_snow_img, 2:b_star_img, 3:b_sun_img,
4:g_moon_img, 5:g_snow_img, 6:g_star_img, 7:g_sun_img,
8:p_moon_img, 9:p_snow_img, 10:p_star_img, 11:p_sun_img,
12:y_moon_img, 13:y_snow_img, 14:y_star_img, 15:y_sun_img
}

# マークの位置
mark_buttonrect = []
for n in range(5):
    mark_buttonrect.append(Rect(10+n*70,425,60,25))

#敵
enemy1_img = pygame.image.load("./mypj3/img/enemy1.png")
enemyrect = Rect(93,60,187,250)

# ボタンの設定
normal_buttonrect = Rect(80, 300, 200, 50)
boss_buttonrect = Rect(80, 375, 200, 50)
return_buttonrect = Rect(80,550,200,50)
history_buttonrect = Rect(120,570,120,30)
normal_button_img = pygame.image.load("./mypj3/img/normal_button.png")
boss_button_img = pygame.image.load("./mypj3/img/boss_button.png")
return_button_img = pygame.image.load("./mypj3/img/return.png")
history_button_img = pygame.image.load("./mypj3/img/history_button.png")


# 入力の制御
up_button_img = pygame.image.load("./mypj3/img/up.png")
down_button_img = pygame.image.load("./mypj3/img/down.png")
up_buttonrect = []
for n in range(5):
    up_buttonrect.append(Rect(10+n*70,400,60,25))
down_buttonrect = []
for n in range(5):
    down_buttonrect.append(Rect(10+n*70,485,60,25))
enter_button_img = pygame.image.load("./mypj3/img/enter.png")
enter_buttonrect = Rect(120,520,120,32)


#mixer.Sound("--.mp3") #音の再生

#画面の種類の設定
gamescene = 0


def home_show(level, image, normal_button=normal_button_img, boss_button=boss_button_img):
    """ホーム画面の描画
    """
    screen.blit(image,(118,50)) #imgの描画・updateされてるから
    font = pygame.font.SysFont(None, 40) #フォントの指定
    lv_display = font.render("Lv {}".format(level), True, (255,255,255))  #文字・色の指定
    screen.blit(lv_display, (150,220)) #テキストの位置
    screen.blit(normal_button, normal_buttonrect)
    screen.blit(boss_button, boss_buttonrect)

def error_show():
    """エラー画面の描画
    """
    font4 = pygame.font.SysFont(None, 33)
    error_message = font4.render("! Cannot enter the same mark !", True, (255,0,0)) 
    screen.blit(error_message, (18,300))
    screen.blit(return_button_img, return_buttonrect)

def history_show():
    """履歴の描画
    """
    screen.blit(return_button_img, return_buttonrect)


def normal_stage(num,turn,hp):
    """通常ステージの描画
    """
    screen.blit(enemy1_img,enemyrect)
    font2 = pygame.font.SysFont(None, 30)
    stage = font2.render("turn:{}".format(turn), True, (255,255,255))
    pygame.draw.line(screen,(0,200,0),(30,40),(30+hp,40),10)
    font3 = pygame.font.SysFont(None, 20)
    hp_word = font3.render("HP", True, (255,255,255))
    hp_value = font3.render("{}".format(hp), True, (255,255,255))
    damage = (turn-1)*10
    if damage != 0:
        pygame.draw.line(screen,(200,0,0),(30+hp,40),(30+hp+damage,40),10)
    screen.blit(stage, (5,5))
    screen.blit(hp_word, (5,35))
    screen.blit(hp_value, (30+hp+damage+2,35))
    screen.blit(enter_button_img, enter_buttonrect)
    screen.blit(history_button_img, history_buttonrect)
    mark_show(num)




def mark_show(num):
    """入力画面の描画
    """
    for n in range(5):
        screen.blit(up_button_img,up_buttonrect[n])
        screen.blit(down_button_img,down_buttonrect[n])
        screen.blit(marks[num[n]],mark_buttonrect[n])


def convert(num):
    """入力された予測をhit&blowの判定用の文字列に変換
    """
    num_convert = []
    for n in range(5):
        num_convert.append(str(num[n]))
        if num_convert[n] == "10":
            num_convert[n] = "a"
        if num_convert[n] == "11":
            num_convert[n] = "b"
        if num_convert[n] == "12":
            num_convert[n] = "c"
        if num_convert[n] == "13":
            num_convert[n] = "d"
        if num_convert[n] == "14":
            num_convert[n] = "e"
        if num_convert[n] == "15":
            num_convert[n] = "f"
    return num_convert[0]+num_convert[1]+num_convert[2]+num_convert[3]+num_convert[4]


def boss_stage():
    """ボスステージの描画
    """
    font2 = pygame.font.SysFont(None, 80)
    stage = font2.render("Boss Stage", True, (255,255,255))
    screen.blit(stage, (25,30))
    screen.blit(return_button_img, return_buttonrect)

running = True
while running:
    screen.fill((0, 0, 0)) 
    if error == 1:
        error_show()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                    if return_buttonrect.collidepoint(event.pos):
                        error = 0
    elif history == 1:
        history_show()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                    if return_buttonrect.collidepoint(event.pos):
                        history = 0
    elif gamescene == 0: #ホーム画面
        home_show(level=lv, image=img)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #上の×ボタンで閉じる
                running = False
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                    if normal_buttonrect.collidepoint(event.pos):
                        gamescene = 1
                    if boss_buttonrect.collidepoint(event.pos):
                        gamescene = 2

    elif gamescene == 1: #Normal Stage
        normal_stage(num,turn,hp)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #上の×ボタンで閉じる
                running = False
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                if up_buttonrect[0].collidepoint(event.pos):
                    num[0] += 1
                    if num[0] == 16:
                        num[0] = 0
                if down_buttonrect[0].collidepoint(event.pos):
                    num[0] -= 1
                    if num[0] == -1:
                        num[0] = 15
                if up_buttonrect[1].collidepoint(event.pos):
                    num[1] += 1
                    if num[1] == 16:
                        num[1] = 0
                if down_buttonrect[1].collidepoint(event.pos):
                    num[1] -= 1
                    if num[1] == -1:
                        num[1] = 15
                if up_buttonrect[2].collidepoint(event.pos):
                    num[2] += 1
                    if num[2] == 16:
                        num[2] = 0
                if down_buttonrect[2].collidepoint(event.pos):
                    num[2] -= 1
                    if num[2] == -1:
                        num[2] = 15
                if up_buttonrect[3].collidepoint(event.pos):
                    num[3] += 1
                    if num[3] == 16:
                        num[3] = 0
                if down_buttonrect[3].collidepoint(event.pos):
                    num[3] -= 1
                    if num[3] == -1:
                        num[3] = 15
                if up_buttonrect[4].collidepoint(event.pos):
                    num[4] += 1
                    if num[4] == 16:
                        num[4] = 0
                if down_buttonrect[4].collidepoint(event.pos):
                    num[4] -= 1
                    if num[4] == -1:
                        num[4] = 15
                if enter_buttonrect.collidepoint(event.pos):
                    for i in num:
                        if num.count(i) > 1:
                            error = 1 # 同じ数字が１つ以上含まれるときにerror=1にする
                    if error == 1:
                        print("error")
                    else:
                        guess_mark = [marks[num[0]],marks[num[1]],marks[num[2]],marks[num[3]],marks[num[4]]]
                        guess_list.append(guess_mark) # マークの履歴
                        guess = convert(num) # マークから文字列へ変換
                        turn += 1
                        hp -= 10
                if history_buttonrect.collidepoint(event.pos):
                    history = 1

    elif gamescene == 2: #Boss Stage
        boss_stage()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                    if return_buttonrect.collidepoint(event.pos):
                        gamescene = 0
    
    pygame.display.update() #スクリーン上のものを書き換えた時にはupdateが必要