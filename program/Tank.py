import pygame,random
import Base

BaseItem = Base.BaseItem

class Tank(BaseItem):
    def __init__(self, left, top):
        super().__init__()
        self.images = {
            'U':pygame.image.load('img/p1tankU.gif'),
            'D':pygame.image.load('img/p1tankD.gif'),
            'L':pygame.image.load('img/p1tankL.gif'),
            'R':pygame.image.load('img/p1tankR.gif')
        }
        self.direction = 'U'
        self.image = self.images[self.direction]
        #坦克所在的区域  Rect->
        self.rect = self.image.get_rect()
        #指定坦克初始化位置 分别距x，y轴的位置
        self.rect.left = left
        self.rect.top = top
        #新增速度属性
        self.speed = 5
        #新增属性： 坦克的移动开关
        self.stop = True
        #新增属性  live 用来记录，坦克是否活着
        self.live = True
        #新增属性： 用来记录坦克移动之前的坐标(用于坐标还原时使用)
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top

    #坦克的移动方法
    def move(self):
        from MainGame import MainGame
        #先记录移动之前的坐标
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top
        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'R':
            if self.rect.left + self.rect.height < MainGame.SCREEN_WIDTH:
                self.rect.left += self.speed
        elif self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < MainGame.SCREEN_HEIGHT:
                self.rect.top += self.speed
    def stay(self):
        self.rect.left = self.oldLeft
        self.rect.top = self.oldTop
    #新增碰撞墙壁的方法
    def hitWalls(self):
        from MainGame import MainGame
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(wall,self):
                self.stay()
    #射击方法
    def shot(self):
        import Bullet
        return Bullet.Bullet(self)
    #展示坦克(将坦克这个surface绘制到窗口中  blit())
    def displayTank(self):
        from MainGame import MainGame
        #1.重新设置坦克的图片
        self.image = self.images[self.direction]
        #2.将坦克加入到窗口中
        MainGame.window.blit(self.image,self.rect)
class MyTank(Tank):
    def __init__(self,left,top):
        super(MyTank, self).__init__(left,top)
    #新增主动碰撞到敌方坦克的方法
    def hitEnemyTank(self):
        from MainGame import MainGame
        for eTank in MainGame.EnemyTank_list:
            if pygame.sprite.collide_rect(eTank,self):
                self.stay()

class EnemyTank(Tank):
    def __init__(self,left,top,speed):
        super(EnemyTank, self).__init__(left,top)
        # self.live = True
        self.images = {
            'U': pygame.image.load('img/enemy1U.gif'),
            'D': pygame.image.load('img/enemy1D.gif'),
            'L': pygame.image.load('img/enemy1L.gif'),
            'R': pygame.image.load('img/enemy1R.gif')
        }
        self.direction = self.randDirection()
        self.image = self.images[self.direction]
        # 坦克所在的区域  Rect->
        self.rect = self.image.get_rect()
        # 指定坦克初始化位置 分别距x，y轴的位置
        self.rect.left = left
        self.rect.top = top
        # 新增速度属性
        self.speed = speed
        self.stop = True
        #新增步数属性，用来控制敌方坦克随机移动
        self.step = 30

    def randDirection(self):
        num = random.randint(1,4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'L'
        elif num == 4:
            return 'R'
    #随机移动
    def randMove(self):
        if self.step <= 0:
            self.direction = self.randDirection()
            self.step = 50
        else:
            self.move()
            self.step -= 1
    def shot(self):
        import Bullet
        num = random.randint(1,1000)
        if num  <= 20:
            return Bullet.Bullet(self)
    def hitMyTank(self):
        from MainGame import MainGame
        if MainGame.TANK_P1 and MainGame.TANK_P1.live:
            if pygame.sprite.collide_rect(self, MainGame.TANK_P1):
                # 让敌方坦克停下来  stay()
                self.stay()