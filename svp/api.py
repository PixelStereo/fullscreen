#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
api access to __players__ and __displays__ 
"""

from player import Player
from display import Display
from __init__ import __displays__, __players__

def new_player(name='Untitled'):
	player = Player(name)
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