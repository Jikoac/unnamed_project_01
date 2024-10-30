import sys
import os
mod_path = os.path.join(os.path.dirname(__file__), "..", "mods")
sys.path.append(mod_path)
mod_generators=[]
mod_upgrades=[]
from items import *
from ai import *
from loot_tables import *
from projectiles import *
from mobs import *
from other import *