# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 20:25:05 2019

@author: u235
"""

from PIL import Image, ImageOps,ImageChops, ImageDraw, ImageFilter, TiffImagePlugin
def create_png_from_tiff():
    names=[]
    Piece_colors=('b','w')
    Piece_type=('K','Q','R','N','B','p')
    for p_t in Piece_type:
        for c_t in Piece_colors:
            names.append(p_t+c_t)
    
    for name in names:        
    
        try:
           im_bw = Image.open(name+'.tif')
        except:
            print('Error read file:'+name+'.tif')
            continue
        im_rgb = im_bw.convert('RGB')
        im_rgb=ImageOps.expand(im_rgb, border=6, fill=(255, 255, 255),)# add white 5px border
        #im_rgb = im_bw.convert('L')
        #im_rgb=ImageOps.expand(im_rgb, border=6, fill=(255),)
        im_mask=im_rgb.copy()
        im_mask=im_mask.filter(ImageFilter.MinFilter(5))# create errode image
        im_mask2=im_mask.copy()
        ImageDraw.floodfill(im_mask, (0,0), value=(0,0,0))# flood fill image
        #ImageDraw.floodfill(im_mask, (0,0), value=(0))
        im_mask = ImageChops.difference(im_mask, im_mask2) # difference between image
        im_mask=ImageOps.invert(im_mask)
        im_mask=im_mask.convert('L')
        im_rgb.putalpha(im_mask)
        left,upper,right,lower = im_mask.getbbox()
        im_rgb = im_rgb.crop((left,upper,right,lower))
        im_rgb.save(name+'.png')
        
create_png_from_tiff()

