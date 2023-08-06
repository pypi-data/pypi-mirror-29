"""
OsensaPlot: A Python module for plotting vectors into a 3D space

Created on Thur Jan 11 12:25:33 2018

@author: Caleb Ng
"""

__author__   = 'Caleb Ng'
__url__      = 'https://github.com/osensa/osensaimos'
__license__  = 'MIT License'

__version__  = '0.0.1'
__status__   = 'Beta'

from vpython import *
import math


# Axes components
xtext = None
ytext = None
ztext = None
xaxis = None
yaxis = None
zaxis = None
centerbox = None

class Pointer:
    def __init__(self, cone, ball):
        self.cone = cone
        self.ball = ball

def calcRadius(v):
    if (math.sqrt(mag(v))*0.10 < 0.10):
        return 0.10
    else:
        return math.sqrt(mag(v))*0.10

def drawVector(v, _color):
    center = vector(0,0,0)
    _radius = 0.10 #calcRadius(v)
    # if (_radius < 0.10):
    #     _radius = 0.10
    c = cone(pos=center, axis=v, radius=_radius, color=_color)
    b = sphere(pos=center, radius=_radius, color=_color)
    return Pointer(c, b)

def drawAxes(len):
    global xtext, ytext, ztext, xaxis, yaxis, zaxis, centerbox
    center = vector(0,0,0)
    upd = vector(0,0,1)
#    len = 2
    if (len/5) > 1:
        h = 1
    else:
        h = len/5
    # Draw text labels
    if xtext is not None:
        xtext.pos = vector(len+h,0,0)
        xtext.text = 'X (+{})'.format(len)
    else:
        xtext = label(pos=vector(len+h,0,0), text='X (+{})'.format(len), align='center', box=False, color=color.white)    
    if ytext is not None:
        ytext.pos = vector(0,len+h,0)
        ytext.text = 'Y (+{})'.format(len)
    else:
        ytext = label(pos=vector(0,len+h,0), text='Y (+{})'.format(len), align='center', box=False, color=color.white)
    if ztext is not None:
        ztext.pos = vector(0,0,len+h)
        ztext.text = 'Z (+{})'.format(len)
    else:
        ztext = label(pos=vector(0,0,len+h), text='Z (+{})'.format(len), align='center', box=False, color=color.white)
    # Draw axis arrows
    if xaxis is None:
        xaxis = arrow(pos=center, axis=vector(len,0,0), shaftwidth=0.1, color=color.white)
    else:
        xaxis.axis = vector(len,0,0)
    if yaxis is None:
        yaxis = arrow(pos=center, axis=vector(0,len,0), shaftwidth=0.1, color=color.white)
    else:
        yaxis.axis = vector(0,len,0)
    if zaxis is None:
        zaxis = arrow(pos=center, axis=vector(0,0,len), shaftwidth=0.1, color=color.white)
    else:
        zaxis.axis = vector(0,0,len)
    # Draw center cube
    if centerbox is None:
        centerbox = box(pos=center, length=0.1, height=0.1, width=0.1)

def resetView():
    scene.up = vector(0,0,1)
    scene.forward = vector(-1,-1,-1)
    scene.camera.pos = vector(1,1,1)
    scene.center = vector(0,0,0)

def initializeView():
    resetView()
    drawAxes(2)
    # scene.autoscale = True
    scene.autoscale = False

    def buttonReset(b):
        resetView()
        # scene.autoscale = True
        # scene.autoscale = False
    button(bind=buttonReset, text='Reset View')
    def buttonAutoScale(b):
        scene.autoscale = not scene.autoscale
        if scene.autoscale:
            b.text = 'Autoscale: ON'
        else:
            b.text = 'Autoscale: OFF'
    button(bind=buttonAutoScale, text='Autoscale: OFF')
    def sliderAction(s):
        drawAxes(s.value)
    slider(bind=sliderAction, min=1, max=20, step=1, value=2, left=20, right=20, top=5, bottom=5)
    
# initializeView()
