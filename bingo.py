#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import sys
from pathlib import Path
from random import sample, shuffle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle, Spacer, Image

#CONST
SPACE = 2 
MARGIN = 0.5 * cm

OUTPUT = Path.cwd() / 'bingo-grid.pdf'
fo=str(OUTPUT.resolve())

doc = SimpleDocTemplate(fo,
                        pagesize = A4,
                        marginLeft = MARGIN ,
                        marginRight = MARGIN ,
                        marginTop = MARGIN ,
                        marginBottom = MARGIN ,
                        )

SIZE_CELL = ((A4[0] - (2 * MARGIN)) / 9)
GRIDS = 3

# get cli arguments

if (len(sys.argv) == 2):
    try :
        GRIDS = int(sys.argv[1])
    except ValueError:
        print("Bad value, try again ...")
        sys.exit()

#functions

def gen_grid(n):

    """"
    Return an array (3 list of 9 elements) of random figures
    fr - Renvoi un tableau (liste de 3 liste à 9 éléments) de nombre aléatoires
    """
    FILE_IMG = 'icone-bingo.png'
    I = Image (FILE_IMG)
    I.drawHeight = SIZE_CELL - 15
    I.drawWidth = SIZE_CELL - 15
    Grille = sample(tuple(range(1,n+1)),15)
    card = [Grille[:5],Grille[5:10], Grille[10:]]
    for l in card:
        l.extend([I]*4)
        shuffle(l)
    return card

def add_table(data):
    """
    reportlab table from a python list.
    fr - Création du tableau sur reportlab à partir d'une liste python
    """
    t=Table(data, colWidths = SIZE_CELL, rowHeights= SIZE_CELL, spaceAfter= SPACE * cm) 
    t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),1,colors.black),
                           ('FONTSIZE', (0,0), (-1,-1),28 ),
                           ('ALIGN',(0,0),(-1,-1),'CENTER'),
                           ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('RIGHTPADDING', (0,0), (-1,-1), 0),
                           ('LEFTPADDING', (0,0), (-1,-1), 0),
                           ('TOPPADDING', (0,0), (-1,-1), 0),
                           ('BOTTOMPADDING', (0,0), (-1,-1), 15),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                          ]))
    return t

def pdf(NUMBER) :
    styles = getSampleStyleSheet()
    styleN = styles['BodyText']
    story = []

    #add some flowables

    for i in range(NUMBER):
        story.append(add_table(gen_grid(90)))

    doc.build(story)

if __name__ == '__main__':
    
    pdf(GRIDS)
    print(f'le fichier se trouve à {fo}')
