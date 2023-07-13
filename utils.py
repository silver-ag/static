import PySimpleGUI as PSG
import numpy as np

def scope(*snds):
    colors = ['pink','green','blue','orange','purple','white']
    graph = PSG.Graph(canvas_size=(600,200), background_color='black', graph_bottom_left = (0,-1), graph_top_right=(1,1))
    layout = [[graph],
              [PSG.Text('Start'), PSG.Slider(range=(0, max([s.length for s in snds])), orientation = 'h', resolution = 0.001, default_value = 0, enable_events = True, key='start'),
               PSG.Button('Redraw')],
              [PSG.Text('Range'), PSG.Slider(range=(0, 1), orientation = 'h', resolution = 0.00001, default_value = 0.1, enable_events = True, key='range')]]
    window = PSG.Window('scope', layout, finalize = True)
    def draw(snd, range, start, color):
        prev = (0,0)
        for i in np.linspace(0, 1, (int)(16000*range)):
            graph.draw_line(prev, (i, snd.f((i*range)+start)), color = color)
            prev = (i, snd.f((i*range)+start))
    for i in range(len(snds)):
        draw(snds[i], 0.1, 0, colors[i])
    while True:
        e,v = window.read()
        if e == PSG.WINDOW_CLOSED:
            break
        elif e == 'Redraw':
            graph.erase()
            for i in range(len(snds)):
                draw(snds[i], v['range'], v['start'], colors[i])
    window.close()
