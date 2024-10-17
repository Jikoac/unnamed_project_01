from base import *
def list_directories(path):
    entries = os.listdir(path)
    directories = [entry for entry in entries if os.path.isdir(os.path.join(path, entry))]
    return directories
mods=list_directories(str(path.mod))
mods.remove('__pycache__')
active_mods=dict(zip(mods,[False]*len(mods)))
def display_mods():
    loc=50
    screen.fill((0,60,50))
    for mod in mods:
        mod_path=path.mod_path(path.mod+mod)
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
        screen.blit(resize(image,(500,500)),(710,loc+game.scroll))
        if active_mods[mod]:
            name=font.render(title,True,(0,255,0))
        else:
            name=font.render(title,True,(255,255,255))
        screen.blit(name,(710,loc+525+game.scroll))
        loc+=575
    pg.display.flip()

def mod_scroll():
    for event in game.event_cache:
        if event.type==pg.MOUSEWHEEL:
            game.scroll+=event.y*25
        elif event.type==pg.MOUSEBUTTONDOWN:
            if event.button==2:
                game.scroll=0

def select_mods():
    pg.time.delay(500)
    running=True
    while running:
        game.events=pg.event.get()
        for event in game.events:
            if event.type==pg.QUIT:
                running=False
            elif event.type==pg.MOUSEBUTTONDOWN or event.type==pg.MOUSEWHEEL:
                game.event_cache.append(event)
        mod_scroll()
        display_mods()
        loc=50
        for mod in mods:
            if button(710,loc+game.scroll,500,500):
                active_mods[mod]=not active_mods[mod]
                loc+=575
        keys=pg.key.get_pressed()
        if keys[pg.K_RETURN] or keys[pg.K_ESCAPE]:
            running=False
        game.event_cache=[]
    return [mod for mod in mods if active_mods[mod]]