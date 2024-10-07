import sys
import os
mod_path = os.path.join(os.path.dirname(__file__), "..", "mods")
sys.path.append(mod_path)
mod_generators=[]
mod_upgrades=[]

try:
    import example_mod.data.spawn_rules as example_mod_spawn
    mod_generators+=example_mod_spawn.generators
except: None
try:
    import example_mod.data.upgrades as example_mod_upgrades
    mod_upgrades+=example_mod_upgrades.upgrades
except: None
from items import *
from ai import *
from loot_tables import *
from projectiles import *
from mobs import *
from other import *