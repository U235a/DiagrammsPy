# -*- coding: utf-8 -*-
"""
14.05 2019

@author: u235
"""

from PIL import Image, ImageOps,ImageChops, ImageDraw, ImageFilter, TiffImagePlugin
name='Board.tif'
def cell(im, types):
    [w,h]=im.size
    
    if types=='3w2b_w':
        p_x, p_y, p_w, p_h = w//16, 3*h//16, w*3//4, h//16
        cr_sz=(p_w, 2)
    elif types=='3b2w_w':
        p_x, p_y, p_w, p_h = w//16, 5*h//16, w*3//4, h//16
        cr_sz=(p_w, 2)
    elif types=='3w2b_h':
        p_x, p_y, p_w, p_h = 3*w//16, h//16, w//16, h*3//4
        cr_sz=(2, p_h)
    elif types=='3b2w_h':
        p_x, p_y, p_w, p_h = 5*w//16, h//16, w//16, h*3//4
        cr_sz=(2, p_h)
    part1=im.crop((p_x, p_y, p_x+p_w, p_y+p_h))
    part1=part1.resize(cr_sz, resample=Image.LANCZOS)
    part1=ImageOps.autocontrast(part1)
       
    if types[1]=='w':
        part1=ImageOps.invert(part1)
    part1=part1.point(lambda p: p<125 and 255) #<125
 
    left,upper,right,lower = part1.getbbox()
    
  
    if types[-1]=='w':
       return [right-left, p_x+left]
    else:
        return [lower-upper, p_y+upper]
    
def Board2coord(name):
    try:
           im_board = Image.open(name)
    except:
            print('Error read file')
    im_board=im_board.convert('L')
    [w,h]=im_board.size
    
    draw_rect=im_board.copy()
    draw_rect = draw_rect.filter(ImageFilter.MinFilter(15)) # morphology closing
    draw_rect = draw_rect.filter(ImageFilter.MaxFilter(15))
    #draw_rect.save('test.png')
    w_w=(3*cell(draw_rect,'3w2b_w')[0]-2*cell(draw_rect,'3b2w_w')[0])//5 
    b_w=(3*cell(draw_rect,'3b2w_w')[0]-2*cell(draw_rect,'3w2b_w')[0])//5
    w_board=cell(draw_rect,'3w2b_w')[0]+cell(draw_rect,'3b2w_w')[0]-w_w-b_w
    x0=cell(draw_rect,'3b2w_w')[1]-w_w 
  
    w_h=(3*cell(draw_rect,'3w2b_h')[0]-2*cell(draw_rect,'3b2w_h')[0])//5 
    b_h=(3*cell(draw_rect, '3b2w_h')[0]-2*cell(draw_rect, '3w2b_h')[0])//5
    h_board=(cell(draw_rect,'3w2b_h')[0]+cell(draw_rect,'3b2w_h')[0])*8//10
    y0=cell(draw_rect,'3b2w_h')[1]-w_h  
    return(x0, y0, w_board, h_board)



    