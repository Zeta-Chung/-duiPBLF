import pygame
import Base

BaseItem = Base.BaseItem

class Bullet(BaseItem):
    def __init__(self, tank):
        #图片
        super().__init__()
        self.image = pygame.image.load('img/enemymissile.gif')
        #方向（坦克方向）
        self.direction = tank.direction
        #位置
        self.rect = self.image.get_rect()
        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width/2 - self.rect.width/2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        #速度
        self.speed = 7
        #用来记录子弹是否活着
        self.live = True
    #子弹的移动方法
    def bulletMove(self):
        from MainGame import MainGame
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                #修改状态值
                self.live = False
        elif self.direction == 'D':
            if self.rect.top < MainGame.SCREEN_HEIGHT - self.rect.height:
                self.rect.top += self.speed
            else:
                # 修改状态值
                self.live = False
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                # 修改状态值
                self.live = False
        elif self.direction == 'R':
            if self.rect.left < MainGame.SCREEN_WIDTH - self.rect.width:
                self.rect.left += self.speed
            else:
                # 修改状态值
                self.live = False
    #展示子弹的方法
    def displayBullet(self):
        from MainGame import MainGame
        MainGame.window.blit(self.image,self.rect)
    #我方子弹碰撞敌方坦克的方法
    def hitEnemyTank(self):
        from MainGame import MainGame
        import Explode
        for eTank in MainGame.EnemyTank_list:
            if pygame.sprite.collide_rect(eTank,self):
                #产生一个爆炸效果
                explode = Explode.Explode(eTank)
                #将爆炸效果加入到爆炸效果列表
                MainGame.Explode_list.append(explode)
                self.live = False
                eTank.live = False
                
    #敌方子弹与我方坦克的碰撞方法
    def hitMyTank(self):
        from MainGame import MainGame
        import Explode
        if pygame.sprite.collide_rect(self,MainGame.TANK_P1):
            # 产生爆炸效果，并加入到爆炸效果列表中
            explode = Explode.Explode(MainGame.TANK_P1)
            MainGame.Explode_list.append(explode)
            #修改子弹状态
            self.live = False
            #修改我方坦克状态
            MainGame.TANK_P1.live = False
            
    #新增子弹与墙壁的碰撞
    def hitWalls(self):
        from MainGame import MainGame
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(wall,self):
                #修改子弹的live属性
                self.live = False
                wall.hp -= 1
                if wall.hp <= 0:
                    wall.live = False