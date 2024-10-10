from mod_import_config import *

def update(image:pg.Surface=none,pos:tuple=(0,0)):
    screen.blit(image,pos)
    pg.display.flip()

def display(show:bool=True):
    screen.blit(background,(0,0))
    screen.blit(ground,((1920-player.x)%1920,1030))
    screen.blit(ground,(((1920-player.x)%1920)-1920,1030))
    screen.blit(ground,(((1920-player.x)%1920)+1920,1030))
    if player.control.attack>0:
        screen.blit(player.attack.texture,(player.attack.x-player.x+(960-player.width//2),1030-player.attack.height-player.attack.y))
    if player.control.shield and player.can_shield:
        screen.blit(player.shield.texture,(player.shield.x-player.x+(960-player.width//2),1030-player.shield.height-player.shield.y))
    for mob in game.mobs.values():
        screen.blit(mob.texture,
                    (mob.x-player.x+mob.texture_offset[0]+(960-player.width//2),
                    1030-mob.height-mob.y+mob.texture_offset[1]))
    screen.blit(player.texture,(960-player.width//2,1030-player.height-player.y))
    if player.armor:
        screen.blit(player.armor_textures[player.facing],(960-player.width//2,1030-player.height-player.y))
    loc=50
    for i in player.loot:
        try:
            it=eval(i)
        except:
            it=i
        try:
            screen.blit(resize(it.texture,(100,100)),(loc+game.scroll_items,50))
        except:
            screen.blit(resize(error_texture,(100,100)),(loc,50))
        item_count=font.render(str(player.loot[i]),True,(255,255,255))
        item_name=font.render(str(it.name),True,(255,255,255))
        screen.blit(item_count,(loc+75+game.scroll_items,175))
        screen.blit(item_name,(loc+game.scroll_items,25))
        loc+=150
    name=font.render(f'{str(game.level)}. {player.name}',True,(255,255,255))
    health=font.render(f'{str(player.hp)}/{str(player.max_hp)}',True,(255,255,255))
    screen.blit(name,(1895-name.get_width(),25))
    screen.blit(health,(1895-health.get_width(),50))
    screen.blit(heart,(1877-health.get_width(),51))
    if show:
        update()

def pause_display():
    display(False)
    loc=50
    for upgrade in upgrades:
        if game.level>=upgrade.level and upgrade.max>0 and loc+game.scroll<1920:
            if loc+game.scroll>-500:
                screen.blit(resize(upgrade.texture,(500,500)),(loc+game.scroll,250))
                upgrade_name=font.render(upgrade.name,True,upgrade.name_color)
                screen.blit(upgrade_name,(loc+game.scroll,800))
                pg.draw.rect(screen,(255,255,255),pg.Rect(loc+game.scroll-2,248,504,504),2)
                if upgrade.show_uses:
                    uses_tooltip(loc+game.scroll,250,500,500,str(upgrade.max))
                item_loc=0
                for item in upgrade.items:
                    if has_enough(item,upgrade.items[item]):
                        text_color=(255,255,255)
                    else:
                        text_color=(255,0,0)
                    item_count=font.render(str(upgrade.items[item]),True,text_color)
                    try:item=eval(item)
                    except:None
                    try:
                        screen.blit(resize(item.texture,(50,50)),(loc+item_loc+game.scroll,850))
                    except:
                        screen.blit(resize(error_texture,(50,50)),(loc+item_loc+game.scroll,850))
                    screen.blit(item_count,(loc+item_loc+game.scroll,925))
                    item_loc+=75
            loc+=550
    score=font.render(str(player.xp),True,(0,255,0))
    screen.blit(score,(1895-score.get_width(),75))
#    loc=50
#    for i in player.loot:
#        try:
#            it=eval(i)
#        except:
#            it=i
#        highlight(loc,50,100,100,it.name)
#        loc+=150
    update()

def button(x, y, width, height, color=None):
    box_rect = pg.Rect(x, y, width, height)
    if color!=None:
        pg.draw.rect(screen, color, box_rect)
    for event in game.event_cache:
        if event.type==pg.MOUSEBUTTONDOWN and event.button==1:
            if pg.mouse.get_pos()==in_rect(box_rect):
                return True
    if player.control.select and pg.mouse.get_pos()==in_rect(box_rect):
        return True
    return False

def highlight(x, y, width, height, text=''):
    box_rect = pg.Rect(x, y, width, height)
    if pg.mouse.get_pos()==in_rect(box_rect):
        mouse=pg.mouse.get_pos()
        tooltip=font.render(text,True,(255,255,255))
        pos=tooltip.get_rect(center=mouse)
        screen.blit(tooltip,(pos[0],pos[1]-10))
        return True
    return False

def uses_tooltip(x, y, width, height, text=''):
    box_rect = pg.Rect(x, y, width, height)
    if pg.mouse.get_pos()==in_rect(box_rect):
        mouse=pg.mouse.get_pos()
        tooltip=font.render(text,True,(255,255,255))
        pos=tooltip.get_rect(center=mouse)
        screen.blit(tooltip,(pos[0],pos[1]-10))
        return True
    return False

def debug_button():
    keys=pg.key.get_pressed()
    if keys[pg.K_LCTRL] and keys[pg.K_d] and pg.mouse.get_pos()[1]<50:
        return True
    return False

class text_box:
    def __init__(self, coords, size=(500,32), default='', color_deselected=(200, 200, 200), color_selected=(255, 255, 255),empty:bool=False,selected_by_default:bool=False,cursor:bool=True):
        self.coords = coords
        self.size = size
        self.default = default
        self.color_deselected = color_deselected
        self.color_selected = color_selected
        self.selected = selected_by_default
        self.text = ''
        self.font = pg.font.Font(None, 32)
        self.rect = pg.Rect(coords, size)
        self.empty=empty
        self.cursor=cursor

    def draw(self):
        # Draw the text box
        color = self.color_selected if self.selected else self.color_deselected
        pg.draw.rect(screen, color, self.rect, 2)

        # Render the text
        display_text = self.text if self.text else self.default
        if self.cursor and self.text and self.selected:display_text+='|'
        text_surface = self.font.render(display_text, True, color)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # Check if the text box is clicked
            if self.rect.collidepoint(event.pos):
                self.selected = True
            else:
                self.selected = False
        if event.type == pg.KEYDOWN and self.selected:
            if event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pg.K_RETURN:
                return self.text
            else:
                self.text += event.unicode
        return None

    def __call__(self):
        for event in game.events:
            result = self.handle_event(event)
            if result is not None:
                if self.empty:
                    self.text=''
                return result
        return None

def start():
    running=True
    name_box=text_box((710,524),(500,32),'Name',(0,180,150),selected_by_default=True)
    while running:
        keys=pg.key.get_pressed()
        game.events=pg.event.get()
        for event in game.events:
            if event.type==pg.QUIT:
                running=False
                return True
        screen.fill((0,60,50))
        name_box.draw()
        pg.display.flip()
        name=name_box()
        if name!=None:
            player.name='Player'
            if name:
                player.name=name
            running=False
        if keys[pg.K_LCTRL] and keys[pg.K_q]:
            return True
    return False

def scroll():
    for event in game.event_cache:
        if event.type==pg.MOUSEWHEEL:
            if pg.mouse.get_pos()[1]>=250:
                game.scroll+=event.y*25
            else:
                game.scroll_items+=event.y*25
        elif event.type==pg.MOUSEBUTTONDOWN:
            if event.button==2:
                game.scroll_items=0

def loop():
    running=True
    paused=False
    fullscreen=True
    game_tick = pg.USEREVENT + 1
    pg.time.set_timer(game_tick, 10)
    if game.music:
        pg.mixer.music.play(-1)
    while running:
        game.events=pg.event.get()
        for event in game.events:
            if event.type==pg.QUIT:
                running=False
            elif event.type==pg.KEYDOWN:
                if event.key==pg.K_f:
                    fullscreen=not fullscreen
                    if fullscreen:
                        screen=pg.display.set_mode((1920,1080),pg.FULLSCREEN|pg.DOUBLEBUF|pg.HWSURFACE)
                    else:
                        screen=pg.display.set_mode((1920,1080),pg.DOUBLEBUF|pg.HWSURFACE)
            elif event.type==pg.MOUSEBUTTONDOWN or event.type==pg.MOUSEWHEEL:
                game.event_cache.append(event)
            elif event.type == pg.ACTIVEEVENT:
                if event.state == pg.APPACTIVE:
                    if event.gain == 0 and fullscreen:
                        paused=True
            elif event.type==game_tick:
                game.get_clicked()
                game.dead=[]
                game.level_up()
                keys=pg.key.get_pressed()
                if keys[pg.K_LCTRL] and keys[pg.K_q]:
                    running=False
                if paused:
                    player.control.get_select()
                    player.control.move_mouse()
                    pg.mouse.set_visible(True)
                    scroll()
                    if game.keys['pause'].click or game.keys['esc'].click:
                        paused=False
                    up_loc=50
                    for upgrade in upgrades:
                        if game.level>=upgrade.level and upgrade.max>0:
                            if button(up_loc+game.scroll,250,500,500):
                                if upgrade():
                                    player.jump_sound.play()
                                else:
                                    player.shield.sound.play()
                            up_loc+=550
                    if debug_button():
                        debug_mode()
                    pause_display()
                else:
                    game.scroll=0
                    pg.mouse.set_visible(False)
                    if game.keys['pause'].click or game.keys['esc'].click:
                        paused=True
                        pg.mouse.set_pos(960,540)
                    for generator in generators:
                        generator()
                    game.spawn_queue={}
                    game.despawn_queue=[]
                    for mob in game.mobs.values():
                        mob()
                        if player.control.shield and player.can_shield and mob.collide(player.shield):
                            if mob.special_ai=='straight_line':
                                mob.facing=player.shield.facing
                            elif player.facing=='left':
                                mob.x-=2*mob.speed*player.knockback
                            else:
                                mob.x+=2*mob.speed*player.knockback
                        if player.control.attack and mob.collide(player.attack):
                            mob.health-=player.damage
                            if mob.health>0:
                                player.attack.power-=1
                            if player.attack.power==0:
                                player.control.attack=0
                        if mob.is_dead():
                            game.dead.append(mob.id)
                        if (mob.x<player.x-1500 or mob.x>player.x+1500) and mob.special_ai=='straight_line' and mob==away_from_player():
                            game.despawn_queue.append(mob.id)
                        if not mob.cooldown and mob.is_hostile and mob.collide(player):
                            if player.control.shield and player.can_guard:
                                if randrange(round(100/(player.armor*1.5))):
                                    player.hp-=mob.damage
                                else:
                                    player.shield.sound.play()
                            elif player.armor:
                                if randrange(round(100/player.armor)):
                                    player.hp-=mob.damage
                                else:
                                    player.shield.sound.play()
                            else:
                                player.hp-=mob.damage
                            mob.health-=round(mob.damage*player.reflection/100)
                            mob.cooldown=100
                        else:
                            mob.cooldown=max(0,mob.cooldown-1)
                    game.mobs.update(game.spawn_queue)
                    for mob_id in game.dead:
                        game.kill(mob_id)
                    for mob_id in game.despawn_queue:
                        game.despawn(mob_id)
                    player()
                    if player.hp<=0:
                        running=False
                    display()
                if keys[pg.K_p]:
                    print(player.xp)
                game.event_cache=[]
                game.time+=1
                if game.level==11:
                    dark_orb.name='Dark Orb'
                if player.armor>=50 and not player.can_guard:
                    player.evolve()
    pg.mixer.music.stop()
    display_score()

def display_score():
    screen.fill((0,60,50))
    font_medium=pg.font.SysFont('Noto Sans',70,True)
    font_large=pg.font.SysFont('Noto Sans',100,True)
    font_small=pg.font.SysFont('Noto Sans',45,True)
    score=font_large.render(str(player.xp/100)+'%',True,(255,255,255))
    location=score.get_rect(center=(960,540))
    screen.blit(score,location)
    name=font_medium.render(player.name,True,(255,255,255))
    location=name.get_rect(center=(960,480))
    screen.blit(name,location)
    if game.win:
        level=font_small.render('Victory!',True,(255,255,255))
    else:
        level=font_small.render(f'Level {str(game.level)}',True,(255,255,255))
    location=level.get_rect(center=(960,600))
    screen.blit(level,location)
    pg.display.flip()
    running=True
    pg.time.delay(500)
    while running:
        for event in pg.event.get():
            if event.type==pg.QUIT:
                running=False
        keys=pg.key.get_pressed()
        if (keys[pg.K_LCTRL] and keys[pg.K_q]) or keys[pg.K_RETURN] or keys[pg.K_ESCAPE]:
            running=False

def debug_mode():
    box=text_box((460,524),(1000,32),'Input prompt',selected_by_default=True)
    running=True
    pg.time.delay(250)
    while running:
        display(False)
        box.draw()
        pg.display.flip()
        game.events=pg.event.get()
        keys=pg.key.get_pressed()
        for event in game.events:
            if event.type==pg.QUIT:
                running=False
                return
        text=box()
        if text!=None:
            try:
                exec(text)
            except:
                print(text)
            return
        if keys[pg.K_ESCAPE]:
            return