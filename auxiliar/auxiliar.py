# -*- coding: UTF-8 -*-
from qgis.core import *
import math
import string
import os

class Auxiliar(object):
    
    def __init__(self, iface):
        super(Auxiliar, self).__init__()
        self.iface = iface
        self.initVariables()
    
    def openFiles(self):
        filePath = os.path.dirname(os.path.dirname(__file__))
        self.filePath250 = os.path.join(filePath, "auxiliar", "MIR250.csv")
        self.filePath100 = os.path.join(filePath, "auxiliar", "MI100.csv")
        self.file250 = open(self.filePath250, 'r')
        self.file100 = open(self.filePath100, 'r')
    
    def closeFiles(self):
        self.file250.close()
        self.file100.close()

    def initVariables(self):
        alpha = string.ascii_uppercase
        self.alphabet = {i: alpha[i-1] for i in range(1,len(alpha)+1)}
        self.pos500 = {
            0: "V",
            1: "X",
            2: "Y",
            3: "Z"
        }
        self.pos250 = {
            0: "A",
            1: "B",
            2: "C",
            3: "D"
        }
        self.pos100 = {
            0: "I",
            1: "II",
            2: "III",
            3: "IV",
            4: "V",
            5: "VI"
        }
        self.pos50 = {
            0: "1",
            1: "2",
            2: "3",
            3: "4"
        }
        self.pos25 = {
            0: "NO",
            1: "NE",
            2: "SO",
            3: "SE"
        }
        
    def calculaCarta(self, point, escala):
        nomeFolha = ""
        limit = {
            250: 0,
            100: 1,
            50 : 2,
            25 : 3
            }[escala]
        
        scaleX = 6.0
        scaleY = 4.0
        
        # VERIFICAR HEMISFERIO
        sign = -1 if point.y() < 0 else 1
        hemisferio = 'N' if sign == 1 else 'S'
        nomeFolha += hemisferio
        
        # VERIFICAR POSIÇÃO EM LATITUDE
        linha = int(point.y()/4) + sign
        linhaAlpha = self.alphabet[sign*linha]
        nomeFolha += linhaAlpha
        nomeFolha += '-'
        
        # VERIFICAR FUSO
        fuso = 30 + int(point.x()/6)
        nomeFolha += str(fuso)
        nomeFolha += '-'
        
        # VERIFICAR ARTICULAÇÃO 1:500.000
        esqFuso = -180 + (fuso-1) * 6
        infFuso = linha * 4
                
        pos500 = -1
        
        scaleX /= 2
        scaleY /= 2
        
        if sign == 1:
            infFuso = (linha-1) * 4
        
        if point.x() < esqFuso + scaleX:
            if point.y() > infFuso + scaleY:
                pos500 = 0
            else:
                pos500 = 2
        else:
            if point.y() > infFuso + scaleY:
                pos500 = 1
            else:
                pos500 = 3
                
        pos500L = self.pos500[pos500]
        
        nomeFolha += pos500L
        nomeFolha += '-'
        
        # VERIFICAR ARTICULAÇÃO 1:250.000
        esqFuso = esqFuso + int(pos500%2)*scaleX
        inf = 0 if pos500 > 1 else 1
        infFuso = infFuso + inf*scaleY
        
        pos250 = -1

        scaleX /= 2
        scaleY /= 2
        
        if point.x() < esqFuso + scaleX:
            if point.y() > infFuso + scaleY:
                pos250 = 0
            else:
                pos250 = 2
        else:
            if point.y() > infFuso + scaleY:
                pos250 = 1
            else:
                pos250 = 3
        
        pos250L = self.pos250[pos250]
        
        nomeFolha += pos250L

        if limit == 0:
            miFolha = self.findMI(nomeFolha, self.file250)
            return (nomeFolha, miFolha) 
        nomeFolha += '-'
        
        # VERIFICAR ARTICULAÇÃO 1:100.000
        esqFuso = esqFuso + int(pos250%2)*scaleX
        inf = 0 if pos250 > 1 else 1
        infFuso = infFuso + inf*scaleY
        
        pos100 = -1
        
        scaleX /= 3
        scaleY /= 2
        
        if point.x() < esqFuso + scaleX:
            if point.y() > infFuso + scaleY:
                pos100 = 0
            else:
                pos100 = 3
        elif point.x() < esqFuso + scaleX*2:
            if point.y() > infFuso + scaleY:
                pos100 = 1
            else:
                pos100 = 4
        else:
            if point.y() > infFuso + scaleY:
                pos100 = 2
            else:
                pos100 = 5
        
        pos100L = self.pos100[pos100]
        
        nomeFolha += pos100L
        if limit == 1:
            miFolha = self.findMI(nomeFolha, self.file100)
            return (nomeFolha, miFolha)
        
        miFolha = self.findMI(nomeFolha, self.file100)
        miFolha += "-"
        nomeFolha += '-'
        
        # VERIFICAR ARTICULAÇÃO 1:50.000        
        esqFuso = esqFuso + int(pos100%3)*scaleX
        inf = 0 if pos100 > 2 else 1
        infFuso = infFuso + inf*scaleY
        
        pos50 = -1
        scaleX /= 2
        scaleY /= 2
        
        if point.x() < esqFuso + scaleX:
            if point.y() > infFuso + scaleY:
                pos50 = 0
            else:
                pos50 = 2
        else:
            if point.y() > infFuso + scaleY:
                pos50 = 1
            else:
                pos50 = 3
        
        pos50L = self.pos50[pos50]
        
        nomeFolha += pos50L
        miFolha += pos50L
        
        if limit == 2:
            return (nomeFolha, miFolha)
        nomeFolha += '-'
        miFolha += "-"
        
        # VERIFICAR ARTICULAÇÃO 1:25.000        
        esqFuso = esqFuso + int(pos50%2)*scaleX
        inf = 0 if pos50 > 1 else 1
        infFuso = infFuso + inf*scaleY
        
        pos25 = -1

        scaleX /= 2
        scaleY /= 2
        
        if point.x() < esqFuso + scaleX:
            if point.y() > infFuso + scaleY:
                infFuso = infFuso + scaleY
                pos25 = 0
            else:
                pos25 = 2
        else:
            esqFuso = esqFuso + scaleX
            if point.y() > infFuso + scaleY:
                infFuso = infFuso + scaleY
                pos25 = 1
            else:
                pos25 = 3
        
        pos25L = self.pos25[pos25]
        
        nomeFolha += pos25L
        miFolha += pos25L
        
        rect = QgsRectangle(esqFuso, infFuso, esqFuso + scaleX, infFuso + scaleY)
        
        return (nomeFolha, miFolha, rect)
                
    def findMI(self, nome, arq):
        for l in arq:
            line = l.split(";")
            if line[0] == nome:
                arq.seek(0)
                return line[1].rstrip()
        arq.seek(0)
        
        return ""



