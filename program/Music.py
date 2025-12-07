import pygame

class Music():
    def __init__(self,fileName):
        self.fileName = fileName
        #先初始化混合器
        pygame.mixer.init()
        pygame.mixer.music.load(self.fileName)
    #开始播放音乐
    def play(self):
        pygame.mixer.music.play()
        pass