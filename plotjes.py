"""
Bio-Informatica project met toolbox

Auteurs: Vani Rembant, Lucas Bos en Jasmijn Peterse
Datum: 25/03 -
Versie: 1.0
"""

import matplotlib.pyplot as plt

def plot_mutatie():
    with open('empty.vcf', 'r') as f:
        lines = f.readlines()
        if lines[0].startswith('#'):
            return
        if lines[5]:
            print("hallo world")