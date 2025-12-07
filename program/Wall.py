import pygame

class Wall():
    def __init__(self,left,top):
        self.image = pygame.image.load('img/steels.gif')
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        #用来判断墙壁是否应该在窗口中展示
        self.live = True
        #用来记录墙壁的生命值
        self.hp = 3
    #展示墙壁的方法
    def displayWall(self):
        from MainGame import MainGame
        MainGame.window.blit(self.image,self.rect)