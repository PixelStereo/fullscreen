#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
api access to __players__ and __displays__ 
"""

from svp.player import Player
from svp.display import Display
from svp import __displays__, __players__

def new_player(name=None, filepath=None):
	player = Player(name, filepath)
	__players__.append(player)
	return player

def get_players():
	return __players__

def new_display(*args, **kwargs):
	display = Display(*args, **kwargs)
	__displays__.append(display)
	return display

def get_displays():
	return __displays__