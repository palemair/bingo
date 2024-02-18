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

#CONSTANTES
ESPACE = 2 
RACINE = Path('/usr/local/include/images')
MARGES = 0.5 * cm
rec= Path.cwd() / 'Grilles-bingo.pdf'
u=str(rec.resolve())

doc = SimpleDocTemplate(u,
                        pagesize = A4,
                        marginLeft = MARGES ,
                        marginRight = MARGES ,
                        marginTop = MARGES ,
                        marginBottom = MARGES ,
                        )

# grid quantity on shell demand

if (len(sys.argv) == 1):
    NOMBRE_DE_GRILLES = 3
else:
    NOMBRE_DE_GRILLES = int(sys.argv[1])

#fonctions
def Calcul_taille_cellule(largeur_totale,marge,quantité):
    return ((largeur_totale - 2 * marge) / quantité) 

TAILLE = Calcul_taille_cellule(A4[0],MARGES,9)


def gen_grille(n):

    """"
    Return array (3 list of 9 elements) of random figures
    fr - Renvoi un tableau (liste de 3 liste à 9 éléments) de nombre aléatoires
    """
    fich = RACINE / 'icone-bingo.png'
    f = str(fich.resolve())
    I = Image (f)
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
    t=Table(data, colWidths = TAILLE, rowHeights= TAILLE, spaceAfter= ESPACE * cm) 
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
    
    Gen_pdf(NOMBRE_DE_GRILLES)
    print(f'le fichier se trouve à {u}')
