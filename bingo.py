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

#CONSTANTS
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

# grid quantity on shell demand

if (len(sys.argv) == 1):
    GRIDS = 3
else:
    GRIDS = int(sys.argv[1])

#functions
def Calcul_taille_cellule(largeur_totale,marge,quantité):
    return ((largeur_totale - 2 * marge) / quantité) 

TAILLE = Calcul_taille_cellule(A4[0],MARGIN,9)


def gen_grille(n):

    """"
    Return array (3 list of 9 elements) of random figures
    fr - Renvoi un tableau (liste de 3 liste à 9 éléments) de nombre aléatoires
    """
    fich = 'icone-bingo.png'
    I = Image (fich)
    I.drawHeight = TAILLE - 15
    I.drawWidth = TAILLE - 15
    Grille = sample(tuple(range(1,n+1)),15)
    carton = [Grille[:5],Grille[5:10], Grille[10:]]
    for l in carton:
        l.extend([I]*4)
        shuffle(l)
    return carton

def ajout_table(data):
    """
    Création du tableau sur reportlab à partir d'une liste python
    """
    t=Table(data, colWidths = TAILLE, rowHeights= TAILLE, spaceAfter= SPACE * cm) 
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

def Gen_pdf(NOMBRE) :
    styles = getSampleStyleSheet()
    styleN = styles['BodyText']
    story = []

    #add some flowables

    for i in range(NOMBRE):
        story.append(ajout_table(gen_grille(90)))

    doc.build(story)

if __name__ == '__main__':
    
    Gen_pdf(GRIDS)
    print(f'le fichier se trouve à {fo}')
