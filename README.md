# 第三组-程序设计实践项目

##  项目简介：基于python的本地运行坦克大战

##  分工：
* 王渊辰:  代码
* 钟浩轩:  代码
* 陈婉秋: 代码
* 肖宏博:  做报告
* 王诗琦:  PPT，项目整体统筹

## 代码具体描述

need :  需求

prototype : 原型









## zhx：游戏核心控制与主循环

我的加强建议是，改动创建墙壁逻辑，改为随机创建

**负责模块：**
- [MainGame](file:\-duiPBLF\Game\tank04.py#L11-L55) 类的核心逻辑
- 游戏主循环 [startGame](file:\-duiPBLF\Game\tank04.py#L16-L29)
- 事件处理 [getEvent](file:\-duiPBLF\Game\tank04.py#L36-L55)
- 游戏对象的创建和协调：
  - [creatMyTank](file:\-duiPBLF\Game\tankall.py#L68-L74)
  - [creatEnemyTank](file:\-duiPBLF\Game\tankall.py#L76-L83)
  - [creatWalls](file:\-duiPBLF\Game\tankall.py#L85-L88)
- 文本渲染 [getTextSurface](file:\-duiPBLF\Game\tankall.py#L206-L216)
- 游戏结束处理 [endGame](file:\-duiPBLF\Game\tank04.py#L32-L34)

**主要职责：**

- 控制整个游戏流程
- 处理用户输入事件
- 协调各游戏组件之间的交互
- 管理游戏状态更新

## wyc：游戏实体与物理系统

加强需求：优化实体逻辑，优化AI

**负责模块：**

- [Tank](file:\-duiPBLF\Game\tank04.py#L58-L70) 基类及所有相关方法：
  - 移动逻辑 [move](file:\-duiPBLF\Game\tank04.py#L62-L63)
  - 碰撞检测 [hitWalls](file:\-duiPBLF\Game\tankall.py#L270-L273)
  - 位置保持 [stay](file:\-duiPBLF\Game\tank24.py#L314-L316)
  - 射击 [shot](file:\-duiPBLF\Game\tank04.py#L66-L67)
  - 显示 [displayTank](file:\-duiPBLF\Game\tank04.py#L69-L70)
- [MyTank](file:\-duiPBLF\Game\tank04.py#L72-L74) 类：
  - 玩家坦克特有逻辑 [hitEnemyTank](file:\-duiPBLF\Game\tankall.py#L398-L406)
- [EnemyTank](file:\-duiPBLF\Game\tank04.py#L77-L79) 类：
  - 敌方AI行为 [randMove](file:\-duiPBLF\Game\tank11.py#L232-L241)
  - 随机方向 [randDirection](file:\-duiPBLF\Game\tank11.py#L220-L229)
  - 射击逻辑 [shot](file:\-duiPBLF\Game\tank04.py#L66-L67)
  - 碰撞处理 [hitMyTank](file:\-duiPBLF\Game\tankall.py#L408-L416)
- [Bullet](file:\-duiPBLF\Game\tank04.py#L82-L90) 类：
  - 子弹移动 [bulletMove](file:\-duiPBLF\Game\tankall.py#L369-L393)
  - 所有碰撞检测：
    - [hitEnemyTank](file:\-duiPBLF\Game\tankall.py#L398-L406)
    - [hitMyTank](file:\-duiPBLF\Game\tankall.py#L408-L416)
    - [hitWalls](file:\-duiPBLF\Game\tankall.py#L270-L273)
  - 显示 [displayBullet](file:\-duiPBLF\Game\tank04.py#L89-L90)
- [Wall](file:\-duiPBLF\Game\tank04.py#L91-L96) 类：
  - 墙壁显示 [displayWall](file:\-duiPBLF\Game\tank04.py#L95-L96)
  - 生命值管理

**主要职责：**

- 实现游戏中所有可交互对象的行为
- 处理物理碰撞和游戏规则逻辑
- 维护各实体的状态

## cwq：视觉效果与音频系统

没啥加强建议，看懂代码先

**负责模块：**

- [Explode](file:\-duiPBLF\Game\tank04.py#L97-L102) 类：
  - 爆炸效果渲染 [displayExplode](file:\-duiPBLF\Game\tank04.py#L101-L102)
- [Music](file:\-duiPBLF\Game\tank04.py#L103-L108) 类：
  - 音频加载和播放 [play](file:\-duiPBLF\Game\tank04.py#L107-L108)
- UI渲染相关：
  - 所有的 `blit*` 方法（[blitWalls](file:\-duiPBLF\Game\tankall.py#L89-L94), [blitEnemyTank](file:\-duiPBLF\Game\tank11.py#L65-L68), [blitBullet](file:\-duiPBLF\Game\tankall.py#L115-L127), [blitEnemyBullet](file:\-duiPBLF\Game\tank16.py#L95-L101), [displayExplodes](file:\-duiPBLF\Game\tankall.py#L143-L148)）
- 屏幕刷新和帧率控制

**主要职责：**
- 处理游戏的视觉表现
- 管理音效系统
- 负责用户界面的渲染
- 确保流畅的游戏体验

这种分工方式遵循了关注点分离原则，每个人负责游戏开发的不同层面，既保证了代码的模块化，又便于团队协作开发。
