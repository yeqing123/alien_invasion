from PIL import Image

class DelImageBG:
    """用于删除图像的背景颜色的类"""

    def __init__(self, image_name):
        """完成一些必要的初始化"""
        self.image_name = image_name

        # 首先打开需要处理的图像
        self.image = Image.open(image_name)
        # 将图像转换为RGBA模式
        self.image_rgba = self.image.convert('RGBA')
        # 创建一个新的空白图像
        self.new_image = Image.new('RGBA', self.image_rgba.size, (0, 0, 0, 0))

    def delete_background(self):
        """遍历原始图像的每个像素，如果发现是非白色，就复制到新的空白图像中"""
        # 获取原始图像的宽度和高度
        width, heigh = self.image_rgba.size

        # 遍历原始图像的每个像素
        for x in range(width):
            for y in range(heigh):
                # 获取当前像素的颜色(r,g,b为颜色，a为透明度)
                r, g, b, a = self.image_rgba.getpixel((x, y))
                # 判断当前像素是否为白色，
                # 如果像素为白色，则将其透明度设置为0，并放入新图像中
                # 否则，直接将该像素复制的新图像中
                if r == 230 and g == 230 and b == 230:
                    self.new_image.putpixel((x, y), (r, g, b, 0))
                else:
                    self.new_image.putpixel((x, y), (r, g, b, a))

        # 最后保存新的图像
        new_name = 'processed_' + self.image_name
        self.new_image.save(new_name)
