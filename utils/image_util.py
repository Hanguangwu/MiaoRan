import cv2
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont
from blind_watermark import WaterMark


def ascii_art(image, width=100):
    """
    把图片转换成ASCII码字符画
    """
    # 转为灰度图
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    # 调整图像宽度，按比例缩放高度
    height = int(width * gray.shape[0] / gray.shape[1])
    resized_gray = cv2.resize(gray, (width, height))

    ascii_chars = "@%#*+=-:. "  # 字符表，明暗逐渐递减
    result = ""

    for row in resized_gray:
        for pixel in row:
            char_idx = pixel * (len(ascii_chars) - 1) // 255
            result += ascii_chars[char_idx]
        result += "\n"
    return result


def sketch_image(image):
    """
    转素描风格图片
    """
    img_gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    img_invert = cv2.bitwise_not(img_gray)
    img_blur = cv2.GaussianBlur(img_invert, (21, 21), sigmaX=0, sigmaY=0)
    sketch = cv2.divide(img_gray, 255 - img_blur, scale=256)
    return sketch  # 返回灰度np.array，可转PIL显示


# image = cv2.imread('dogs.webp')
#
# sketch = sketch_image(image)
#
# Image.fromarray(sketch).save('sketch.jpg')

def embed_visible_watermark(image_pil, watermark_text, pos=(10, 10), opacity=128):
    """
    给图片添加明水印（文本）
    """
    watermark_overlay = Image.new("RGBA", image_pil.size)
    draw = ImageDraw.Draw(watermark_overlay)
    font_size = max(20, image_pil.size[0] // 20)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    draw.text(pos, watermark_text, fill=(255, 255, 255, opacity), font=font)
    # 结合原图
    watermarked = Image.alpha_composite(image_pil.convert("RGBA"), watermark_overlay)
    return watermarked.convert("RGB")


def embed_blind_watermark(image_pil, wm_text, pw_img=1, pw_wm=1, out_path='output_embed.png'):
    """
    使用 blind_watermark 包给图片嵌入隐水印
    """
    bwm = WaterMark(password_img=pw_img, password_wm=pw_wm)

    # blind_watermark 接口需要路径，先保存临时图片
    tmp_input = 'tmp_input.png'
    image_pil.save(tmp_input)

    bwm.read_img(tmp_input)
    bwm.read_wm(wm_text, mode='str')
    bwm.embed(out_path)
    result_img = Image.open(out_path)
    return result_img


def extract_blind_watermark(image_path, wm_len=128, pw_img=1, pw_wm=1):
    bwm = WaterMark(password_img=pw_img, password_wm=pw_wm)
    wm_extract = bwm.extract(image_path, wm_shape=wm_len, mode='str')
    return wm_extract


