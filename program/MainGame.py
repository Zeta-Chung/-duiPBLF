import pygame,time,random
import Tank,Music,Wall,Bullet

MyTank = Tank.MyTank
EnemyTank = Tank.EnemyTank
Music = Music.Music
Wall = Wall.Wall
Bullet = Bullet.Bullet

_display = pygame.display
COLOR_BLACK = pygame.Color(0, 0, 0)
COLOR_RED = pygame.Color(255, 0, 0)
COLOR_GREEN = pygame.Color(0, 255, 0)
COLOR_WHITE = pygame.Color(255, 255, 255)


class MainGame():
    # 游戏主窗口
    window = None
    SCREEN_HEIGHT = 500
    SCREEN_WIDTH = 800
    # 创建我方坦克
    TANK_P1 = None
    # 存储所有敌方坦克
    EnemyTank_list = []
    # 要创建的敌方坦克的数量
    EnemTank_count = 5
    # 存储我方子弹的列表
    Bullet_list = []
    # 存储敌方子弹的列表
    Enemy_bullet_list = []
    # 爆炸效果列表
    Explode_list = []
    # 墙壁列表
    Wall_list = []

    # 开始游戏方法
    def startGame(self):
        _display.init()
        # 创建窗口加载窗口
        MainGame.window = _display.set_mode([MainGame.SCREEN_WIDTH, MainGame.SCREEN_HEIGHT])
        self.creatMyTank()
        self.creatEnemyTank()
        self.creatWalls()
        # 设置一下游戏标题
        _display.set_caption("坦克大战")
        # 让窗口持续刷新操作
        while True:
            # 在循环中持续完成事件的获取
            self.getEvent()
            
            # 检查是否所有敌方坦克都被消灭，如果是则显示成功界面
            if len(MainGame.EnemyTank_list) == 0:
                self.showSuccessScreen()
                time.sleep(0.02)
                # 窗口的刷新
                _display.update()
                continue
            # 检查MyTank是否被消灭，如果是则显示失败界面
            if not MainGame.TANK_P1.live:
                self.showFailureScreen()
                time.sleep(0.02)
                # 窗口的刷新
                _display.update()
                continue

            # 给窗口完成一个填充颜色
            MainGame.window.fill(COLOR_BLACK)
            # 将绘制文字得到的小画布，粘贴到窗口中
            MainGame.window.blit(self.getTextSurface("剩余敌方坦克%d辆" % len(MainGame.EnemyTank_list)), (5, 5))
            # 调用展示墙壁的方法
            self.blitWalls()
            if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                # 将我方坦克加入到窗口中
                MainGame.TANK_P1.displayTank()
            else:
                del MainGame.TANK_P1
                MainGame.TANK_P1 = None
            # 循环展示敌方坦克
            self.blitEnemyTank()
            # 根据坦克的开关状态调用坦克的移动方法
            if MainGame.TANK_P1 and not MainGame.TANK_P1.stop:
                MainGame.TANK_P1.move()
                # 调用碰撞墙壁的方法
                MainGame.TANK_P1.hitWalls()
                MainGame.TANK_P1.hitEnemyTank()
            # 调用渲染子弹列表的一个方法
            self.blitBullet()
            # 调用渲染敌方子弹列表的一个方法
            self.blitEnemyBullet()
            # 调用展示爆炸效果的方法
            self.displayExplodes()
            time.sleep(0.02)
            # 窗口的刷新
            _display.update()

    # 创建我方坦克的方法
    def creatMyTank(self):
        # 创建我方坦克
        MainGame.TANK_P1 = MyTank(400, 300)
        # 创建音乐对象
        music = Music('img/start.wav')
        # 调用播放音乐方法
        music.play()

    # 创建敌方坦克
    def creatEnemyTank(self):
        top = 100
        for i in range(MainGame.EnemTank_count):
            speed = random.randint(3, 6)
            # 每次都随机生成一个left值
            left = random.randint(1, 7)
            eTank = EnemyTank(left * 100, top, speed)
            MainGame.EnemyTank_list.append(eTank)

    # 创建墙壁的方法
    def creatWalls(self):
        for i in range(6):
            wall = Wall(130 * i, 240)
            MainGame.Wall_list.append(wall)

    def blitWalls(self):
        for wall in MainGame.Wall_list:
            if wall.live:
                wall.displayWall()
            else:
                MainGame.Wall_list.remove(wall)

    # 将敌方坦克加入到窗口中
    def blitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if eTank.live:
                eTank.displayTank()
                # 坦克移动的方法
                eTank.randMove()
                # 调用敌方坦克与墙壁的碰撞方法
                eTank.hitWalls()
                # 敌方坦克是否撞到我方坦克
                eTank.hitMyTank()
                # 调用敌方坦克的射击
                eBullet = eTank.shot()
                # 如果子弹为None。不加入到列表
                if eBullet:
                    # 将子弹存储敌方子弹列表
                    MainGame.Enemy_bullet_list.append(eBullet)
            else:
                MainGame.EnemyTank_list.remove(eTank)

    # 将我方子弹加入到窗口中
    def blitBullet(self):
        for bullet in MainGame.Bullet_list:
            # 如果子弹还活着，绘制出来，否则，直接从列表中移除该子弹
            if bullet.live:
                bullet.displayBullet()
                # 让子弹移动
                bullet.bulletMove()
                # 调用我方子弹与敌方坦克的碰撞方法
                bullet.hitEnemyTank()
                # 调用判断我方子弹是否碰撞到墙壁的方法
                bullet.hitWalls()
            else:
                MainGame.Bullet_list.remove(bullet)

    # 将敌方子弹加入到窗口中
    def blitEnemyBullet(self):
        for eBullet in MainGame.Enemy_bullet_list:
            # 如果子弹还活着，绘制出来，否则，直接从列表中移除该子弹
            if eBullet.live:
                eBullet.displayBullet()
                # 让子弹移动
                eBullet.bulletMove()
                # 调用是否碰撞到墙壁的一个方法
                eBullet.hitWalls()
                if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                    eBullet.hitMyTank()
            else:
                MainGame.Enemy_bullet_list.remove(eBullet)

    # 新增方法： 展示爆炸效果列表
    def displayExplodes(self):
        for explode in MainGame.Explode_list:
            if explode.live:
                explode.displayExplode()
            else:
                MainGame.Explode_list.remove(explode)

    # 获取程序期间所有事件(鼠标事件，键盘事件)
    def getEvent(self):
        # 1.获取所有事件
        eventList = pygame.event.get()
        # 2.对事件进行判断处理(1、点击关闭按钮  2、按下键盘上的某个按键)
        for event in eventList:
            # 判断event.type 是否QUIT，如果是退出的话，直接调用程序结束方法
            if event.type == pygame.QUIT:
                self.endGame()
            # 判断事件类型是否为按键按下，如果是，继续判断按键是哪一个按键，来进行对应的处理
            if event.type == pygame.KEYDOWN:
                # 如果所有坦克都已被消灭，按ESC键重新开始游戏
                if len(MainGame.EnemyTank_list) == 0 and event.key == pygame.K_ESCAPE:
                    # 重置游戏
                    self.resetGame()
                    return
                    
                # 如果我方坦克被消灭，按ESC键重新开始游戏
                if (not MainGame.TANK_P1 or not MainGame.TANK_P1.live) and event.key == pygame.K_ESCAPE:
                    # 重置游戏
                    self.resetGame()
                    return

                if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                    # 具体是哪一个按键的处理
                    if event.key == pygame.K_LEFT:
                        print("坦克向左调头，移动")
                        # 修改坦克方向
                        MainGame.TANK_P1.direction = 'L'
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_RIGHT:
                        print("坦克向右调头，移动")
                        # 修改坦克方向
                        MainGame.TANK_P1.direction = 'R'
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_UP:
                        print("坦克向上调头，移动")
                        # 修改坦克方向
                        MainGame.TANK_P1.direction = 'U'
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_DOWN:
                        print("坦克向下掉头，移动")
                        # 修改坦克方向
                        MainGame.TANK_P1.direction = 'D'
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_SPACE:
                        print("发射子弹")
                        if len(MainGame.Bullet_list) < 3:
                            # 产生一颗子弹
                            m = Bullet(MainGame.TANK_P1)
                            # 将子弹加入到子弹列表
                            MainGame.Bullet_list.append(m)
                            music = Music('img/fire.wav')
                            music.play()
                        else:
                            print("子弹数量不足")
                        print("当前屏幕中的子弹数量为:%d" % len(MainGame.Bullet_list))
            # 结束游戏方法
            if event.type == pygame.KEYUP:
                # 松开的如果是方向键，才更改移动开关状态
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                        # 修改坦克的移动状态
                        MainGame.TANK_P1.stop = True

    # 左上角文字绘制的功能
    def getTextSurface(self, text):
        # 初始化字体模块
        pygame.font.init()
        # 创建字体对象
        font = pygame.font.SysFont('kaiti', 18)
        # 使用对应的字符完成相关内容的绘制
        textSurface = font.render(text, True, COLOR_RED)
        return textSurface

    # 文字绘制的功能（可自定义颜色和大小）
    def getCustomTextSurface(self, text, size=18, color=COLOR_RED):
        # 初始化字体模块
        pygame.font.init()
        # 创建字体对象
        font = pygame.font.SysFont('kaiti', size)
        # 使用对应的字符完成相关内容的绘制
        textSurface = font.render(text, True, color)
        return textSurface
        
    # 显示成功界面的方法
    def showSuccessScreen(self):
        # 只在第一次显示时播放音效
        if not hasattr(self, '_success_sound_played'):
            # 播放成功音效
            try:
                success_music = Music('img/success.mp3')  # 使用更通用的文件名
                success_music.play()
            except:
                # 如果音效文件不存在，则不播放
                pass
            self._success_sound_played = True
            
        # 填充绿色背景
        MainGame.window.fill(COLOR_GREEN)
        
        # 显示成功文字
        success_text = self.getCustomTextSurface("恭喜你，过关了！", 50, COLOR_WHITE)
        text_rect = success_text.get_rect()
        text_rect.center = (MainGame.SCREEN_WIDTH // 2, MainGame.SCREEN_HEIGHT // 2 - 50)
        MainGame.window.blit(success_text, text_rect)
        
        # 显示提示文字
        prompt_text = self.getCustomTextSurface("按ESC键重新开始游戏", 36, COLOR_WHITE)
        prompt_rect = prompt_text.get_rect()
        prompt_rect.center = (MainGame.SCREEN_WIDTH // 2, MainGame.SCREEN_HEIGHT // 2 + 50)
        MainGame.window.blit(prompt_text, prompt_rect)
        
        # 更新显示
        _display.update()

    # 显示失败界面的方法
    def showFailureScreen(self):
        # 只在第一次显示时播放音效
        if not hasattr(self, '_failure_sound_played'):
            # 播放失败音效
            try:
                failure_music = Music('img/fail.wav')  # 使用更通用的文件名
                failure_music.play()
            except:
                # 如果音效文件不存在，则不播放
                pass
            self._failure_sound_played = True

        # 填充红色背景
        MainGame.window.fill(COLOR_RED)

        # 显示失败文字
        failure_text = self.getCustomTextSurface("游戏失败，请重新开始！", 50, COLOR_WHITE)
        text_rect = failure_text.get_rect()
        text_rect.center = (MainGame.SCREEN_WIDTH // 2, MainGame.SCREEN_HEIGHT // 2 - 50)
        MainGame.window.blit(failure_text, text_rect)

        # 显示提示文字
        prompt_text = self.getCustomTextSurface("按ESC键重新开始游戏", 36, COLOR_WHITE)
        prompt_rect = prompt_text.get_rect()
        prompt_rect.center = (MainGame.SCREEN_WIDTH // 2, MainGame.SCREEN_HEIGHT // 2 + 50)
        MainGame.window.blit(prompt_text, prompt_rect)

        _display.update()

    # 重置游戏的方法
    def resetGame(self):
        # 清空所有列表
        MainGame.EnemyTank_list.clear()
        MainGame.Bullet_list.clear()
        MainGame.Enemy_bullet_list.clear()
        MainGame.Explode_list.clear()
        MainGame.Wall_list.clear()
        
        # 重置音效标记
        if hasattr(self, '_success_sound_played'):
            delattr(self, '_success_sound_played')
        if hasattr(self, '_failure_sound_played'):
            delattr(self, '_failure_sound_played')
        
        # 重新创建我方坦克
        self.creatMyTank()
        
        # 重新创建敌方坦克
        self.creatEnemyTank()
        
        # 重新创建墙壁
        self.creatWalls()
        
    def endGame(self):
        exit()