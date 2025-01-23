#!./env/bin/python3
#-*- coding: utf-8 -*-
import sys
from pathlib import Path
from collections.abc import Sequence
from itertools import islice
from random import randrange
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle, Spacer, Image

def add_table(data):
    """
    reportlab table from a python list.
    fr - Création du tableau avec reportlab à partir d'une liste python
    """
    t=Table(data, colWidths = SIZE_CELL, rowHeights= SIZE_CELL, spaceAfter= SPACE * cm) 
    t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),1,colors.black),
                           ('FONTSIZE', (0,0), (-1,-1),30),
                           ('ALIGN',(0,0),(-1,-1),'CENTER'),
                           ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('RIGHTPADDING', (0,0), (-1,-1), 0),
                           ('LEFTPADDING', (0,0), (-1,-1), 0),
                           ('TOPPADDING', (0,0), (-1,-1), 0),
                           ('BOTTOMPADDING', (0,0), (-1,-1), 24),
                           ('BOX', (0,0), (-1,-1), 0.2, colors.black),
                          ]))
    return t

# get cli arguments


#functions
def get_sample(data : Sequence, nb : int)->list:
    
    ensemble = list(data)
    assert(len(ensemble) >= nb) and (nb >= 1)
    return [ensemble.pop(randrange(len(ensemble))) for x in range(nb)]

def melange(data : list)->list:
    
    if len(data) >= 1: 
        for j in range(len(data) - 1,1,-1):
            index = randrange(0,j-1)
            data[index],data[j] = data[j],data[index]
    return data

def batch(iterable : Sequence, n : int) -> list:

    assert (n>1) and n<len(iterable)
    new = iter(iterable)
    while ret := list(islice(new,n)):
        yield ret

def gen_grid(n : int, image):

    """"
    Return an array (3 list of 9 elements) of random figures
    fr - Renvoi un tableau (3 listes de 9 éléments) de nombre aléatoires
    """

    Grille = get_sample(tuple(range(1,n+1)),15)
    card = list(batch(Grille,5))

    for l in card:
        l.extend([image]*4)
        melange(l)
    return card

if __name__ == '__main__':
    
    #CONST
    SPACE = 2 
    MARGIN = 0.5 * cm
    SIZE_CELL = ((A4[0] - (2 * MARGIN)) / 9)
    FILE_IMG = 'icone-bingo.png'

    OUTPUT = Path.cwd() / 'bingo-grid.pdf'
    fo=str(OUTPUT.resolve())

    I = Image(FILE_IMG)
    I.drawHeight, I.drawWidth = (SIZE_CELL - 15,) * 2

    doc = SimpleDocTemplate(fo,
                            pagesize = A4,
                            marginLeft = MARGIN ,
                            marginRight = MARGIN ,
                            marginTop = MARGIN ,
                            marginBottom = MARGIN ,
                            )

    if (len(sys.argv) == 2):
        try :
            GRIDS = int(sys.argv[1])
        except ValueError:
            print("Bad value, try again ...")
            sys.exit()
    else :
        GRIDS = 3

    styles = getSampleStyleSheet()
    styleN = styles['BodyText']
    story = [add_table(gen_grid(90,I)) for x in range(GRIDS)]
    doc.build(story)
    print(f'le fichier se trouve à {fo}')
