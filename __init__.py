# -*- coding: utf-8 -*-

from main import Main

def name():
    return "MapFinder Brasil"

def description():
    return "Find the topographical chart (nomenclature index and index map - Brazil) that covers a defined area or a selected feature."

def version():
    return "Version 1.0"

def classFactory(iface):
    return Main(iface)

def qgisMinimumVersion():
    return "2.0"

def author():
    return "Diego Benincasa"

def email():
    return "diego@diegobenincasa.com"

def icon():
    return "icons/main.png"