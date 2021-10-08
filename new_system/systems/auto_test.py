
from. import show_game4


class Automation(show_game4.ShowGame):

    def __init__(self):
        super().__init__()

    def stage_select(self):
        """ステージセレクト画面
        """
        font = pygame.font.SysFont(
            "bizudminchomediumbizudpminchomediumtruetype", 30)
        level = font.render("ステージを選んで下さい", True, "WHITE")
        self.screen.blit(level, (11, 10))
        font2 = pygame.font.SysFont("algerian", 40)
        for i in range(self.max_dungeon_num):  # ステージの数だけ描画
            level = font2.render("LEVEL:{}".format(i+1), True, "WHITE")
            self.screen.blit(level, (100, 100+100*i))
        self.screen.blit(self.return_button_img, self.return_buttonrect)

    def judge_stage_select(self):
        """ステージセレクト画面のボタンの判定
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                for i in range(self.max_dungeon_num):
                    if self.stage_select_buttonrect[i].collidepoint(event.pos):
                        self.dungeon_num = i+1
                        pygame.mixer.Channel(0).play(
                            pygame.mixer.Sound(self.se_dict["start"]))
                        time.sleep(2)
                        if self.gamescene == 1:
                            pygame.mixer.music.load(self.bgm_dict["normal"])
                            pygame.mixer.music.set_volume(0.3)
                            pygame.mixer.music.play(loops=-1)
                        elif self.gamescene == 2:
                            pygame.mixer.music.load(self.bgm_dict["boss"])
                            pygame.mixer.music.set_volume(0.3)
                            pygame.mixer.music.play(loops=-1)
                if self.return_buttonrect.collidepoint(event.pos):
                    self.gamescene = 0
