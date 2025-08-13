from PIL import Image, ImageFont, ImageDraw
import io


def add_watermark(photo_data, text: str) -> io.BytesIO:
    """
    bg: фоновое изображение размером (2width, 2height).
    На центр bg вставляется переданное фото размером (width, height).
    Создается изображение watermark_img размером (2width, 2height) с наклоном.
    Затем на фон накладывается водяной знак.
    Из итогового изображения вырезается область размером (width, height) — результат (result).
    """
    photo = Image.open(photo_data)
    width = photo.width
    height = photo.height
    text = f"{f"{text}    " * (width//20)}\n\n" * (height//20)
    font_size = width // 20
    font = ImageFont.truetype("arial.ttf", size=font_size)
    bg = Image.new("RGB", (width*2, height*2), (0, 0, 0))
    bg.paste(photo, (width//2, height//2))
    watermark_img = Image.new("RGB", (width*2, height*2), (0, 0, 0))
    watermark = ImageDraw.Draw(watermark_img)
    watermark.multiline_text((0, 0), text, font=font, fill=(255, 255, 255, 50))
    watermark_img = watermark_img.rotate(45)
    result = Image.blend(bg, watermark_img, 0.1).crop((width//2, height//2, width//2+width, height//2+height))
    result_byte_arr = io.BytesIO()
    result.save(result_byte_arr, format="JPEG")
    result_byte_arr.seek(0)
    return result_byte_arr


