#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
svp module access is done by 

import svp
get_players() / remove_player
get_displays() / remove_display

"""

from svp.display import Display
from svp.player import Player

__players__ = Player.__players__
__displays__ = Display.__displays__

def get_players():
	return __players__

def get_displays():
	return __displays__