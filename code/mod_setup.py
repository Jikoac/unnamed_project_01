from base import *
def list_directories(path):
    entries = os.listdir(path)
    directories = [entry for entry in entries if os.path.isdir(os.path.join(path, entry))]
    return directories
mods=list_directories(str(path.mod))
mods.remove('__pycache__')
def display_mods():
    loc=50
    for mod in mods:
        mod_path=path.mod_path(path.main+mod)
        image=pg.image.load(mod_path+'icon.png')
        screen.blit(image,(710,loc))
display_mods()