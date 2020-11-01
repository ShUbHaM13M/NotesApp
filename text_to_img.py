from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os

os.chdir('./QuoteItRes')


class QuoteImage:
    def __init__(self, font, background, text, text_color, by_text, author_font):
        font_path = os.path.join('./fonts', f'{font}.ttf')

        self.font = ImageFont.truetype(
            font_path, size=26)
        self.text = text
        self.text_color = text_color

        self.author = by_text
        self.author_text = ImageFont.truetype(
            os.path.join('./fonts', f'{author_font}.ttf'), size=20)

        self.img = Image.open(f'./backgrounds/{background}.png')
        self.draw = ImageDraw.Draw(self.img)

    def saveImage(self):
        x, y = self.img.size
        text_width, text_height = self.draw.textsize(self.text)

        self.draw.text((x * 0.4 - text_width, y * 0.4 - text_height), self.text,
                       fill=self.text_color, font=self.font)

        text_width, text_height = self.draw.textsize(f'-{self.author}')
        self.draw.text((x * 0.8 - text_width, y * 0.8 - text_height), f'-{self.author}',
                       fill=self.text_color, font=self.author_text)
        self.img.save(f'{self.author}.png')


if __name__ == '__main__':
    quoteImage = QuoteImage('poppins_regular',
                            '102',
                            "i am a fucking GOD",
                            "rgb(0, 0, 255)",
                            "SeyTonic",
                            'poppins_regular')

    quoteImage.saveImage()
