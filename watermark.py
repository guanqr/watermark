# coding:utf-8
# 给图片添加防盗水印
# https://guanqr.com/*

from PIL import Image, ImageDraw, ImageFont
import os


# 读取指定文件夹图片列表，记录文件名
imgOpen = 'now/baishezhuan'
imgSave = 'print/baishezhuan'
publisher = 'liaoyuan'

imgList = os.listdir(imgOpen)

for index in range(len(imgList)):
    imgList[index] = imgList[index][:-4] 
#print(imgList)


# 添加水印
def add_text_to_image(image, text):
    font = ImageFont.truetype('BerkshireSwash-Regular.ttf', 54)
   
    # 添加背景
    new_img = Image.new('RGBA', (image.size[0] * 3, image.size[1] * 3), (0, 0, 0, 0))
    new_img.paste(image, image.size)
   
    # 添加水印
    font_len = len(text)
    rgba_image = new_img.convert('RGBA')
    text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)
   
    for i in range(0, rgba_image.size[0], font_len*30+100):
        for j in range(0, rgba_image.size[1], 200):
            image_draw.text((i, j), text, font=font, fill=(255, 255, 255, 50))
    text_overlay = text_overlay.rotate(45)
    image_with_text = Image.alpha_composite(rgba_image, text_overlay)
   
    # 裁切图片
    image_with_text = image_with_text.crop((image.size[0], image.size[1], image.size[0] * 2, image.size[1] * 2))
    return image_with_text


# PNG 转 JPG
def png2jpg(pngPath):
    img = Image.open(pngPath) 
    (w, h) = img.size
    infile = pngPath
    outfile = os.path.splitext(infile)[0] + ".jpg"
    img = Image.open(infile)
    img = img.resize((int(w), int(h)), Image.ANTIALIAS)
    try:
        if len(img.split()) == 4:
            # prevent IOError: cannot write mode RGBA as BMP
            r, g, b, a = img.split()
            img = Image.merge("RGB", (r, g, b))
            img.convert('RGB').save(outfile, quality=70)
            os.remove(pngPath)
        else:
            img.convert('RGB').save(outfile, quality=70)
            os.remove(pngPath)
        return outfile
    except Exception as e:
        print("PNG 转换 JPG 错误", e)


# 缩放图片到指定尺寸
def resizeByHeight(jpgPath, newHeight): 
    img = Image.open(jpgPath) 
    (x, y) = img.size
    ratio = y / newHeight
    x_s = int(x / ratio)
    y_s = newHeight
    out = img.resize((x_s, y_s), Image.ANTIALIAS) 
    out.save(jpgPath) 


if __name__ == '__main__':
    for index in range(len(imgList)):
        fileName = imgList[index]
        openAddress = imgOpen + '/' + fileName + '.jpg'
        saveAddress = imgSave + '/' + publisher + '-' + fileName + '.png'
        resizeByHeight(openAddress, 1600)
        img = Image.open(openAddress)
        im_after = add_text_to_image(img, u'Guan Qirui Collection')
        im_after.save(saveAddress)
        png2jpg(saveAddress)
        print(fileName)