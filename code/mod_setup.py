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
        try:
            image=pg.image.load(mod_path+'icon.png')
        except:
            image=error_texture
        try:
            f=open(mod_path+'title.txt','r')
            title=f.read()
            f.close()
        except:
            title=mod
        screen.blit(image,(710,loc))
        name=font.render(title,True,(255,255,255))
        screen.blit(name,(710,loc+525))
        loc+=575
display_mods()