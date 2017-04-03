#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
svp module access is done by 

import svp
get_players() / remove_player
get_displays() / remove_display

"""

from svp.layer import Layer
from svp.window import Window
from svp.Sources.player import Player

__players__ = Player.__players__
__windows__ = Window.__windows__
__layers__ = Layer.__layers__

def get_players():
	return __players__

def get_windows():
	return __windows__

def get_layers():
	return __layers__