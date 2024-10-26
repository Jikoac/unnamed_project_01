from mod_setup import *
def list_directories(path):
    entries = os.listdir(path)
    directories = [entry for entry in entries if os.path.isdir(os.path.join(path, entry))]
    return directories

def activate_mods():
    mods=select_mods()
    imports=['items','ai','loot_tables','projectiles','mobs','other']
    import_data={'items':'item_data','ai':'ai_data','loot_tables':'loot_table_data','projectiles':'projectile_data','mobs':'mob_data'}
    for i in imports:
        f=open(path.code(i),'w')
        try:
            write_data=f'import os\nimport sys\nfrom {import_data[i]} import *\n'
        except: write_data='import os\nimport sys\n'
        for mod in mods:
            write_data+=f'try:\n    from {mod}.data.{i} import *\nexcept: None\n'
        f.write(write_data)
        f.close()
    write_data='''import sys
import os
mod_path = os.path.join(os.path.dirname(__file__), "..", "mods")
sys.path.append(mod_path)
mod_generators=[]
mod_upgrades=[]\n'''
    for mod in mods:
        write_data+=f'''
try:
    import {mod}.data.spawn_rules as {mod}_spawn
    mod_generators+={mod}_spawn.generators
except: None
try:
    import {mod}.data.upgrades as {mod}_upgrades
    mod_upgrades+={mod}_upgrades.upgrades
except: None\n'''
    write_data+='''from items import *
from ai import *
from loot_tables import *
from projectiles import *
from mobs import *
from other import *'''
    f=open(path.code('mod_imports'),'w')
    f.write(write_data)
    f.close()
    project_code_path = os.path.abspath(os.path.join(os.path.dirname(__file__),  '..'))
    sys.path.append(project_code_path)
    project_code_path = os.path.abspath(os.path.join(os.path.dirname(__file__),  '..','mods'))
    sys.path.append(project_code_path)
    '{mod}_path = os.path.join(os.path.dirname(__file__), "..", "mods", {mod}, "code")'
from mod_imports import *