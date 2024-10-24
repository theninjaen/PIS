# 1 Import
import PySimpleGUI as sg
import os
from random import randint


layout = [[sg.Text('Snake Game - PySimpleGUI + PyGame')],
          [sg.Graph((800, 600), (0, 0), (800, 600),
                    background_color='lightblue', key='-GRAPH-')],
          [sg.Exit()]]

window = sg.Window('Snake Game using PySimpleGUI and PyGame',
                   layout, finalize=True)


while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

window.close()