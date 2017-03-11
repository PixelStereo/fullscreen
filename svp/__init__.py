#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
svp module access is done by 
get_players() / add_player / remove_player
get_displays() / add_display / remove_display
"""

import numpy as np
import cv2
import os

from player import Player
from display import Display

__players__ = []
def new_player(name='Untitled'):
	player = Player(name)
	__players__.append(player)
	return player

def get_players():
	return __players__

__displays__ = []
def new_display(name='Untitled', visible=True):
	display = Display(name, visible)
	__displays__.append(display)
	return display

def get_displays():
	return __displays__