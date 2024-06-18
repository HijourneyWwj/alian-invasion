import pygame
import numpy as np

"""通用羽化效果"""
"""
入参：
1. surface:这是一个 pygame.Surface 对象，用于绘制护盾的图像。它是一个带有 alpha 通道的表面，因此支持透明度。

2. radius:圆的半径。指定了护盾圆形的大小。

3. color:圆形边框的颜色，是一个包含 RGBA 值的四元组 (R, G, B, A)。前三个值是红、绿、蓝颜色值（0-255），最后一个值是 alpha 透明度（0-255）。

4. border_thickness:圆形边框的厚度。用于指定护盾边框的宽度。

5. feather_radius:羽化效果的半径。指定了从边框开始向外渐变模糊的距离。
"""

def feather(surface, radius, color, border_thickness, feather_radius):
    """应用羽化效果"""
    width, height = surface.get_size()
    center_x, center_y = width // 2, height // 2

    for y in range(height):
        for x in range(width):
            dist = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
            if radius - border_thickness <= dist <= radius:
                alpha = max(0, 255 - int((dist - (radius - border_thickness)) / feather_radius * 255))
                surface.set_at((x, y), (*color[:3], alpha))
            elif dist > radius:
                surface.set_at((x, y), (0, 0, 0, 0))
