#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
api access to __players__ and __displays__ 
"""

from svp.player import Player, SmartPlayer
from svp.display import Display
from svp.displayGL import DisplayGL
from svp import __displays__, __players__

def new_player(name=None, filepath=None):
	player = Player(name, filepath)
	__players__.append(player)
	return player

def new_smart_player(name=None, filepath=None):
	smart_player = SmartPlayer(name, filepath)
	__players__.append(smart_player)
	return smart_player

def get_players():
	return __players__

def new_display(*args, **kwargs):
	if 'mode' in kwargs.keys():
		display = DisplayGL(*args, **kwargs)
	else:
		display = Display(*args, **kwargs)
	__displays__.append(display)
	return display

def get_displays():
	return __displays__