# coding=utf-8
# uliontse

import os
import string
import numpy as np
from random import randint,sample

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
except ImportError:
    import Image, ImageDraw, ImageFilter, ImageFont


def generate(number=4,bgSize=None,font=None,colorAll=None,pool=None,drawLine=True,foggy=True,
             saveDirPath=None,showImg=True,returnText=True):
    '''
    :param number: int,
    :param bgSize: tuple,backgroundSize(width,height). The `height` affects `fontSize` & `lineWidth`.
    :param font: str,Default font 'arial'. Windows :file:`C:\fontPath\arial.ttf` directory.
    :param colorAll: tuple,(bgColor,fontColor,lineColor). Default colorAll=('white','blue','red').
    :param pool: set, Default {[A-Za-z0-9]}
    :param drawLine: boolean,
    :param foggy: boolean,
    :param saveDirPath: str, Default `os.getcwd()`
    :param showImg: boolean,
    :param returnText: boolean,
    :return: None or str
    '''

    bgSize = bgSize or (200,80)
    font = font or r'arial.ttf'
    colorAll = colorAll or ('white','blue','red')
    pool = pool or list(string.ascii_letters) + [str(x) for x in range(10)]
    text = ''.join(sample(set(pool), number))
    font = ImageFont.truetype(font,bgSize[1])

    if not foggy:
        image = Image.new(mode='RGBA', size=bgSize, color=colorAll[0])
    else:
        fogArray = np.random.randint(0,255,size=(bgSize[1],bgSize[0],3),dtype=np.uint8)
        image = Image.fromarray(fogArray)

    draw = ImageDraw.Draw(image)
    textInd = ((bgSize[0]-font.getsize(text)[0])/2,(bgSize[1]-font.getsize(text)[1])/2)
    draw.text(xy=textInd,text=text,font=font,fill=colorAll[1])

    if drawLine:
        lineInd = [(textInd[0],randint(int(textInd[1]+1),bgSize[1]-int(textInd[1]-1))),
                    (bgSize[0]-textInd[0],randint(int(textInd[1]+1),bgSize[1]-int(textInd[1]-1)))]
        draw.line(xy=lineInd,fill=colorAll[2],width=int(bgSize[1]//10))

    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    if showImg: image.show()
    if not saveDirPath:
        image.save('vcode.png')
        print('Save OK! \nsaveDirPath: {}'.format(os.getcwd()))
    else:
        try:
            image.save(saveDirPath + r'/vcode_{}.png'.format(text))
        except:
            image.save(saveDirPath + r'\\vcode_{}.png'.format(text))
        finally:
            print('Save OK! \nsaveDirPath: {}'.format(saveDirPath))

    return text if returnText else None

