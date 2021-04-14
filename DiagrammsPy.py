# -*- coding: utf-8 -*-
"""
14.05.20 2019

@author: u235
"""

from PIL import Image, ImageOps,ImageChops, ImageDraw, ImageFilter, TiffImagePlugin
from pillow_test import create_png_from_tiff
from board2coord import Board2coord
create_png_from_tiff()
name='Board.tif'
x0, y0, w_board, h_board=Board2coord(name)
pos1=('abcdefgh')
i=0
              

def fen2chess(fen):
        d = {'r': 'Rb', 'R': 'Rw','n':'Nb','N':'Nw',\
         'q': 'Qb', 'Q': 'Qw','k': 'Kb', 'K': 'Kw',\
         'b': 'Bb', 'B': 'Bw','p': 'pb', 'P': 'pw',\
             'z': ''}
        pos1=('abcdefgh')
        pos2=('87654321')
        fen=fen.split(' ')[0]
        s=('')
        for i in fen:
            if i in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                s+=int(i)*'z'
            elif i=='/':
                s+=''
            else:
                s+=i
        chess=''
        for i in range(64):
            c=divmod(i,8)
           
            coord=pos1[c[1]]+pos2[c[0]]
            
            if s[i]!='z':
                p=d[s[i]]+coord
                chess+=p
                chess+=','
        
        chess=chess.strip(',')
        return chess
   

with open('fen.txt', 'r') as f:
    read_data = f.readlines()
f.close()  
board = Image.open('Board.tif')
im_mode=board.mode
board=board.convert('RGBA')
for line in read_data:
    board2=board.copy()
    line=fen2chess(line)
    Pieces=line.strip().split(',')
    i+=1
    for Piece in Pieces:
        fig=Piece[0:2]
        pos=[ 1+pos1.index(Piece[-2]), 9-int(Piece[-1])]
        fig_im = Image.open(fig+'.png')
        pos_x=int(pos[0]*w_board/8-w_board/16+x0-fig_im.size[0]/2)
        pos_y=int(pos[1]*h_board/8-h_board/16+y0-fig_im.size[1]/2)
        board2.alpha_composite(fig_im, (pos_x, pos_y))
              
    board2=board2.convert(im_mode)    
    board2.save('Board'+str(i)+'.png')
        
