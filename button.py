import pygame.font  #让 Pygame 能够将文本渲染到屏幕上

class Button:
    """为游戏创建按钮的类"""
    def __init__(self,ai_game,msg,button_color):
        """初始化按钮的属性"""  #将按钮通用的属性抽象成类
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # 设置按钮的尺寸和其他属性  由于只有一个按钮，且属性是固定的，所以可以直接填入实际的数值
        self.width, self.height = 200,50  # 按钮的宽高
        self.button_color = button_color    #(0,135,0) 按钮颜色
        self.text_color = (255,255,255) #文字颜色，白色
        self.font=pygame.font.SysFont(None,48) #调用pygame的方法，生成按钮中文字的样式属性

        # 创建按钮的 rect 对象，并使其居中
        self.rect = pygame.Rect(0,0,self.width,self.height) #设置按钮的矩形
        self.rect.center = self.screen_rect.center #让按钮的位置在屏幕位置的中间

        # 按钮的标签只需创建一次，调用方法创建标签
        self._prep_msg(msg)

    def _prep_msg(self,msg):
        """将 msg 渲染为图像，并使其在按钮上居中""" # Pygame 处理文本的方式font.render，将要显示的字符串渲染为图像。
        self.msg_image = self.font.render(msg,True,self.text_color,self.button_color) # 用font方法将文本转为图像msg_image
        self.msg_image_rect = self.msg_image.get_rect() #获取图像的矩形
        self.msg_image_rect.center = self.rect.center #让文本图片位置设置在按钮中间

    def draw_button(self):
        """绘制一个用颜色填充的按钮，再绘制文本"""
        self.screen.fill(self.button_color,self.rect) #根据矩形大小绘制按钮，并填充颜色
        self.screen.blit(self.msg_image,self.msg_image_rect) #在游戏屏幕screen上，调用blit方法，将文本图像绘制在按钮图像上

