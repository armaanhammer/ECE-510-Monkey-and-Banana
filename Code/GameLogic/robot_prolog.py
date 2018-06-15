# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 18:59:46 2018

@author: etcyl
"""

from prolog import Prolog
from easy import *

prolog = Prolog()
prolog.consult("final_proj.pl")

x = bool(list(prolog.query("atGoal(10, 10, 10, 10)")))
y = bool(list(prolog.query("atGoal(15, 15, 10, 10)")))
