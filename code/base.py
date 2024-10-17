import pygame as pg
import os
from random import *
import inspect
import types
import sys

pg.init()
pg.mixer.init()
screen=pg.display.set_mode((1920,1080),pg.FULLSCREEN|pg.DOUBLEBUF|pg.HWSURFACE)

def flip_mask(mask:pg.mask.Mask):
    flipped_mask = pg.mask.Mask((mask.get_size()))
    for x in range(mask.get_size()[0]):
        for y in range(mask.get_size()[1]):
            if mask.get_at((x, y)):
                flipped_mask.set_at((mask.get_size()[0] - 1 - x, y), 1)
    return flipped_mask

class path:
    class subpath:
        def __init__(self,path,extension:str='.py'):
            self.direct=path
            self.extension=extension
        def __call__(self,file):
            return self.direct+'/'+file+self.extension
        def __str__(self):
            return self.direct
        def __add__(self,other):
            return self.direct+'/'+other
    def __init__(self):
        path = os.path.abspath(__file__)
        self.main=self.subpath(path.replace('\\','/').replace('/code/base.py',''))
        self.asset=self.subpath(self.main+'assets','')
        self.code=self.subpath(self.main+'code')
        self.texture=self.subpath(self.asset+'textures','.png')
        self.sound=self.subpath(self.asset+'sounds','.mp3')
        self.mod=self.subpath(self.main+'mods','.py')
        self.data=self.subpath(self.main+'data','')
    def __call__(self,file):
        return self.main+'/'+file
    class mod_path(subpath):
        def __init__(self,name):
            self.main=path.subpath(name)
            self.asset=path.subpath(self.main+'assets')
            self.texture=path.subpath(self.asset+'textures','.png')
            self.sound=path.subpath(self.asset+'sounds','.mp3')
            self.code=path.subpath(self.main+'data')
            self.direct=str(self.main)
            self.primary=path.subpath(self.direct,'')
            self.extension='.py'
    class data_path(subpath):
        def __init__(self,name):
            self.main=path.subpath(path.data+name,'')
            self.stat=self.main+'stats'
            self.mob=self.main+'mobs'
            self.upgrade=self.main+'upgrades'
            self.mod=self.main+'mods'
            self.name=self.main+'name'
            self.loot=self.main+'loot'
            self.direct=str(self.main)
            self.extension=''
    def __add__(self,other):
        return self.main+'/'+other

path=path()

class game_player:
    class player_shield:
        def __init__(self):
            self.x=0
            self.y=0
            self.textures={
                'right':pg.image.load(path.texture('shield')),
                'left':pg.transform.flip(pg.image.load(path.texture('shield')),True,False)
                }
            self.texture=self.textures['right']
            self.shape=pg.mask.from_surface(pg.image.load(path.texture('shield')))
            self.shapes={
                'right':self.shape,
                'left':flip_mask(self.shape)
            }
            self.width,self.height=self.shape.get_size()
            self.facing='right'
            self.active=False
            self.sound=pg.mixer.Sound(path.sound('shield'))
        def __call__(self):
            self.facing=player.facing
            self.texture=self.textures[self.facing]
            self.shape=self.shapes[self.facing]
            self.y=player.y
            if self.facing=='left':
                self.x=player.x-self.width
            else:
                self.x=player.x+player.width
            if not self.active:
                pg.mixer.Sound.play(self.sound)
                self.active=True

    class slash_attack:
        def __init__(self):
            self.x=0
            self.y=0
            self.textures={
                'right':pg.image.load(path.texture('attack')),
                'left':pg.transform.flip(pg.image.load(path.texture('attack')),True,False)
                }
            self.texture=self.textures['right']
            self.shape=pg.mask.from_surface(pg.image.load(path.texture('attack')))
            self.shapes={
                'right':self.shape,
                'left':flip_mask(self.shape)
            }
            self.width,self.height=self.shape.get_size()
            self.facing='right'
            self.power=0
            self.sound=pg.mixer.Sound(path.sound('slash'))
            self.speed=10
        def __call__(self):
            self.facing=player.facing
            self.texture=self.textures[self.facing]
            self.shape=self.shapes[self.facing]
            self.y=player.y
            self.power=player.power
            pg.mixer.Sound.play(self.sound)

    class player_control:
            def __init__(self):
                self.jump=0
                self.move='none'
                self.attack=0
                self.hold_attack=False
                self.shield=False
                self.select=False
                self.select_held=False
            def __call__(self):
                keys=pg.key.get_pressed()
                if keys[pg.K_d]:
                    self.move='right'
                elif keys[pg.K_a]:
                    self.move='left'
                else:
                    self.move='none'
                if keys[pg.K_w] and player.y==0:
                    self.jump=player.jump_height
                    pg.mixer.Sound.play(player.jump_sound)
                if keys[pg.K_SPACE] and not keys[pg.K_s]:
                    if not self.hold_attack:
                        self.attack=player.range
                        self.hold_attack=True
                else:
                    self.hold_attack=False
                if keys[pg.K_s]:
                    self.shield=True
                else:
                    self.shield=False
            def get_select(self):
                self.select=False
                keys=pg.key.get_pressed()
                if keys[pg.K_SPACE] or keys[pg.K_RETURN]:
                    if not self.select_held:
                        self.select=True
                        self.select_held=True
                else:
                    self.select_held=False
            def move_mouse(self):
                keys=pg.key.get_pressed()
                if keys[pg.K_UP] or keys[pg.K_w]:
                    pg.mouse.set_pos(add(pg.mouse.get_pos(),(0,-5)))
                if keys[pg.K_LEFT] or keys[pg.K_a]:
                    pg.mouse.set_pos(add(pg.mouse.get_pos(),(-5,0)))
                if keys[pg.K_DOWN] or keys[pg.K_s]:
                    pg.mouse.set_pos(add(pg.mouse.get_pos(),(0,5)))
                if keys[pg.K_RIGHT] or keys[pg.K_d]:
                    pg.mouse.set_pos(add(pg.mouse.get_pos(),(5,0)))

    def __init__(self,name:str='Player'):
        self.x=0
        self.y=0
        self.name=name
        self.loot={}
        self.xp=0
        self.max_hp=10
        self.hp=10
        self.damage=1
        self.speed=2
        self.range=25
        self.texture_main=pg.image.load(path.texture('man'))
        self.shape_main=pg.mask.from_surface(pg.image.load(path.texture('mannequin')))
        self.texture_flipped=pg.transform.flip(self.texture_main,True,False)
        self.shape_flipped=flip_mask(self.shape_main)
        self.facing='right'
        self.textures={
            'right':self.texture_main,
            'left':self.texture_flipped
        }
        self.shapes={
            'right':self.shape_main,
            'left':self.shape_flipped
        }
        self.texture=self.textures['right']
        self.shape=self.shapes['right']
        self.width,self.height=self.shape_main.get_size()
        self.control=self.player_control()
        self.attack=self.slash_attack()
        self.can_shield=False
        self.xp_boost=1
        self.power=1
        self.jump_height=50
        self.shield=self.player_shield()
        self.knockback=1
        self.jump_sound=pg.mixer.Sound(path.sound('jump'))
    def __call__(self):
        self.control()
        if self.control.jump>0:
            self.y+=4.5
            self.control.jump-=1
        else:
            self.y=max(self.y-3,0)
        if self.control.move=='left':
            self.facing='left'
            self.x-=self.speed
            if self.y>50:
                self.x-=self.speed/10
        elif self.control.move=='right':
            self.facing='right'
            self.x+=self.speed
            if self.y>50:
                self.x+=self.speed/10
        self.texture=self.textures[self.facing]
        self.shape=self.shapes[self.facing]
        if self.control.attack:
            if self.control.attack==self.range:
                if self.facing=='right':
                    self.attack.x=self.x+self.width
                if self.facing=='left':
                    self.attack.x=self.x-self.attack.width
                self.attack()
            else:
                if self.attack.facing=='right':
                    self.attack.x+=self.attack.speed
                elif self.attack.facing=='left':
                    self.attack.x-=self.attack.speed*0.996
            self.control.attack=max(self.control.attack-1,0)
        if self.control.shield:
            self.shield()
        else:
            self.shield.active=False
player=game_player()

class between:
    def __init__(self,number,other_number=None):
        try:
            self.range=(number[0],number[1])
        except:
            self.range=number,other_number
        def __eq__(self,other):
            if isinstance(other,between):
                if max(other.range)>=min(self.range) and max(other.range)<=max(self.range):
                    return True
                elif min(other.range)>=min(self.range) and min(other.range)<=max(self.range):
                    return True
                else:
                    return False
            else:
                if other>=min(self.range) and other<=max(self.range):
                    return True
                else:
                    return False

class in_rect:
    def __init__(self,rect):
        self.x,self.y=rect.topleft
        self.width,self.height=rect.size
    def __eq__(self,point):
        if point[0]>=self.x and point[0]<=self.x+self.width and point[1]>=self.y and point[1]<=self.y+self.height:
            return True
        return False


class key:
    def __init__(self,key:int=pg.K_ESCAPE):
        self.key=key
        self.click=False
        self.clicked=False
    def __call__(self):
        keys=pg.key.get_pressed()
        self.click=False
        if keys[self.key]:
            if not self.clicked:
                self.click=True
                self.clicked=True
        else:
            self.clicked=False
        return self.click

class mouse_click:
    def __init__(self,key:int=1):
        self.key=key
        self.click=False
        self.clicked=False
        self.pos=(0,0)
    def __call__(self):
        pressed=False
        self.click=False
        for event in game.events:
            if event.type==pg.MOUSEBUTTONDOWN:
                if event.button==self.key:
                    if not self.clicked:
                        self.click=True
                        self.clicked=True
                        self.pos=event.pos
                        self.x,self.y=self.pos
                    pressed=True
            if not pressed:
                self.clicked=False
        return self.click

class test_mouse_click:
    def __init__(self, button=1):
        self._click = False
        self.button = button
        self.pos=(0,0)

    @property
    def click(self):
        return self._click

    def __call__(self):
        for event in game.events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == self.button:
                self._click = True
                self.pos=event.pos
                self.x,self.y=self.pos
                break
        else:
            self._click = False

class game_class:
    keys={
        'l_mouse':test_mouse_click(),
        'esc':key(),
        'pause':key(pg.K_PAUSE)
    }
    events=[]
    scroll=0
    scroll_items=0
    dead=[]
    mobs={}
    mob_count=0
    time=0
    level=0
    win=False
    levels={
        0:0,
        1:1,
        2:10,
        3:25,
        4:50,
        5:100,
        6:250,
        7:500,
        8:1000,
        9:2500,
        10:5000,
        11:10000,
        12:15000,
        13:20000,
        14:25000,
        15:30000,
        15:35000,
        17:40000,
        18:50000,
        19:60000,
        20:80000,
        21:100000,
        22:150000
    }
    event_cache=[]
    #screen=screen
    def spawn(self,mob,x,y,facing='right'):
        number='0'*(8-len(hex(self.mob_count)))+hex(self.mob_count).replace('0x','')
        self.mobs.update({number:mob_instance(mob,x,y,number,facing)})
        self.mob_count+=1
    def kill(self,mob_id):
        self.mobs[mob_id].give_loot()
        player.xp+=self.mobs[mob_id].xp
        self.mobs.pop(mob_id)
    def despawn(self,mob_id):
        self.mobs.pop(mob_id)
    def level_up(self):
        if player.xp<150000:
            for lvl in self.levels.keys():
                if player.xp>=self.levels[lvl] and player.xp<self.levels[lvl+1]:
                    game.level=lvl
        else:
            self.win=True
            self.level=11
    def get_clicked(self):
        for key in self.keys.values():
            key()
    def summon(self,mob,x,y,facing,id,hp):
        self.mobs.update({id:mob_instance(mob,x,y,id,facing)})
        self.mobs[id].health=hp


game=game_class()

class mob:
    def __init__(self,
            ai:str='no_ai',
            loot:str='no_loot',
            texture:str='mannequin',
            shape:str='default',
            health:int=0,
            texture_offset:tuple=(0,0),
            ranged:dict={
                'projectile':'None',
                'fire_rate':0,
                'offset':(0,0),
                'sound':'none'
            },
            mob_type:str='none',
            death_sound:str='none',
            xp:int=1,
            damage:int=1
    ):
        current_frame = inspect.currentframe()
        caller_frame = inspect.getouterframes(current_frame, 2)
        caller_filepath = caller_frame[1].filename
        self.filepath = os.path.abspath(caller_filepath)
        self.module=path.mod_path(self.filepath.replace('\\','/').replace(f'/data/{os.path.basename(self.filepath)}',''))
        self.special_ai=False
        try:
            self.__dict__.update(eval(ai).__dict__)
        except:
            self.__dict__.update(ai.__dict__)
        try:
            self.loot=eval(loot)
        except:
            self.loot=loot
        try:
            self.texture_main=pg.image.load(self.module.texture(texture))
        except:
            try:
                self.texture_main=pg.image.load(path.texture(texture))
            except:
                self.texture_main=error_texture
        if shape=='default':
            try:
                self.shape_main=pg.mask.from_surface(pg.image.load(self.module.texture(texture)))
            except:
                self.shape_main=pg.mask.from_surface(pg.image.load(path.texture(texture)))
        else:
            try:
                self.shape_main=pg.mask.from_surface(pg.image.load(self.module.texture(shape)))
            except:
                try:
                    self.shape_main=pg.mask.from_surface(pg.image.load(path.texture(shape)))
                except:
                    self.shape_main=pg.mask.from_surface(error_texture)
        self.health=health
        self.texture_offset=texture_offset
        ranged_data={
            'projectile':'None',
            'fire_rate':1,
            'offset':(0,0),
            'sound':'none'
            }
        ranged_data.update(ranged)
        try:
            self.projectile=eval(ranged_data['projectile'])
        except:
            self.projectile=ranged_data['projectile']
        self.fire_rate=ranged_data['fire_rate']
        self.projectile_offset=ranged_data['offset']
        self.type=mob_type
        try:
            self.death_sound=pg.mixer.Sound(self.module.sound(death_sound))
        except:
            self.death_sound=pg.mixer.Sound(path.sound(death_sound))
        try:
            self.shoot_sound=pg.mixer.Sound(self.module.sound(ranged_data['sound']))
        except:
            self.shoot_sound=pg.mixer.Sound(path.sound(ranged_data['sound']))
        self.width,self.height=self.shape_main.get_size()
        self.xp=xp
        self.texture_flipped=pg.transform.flip(self.texture_main,True,False)
        self.shape_flipped=flip_mask(self.shape_main)
        self.textures={
            'right':self.texture_main,
            'left':self.texture_flipped
        }
        self.shapes={
            'right':self.shape_main,
            'left':self.shape_flipped
        }
        self.texture=self.textures['right']
        self.shape=self.shapes['right']
        self.damage=damage

class loot_table:
    class item:
        def __init__(self,item,chance):
            self.item=item
            self.chance=chance
            self.loot=[item]*chance
    def __init__(self,
                items:dict={'void':0},
                drops:int=1,
                limited_items:bool=False
        ):
        self.items=[self.item(item,items[item]) for item in items]
        self.drops=drops
        self.limited_items=limited_items
    def __call__(self,drops:int=0):
        if drops==0:drops=self.drops
        items=[]
        loot=[]
        for item in self.items:
            items+=item.loot
        try:
            for i in range(drops):
                drop=items.pop(randrange(len(items)))
                if drop!='void':
                    loot.append(drop)
                if not self.limited_items:
                    items.append(drop)
        except:
            for i in range(len(items)):
                drop=items.pop(randrange(len(items)))
                if drop!='void':
                    loot.append(drop)
                if not self.limited_items:
                    items.append(drop)
        return loot

class ai:
    def __init__(self,
                is_hostile:bool=False,
                min_distance:int=0,
                max_distance:int=960,
                speed:float=0.1,
                flee:bool=False,
                behavior:str='idle'
        ):
        self.is_hostile=is_hostile
        self.min_distance=min_distance
        self.max_distance=max_distance
        self.speed=speed
        self.flee=flee
        self.behavior=behavior

class ai_line:
    def __init__(self,
                speed:float=1,
                is_hostile:bool=False
        ):
        self.speed=speed
        self.special_ai='straight_line'
        self.is_hostile=is_hostile

class projectile:
    def __init__(self,
            ai:str='ai_line(2)',
            loot:str='no_loot',
            texture:str='mannequin',
            shape:str='default',
            health:int=0,
            texture_offset:tuple=(0,0),
            mob_type:str='none',
            death_sound:str='none',
            damage:int=1
    ):
        current_frame = inspect.currentframe()
        caller_frame = inspect.getouterframes(current_frame, 2)
        caller_filepath = caller_frame[1].filename
        self.filepath = os.path.abspath(caller_filepath)
        self.module=path.mod_path(self.filepath.replace('\\','/').replace(f'/data/{os.path.basename(self.filepath)}',''))
        self.special_ai=False
        try:
            self.__dict__.update(eval(ai).__dict__)
        except:
            self.__dict__.update(ai.__dict__)
        try:
            self.loot=eval(loot)
        except:
            self.loot=loot
        try:
            self.texture_main=pg.image.load(self.module.texture(texture))
        except:
            try:
                self.texture_main=pg.image.load(path.texture(texture))
            except:
                self.texture_main=error_texture
        if shape=='default':
            try:
                self.shape_main=pg.mask.from_surface(pg.image.load(self.module.texture(texture)))
            except:
                self.shape_main=pg.mask.from_surface(pg.image.load(path.texture(texture)))
        else:
            try:
                self.shape_main=pg.mask.from_surface(pg.image.load(self.module.texture(shape)))
            except:
                try:
                    self.shape_main=pg.mask.from_surface(pg.image.load(path.texture(shape)))
                except:
                    self.shape_main=pg.mask.from_surface(error_texture)
        self.health=health
        self.texture_offset=texture_offset
        ranged_data={
            'projectile':'None',
            'fire_rate':1,
            'offset':(0,0),
            'sound':'none'
            }
        try:
            self.projectile=eval(ranged_data['projectile'])
        except:
            self.projectile=ranged_data['projectile']
        self.fire_rate=ranged_data['fire_rate']
        self.projectile_offset=ranged_data['offset']
        self.type=mob_type
        try:
            self.death_sound=pg.mixer.Sound(self.module.sound(death_sound))
        except:
            self.death_sound=pg.mixer.Sound(path.sound(death_sound))
        self.width,self.height=self.shape_main.get_size()
        self.xp=0
        self.texture_flipped=pg.transform.flip(self.texture_main,True,False)
        self.shape_flipped=flip_mask(self.shape_main)
        self.textures={
            'right':self.texture_main,
            'left':self.texture_flipped
        }
        self.shapes={
            'right':self.shape_main,
            'left':self.shape_flipped
        }
        self.texture=self.textures['right']
        self.shape=self.shapes['right']
        self.damage=damage

class item:
    def __init__(self,
        item_id:str='no_id',
        texture:str='none',
        name:str=None
    ):
        current_frame = inspect.currentframe()
        caller_frame = inspect.getouterframes(current_frame, 2)
        caller_filepath = caller_frame[1].filename
        self.filepath = os.path.abspath(caller_filepath)
        self.module=path.mod_path(self.filepath.replace('\\','/').replace(f'/data/{os.path.basename(self.filepath)}',''))
        
        try:
            self.texture=pg.image.load(self.module.texture(texture))
        except:
            try:
                self.texture=pg.image.load(path.texture(texture))
            except:
                self.texture=error_texture
        self.id=item_id
        if name==None:
            self.name=self.id
        else:
            self.name=name

class mob_instance(mob):
    def __call__(self):
        return
    def __init__(self,data:mob,x:float,y:float,mob_id:str='000000',facing:str='right'):
        self.__dict__.update(data.__dict__)
        self.x=x
        self.y=y
        self.spawned=game.time
        self.id=mob_id
        self.max_health=self.health
        self.facing=facing
        self.cooldown=0
    def shoot(self):
        if self.fire_rate:
            if (game.time%(100//self.fire_rate))==(self.spawned%(100//self.fire_rate)) and game.time>self.spawned:
                game.spawn(projectile,self.x+(self.width/2)-(projectile.width/2)+self.projectile_offset[0],self.y+(self.height/2)-(projectile.height/2)+self.projectile_offset[1],self.facing)
                pg.mixer.Sound.play(self.shoot_sound)
    def collide(self, other):
        offset_x = other.x - self.x
        offset_y = -(other.y+other.height) - -(self.y+self.height)
        return self.shape.overlap(other.shape, (offset_x, offset_y))
    def give_loot(self):
        for i in self.loot():
            try:
                player.loot[i]+=1
            except:
                player.loot.update({i:1})
    def __call__(self):
        if not self.special_ai:
            if self.x>player.x and self.x<player.x+self.min_distance:
                self.x+=self.speed
                self.facing='right'
            elif self.x<player.x and self.x>player.x-self.min_distance:
                self.x-=self.speed
                self.facing='left'
            elif self.x<player.x-self.max_distance:
                self.x+=self.speed
                self.facing='right'
            elif self.x>player.x+self.max_distance:
                self.x-=self.speed
                self.facing='left'
            elif self.x>player.x:
                self.facing='left'
            else:
                self.facing='right'
        elif self.special_ai=='straight_line':
            if self.facing=='right':
                self.x+=self.speed
            else:
                self.x-=self.speed
        elif self.special_ai=='custom':
            self.ai
        self.texture=self.textures[self.facing]
        self.shape=self.shapes[self.facing]
        self.shoot()
    def is_dead(self):
        if self.health<=0 and self.max_health:
            return True
        return False
    def __format__(self,format_spec):
        if format_spec=='data':
            return f'({self.type},{self.x},{self.y},"{self.facing}","{self.id}",{self.health})'
class spawn_rule:
    def __init__(self,
            chance:float=1,
            min_level:int=0,
            max_level:int=None,
            mob:mob=None,
            min_distance:int=0,
            max_distance:int=960,
            spawn_height:int=0
    ):
        self.chance=chance
        self.min_level=min_level
        self.max_level=max_level
        self.mob=mob
        self.min_distance=min_distance
        self.max_distance=max_distance
        self.spawn_height=spawn_height
    def __call__(self):
        spawn=False
        if game.level>=self.min_level:
            try:
                if game.level<=self.max_level:
                    if not randrange(round(1000/self.chance)):
                        spawn=True
            except:
                if not randrange(round(1000/self.chance)):
                    spawn=True
        if spawn:
            if randrange(2):
                game.spawn(self.mob,player.x+player.width//2+randint(self.min_distance,self.max_distance),self.spawn_height)
            else:
                game.spawn(self.mob,player.x+player.width//2-randint(self.min_distance,self.max_distance)-self.mob.width,self.spawn_height)

def heal_upgrade(power:int=1):
    def wrapper():
        player.hp=min(player.hp+power,player.max_hp)
    return wrapper
def max_hp_upgrade(power:int=1):
    def wrapper():
        player.max_hp+=power
    return wrapper
def damage_upgrade(power:int=1):
    def wrapper():
        player.damage+=power
    return wrapper
def range_upgrade(power:int=1):
    def wrapper():
        player.range+=power
    return wrapper
def speed_upgrade(power:int=1):
    def wrapper():
        player.speed+=power
    return wrapper
def power_upgrade(power:int=1):
    def wrapper():
        player.power+=power
    return wrapper
def xp_upgrade(power:int=1):
    def wrapper():
        player.xp_boost+=power
    return wrapper
def jump_upgrade(power:int=1):
    def wrapper():
        player.jump_height+=power
    return wrapper
def knock_upgrade(power:int=1):
    def wrapper():
        player.knockback+=power
    return wrapper
def strike_upgrade(power:int=1):
    def wrapper():
        player.attack.speed+=power
    return wrapper
def multiple(*functions):
    def output():
        for f in functions:
            f()
    return output

class upgrade:
    def  __init__(self,
            items:dict={'bread':1},
            upgrade=heal_upgrade(1),
            upgrade_id:str='no_id',
            name:str='Upgrade',
            texture:str='none',
            level:int=1,
            max:int=-1,
            show_uses:bool=False,
            name_color=(255,255,255)
    ):
        current_frame = inspect.currentframe()
        caller_frame = inspect.getouterframes(current_frame, 2)
        caller_filepath = caller_frame[1].filename
        self.filepath = os.path.abspath(caller_filepath)
        self.module=path.mod_path(self.filepath.replace('\\','/').replace('/code/upgrades.py',''))
        self.max=max
        self.show_uses=show_uses

        try:
            self.texture=pg.image.load(self.module.texture(texture))
        except:
            try:
                self.texture=pg.image.load(path.texture(texture))
            except:
                self.texture=error_texture
        self.items=items
        self.upgrade=upgrade
        self.id=upgrade_id
        self.name=name
        self.level=level
        self.name_color=name_color
    def __call__(self):
        affordable=True
        for i in self.items:
            try:
                if player.loot[i]<self.items[i]:
                    affordable=False
            except:
                affordable=False
        if affordable:
            self.max-=1
            self.upgrade()
            for i in self.items:
                player.loot[i]-=self.items[i]
            return True
        return False

forward=ai_line
no_ai=ai(speed=0)
no_loot=loot_table(items={'air':0},drops=0)

none=pg.image.load(path.texture('none'))
background=pg.image.load(path.texture('background'))
ground=pg.image.load(path.texture('ground'))
error_texture=pg.image.load(path.texture('deny'))
heart=pg.image.load(path.texture('lil_heart'))

font=pg.font.SysFont('Noto Sans',25)

generators=[]
upgrades=[]

resize=pg.transform.scale

def add(x,y):
    return tuple([x[i]+y[i] for i in range(len(x))])

def binary(value:int|str=0,length:int=8):
    '''Convert a string or int to binary'''
    if isinstance(value,str):
        out=''
        for l in value:
            out+=f'{ord(l):0{length}b}'
        return out
    return f'{value:0{length}b}'

def total(x):
    '''Returns a range of the length of \'x\''''
    return(list(range(len(x))))

class bitset:
    '''A class for data stored in binary, 
the special keys are:
    any: any bit in the data, 
    all: all bits in the data, 
    int: the data as an integer, 
    len: the length of the data, 
    bin: the data as binary, 
    range: the range keywords, 
    map: the keywords, 
    color: the data as a color'''
    def __init__(self, length:int=8,*keys:str,**kwargs):
        self.data = 0
        self.length = length
        bit_range=range(length)
        self.keys=dict(zip(keys,bit_range))
        self.ranges:dict[str,tuple[int,int]]={}
        if 'ranges' in kwargs:
            self.ranges.update(kwargs['ranges'])
        if 'keys' in kwargs:
            self.keys.update(kwargs['keys'])
        self.from_str,self.from_bytes=self.new_methods()

    def __call__(self, length:int):
        if length < self.length:
            self.data = min(self.data,(2**length)-1)
        self.length = length

    def __getitem__(self, index:int):
        if type(index)==str:
            if index in self.ranges:
                index=self.ranges[index]
            elif index in self.keys:
                index=self.keys[index]
            else:
                raise KeyError(index)
        if isinstance(index,tuple):
            index=range(index[0],index[1])
        if index==any:
            return any(f'{self.data:0{self.length}b}')
        elif index==all:
            return all(f'{self.data:0{self.length}b}')
        elif index==int:
            return self.data
        elif index==len:
            return self.length
        elif index==bin:
            return repr(self)
        elif index==range:
            return self.ranges
        elif index==map:
            return self.keys
        elif isinstance(index,range):
            value=[]
            for i in index:
                value.append(str(int((self.data >> i) & 1 == 1)))
            value.reverse()
            return ''.join(value)
        elif index >= self.length:
            raise IndexError("Index out of range")
        else:
            return (self.data >> index) & 1 == 1

    def __setitem__(self, index:int|None, value:int):
        if type(index)==str:
            if index in self.ranges:
                index=self.ranges[index]
            elif index in self.keys:
                index=self.keys[index]
            else:
                raise KeyError(index)
        if isinstance(index,tuple):
            index=range(index[0],index[1])
        if index==any:
            index=randrange(self.length)
        if index==all:
            self.data=int('0b'+(str(int(value))*self.length),base=2)
        elif index==len:
            self(value)
        elif index==int:
            self.data=value
            self.length=max(self.length,len(repr(self)))
        elif index==bin:
            self.data=int(str(value),base=2)
            self.length=max(self.length,len(repr(self)))
        elif index==range:
            self.ranges=value
        elif index==map:
            self.keys=value
        elif isinstance(index,range):
            if max(index) >= self.length:
                raise IndexError("Index out of range")
            value=str(value)
            for i in index:
                if int(value[len(index)-1-(i-min(index))]):
                    self.data |= (1 << i)
                else:
                    self.data &= ~(1 << i)
        else:
            if index >= self.length:
                raise IndexError("Index out of range")
            if value:
                self.data |= (1 << index)
            else:
                self.data &= ~(1 << index)

    def __repr__(self):
        return f'{self.data:0{self.length}b}'
    
    def toggle(self,index:str|int=0):
        self[index]= not self[index]

    def number(self,index:range):
        if isinstance(index,str):
            index=self.ranges[index]
        if isinstance(index,tuple):
            index=range(index[0],index[1])
        value=[]
        for i in index:
            value.append(str(int((self.data >> i) & 1 == 1)))
        value.reverse()
        value=''.join(value)
        return int(value,base=2)
    
    def ascii(self,index:int=0,utf:int=8):
        return chr(self.number(range(index,index+utf)))

    def assign_character(self,value='a',index:int=0):
        for i in total(binary(value)):
            self[index+i]=bool(int(binary(value)[len(binary(value))-1-i]))

    def bytes(self):
        return int(repr(self.data), 2).to_bytes((len(repr(self.data)) + 7) // 8, byteorder='big')
    
    def from_bytes(bytes:bytes=int(0).to_bytes()):
        self=bitset(len(bytes)*8)
        self.data=int.from_bytes(bytes)
        self.adjust()
        return self

    def str(self,utf:int=8):
        string=''
        for i in range(0,self.length,utf):
            string+=self.ascii(i,utf)
        return string
    
    def from_str(string:str='',utf:int=8):
        self=bitset(len(string)*utf)
        for i in range(len(string)):
            self.assign_character(string[i],i*utf)
        self.adjust()
        return self
    
    def adjust(self,can_extend:bool=True,can_shorten:bool=False):
        if can_extend:
            self.length=max(self.length,len(repr(self.data)))
        if can_shorten:
            self.length=min(self.length,len(repr(self.data)))

    def new_methods(self):
        def str_method(string:str,utf:int=8):
            data=bitset(len(string)*utf)
            for i in range(len(string)):
                data.assign_character(string[i],i*utf)
            self.adjust()
            self.data=data.data
        def bytes_method(bytes:bytes):
            data=bitset(len(bytes)*8)
            data.data=int.from_bytes(bytes)
            self.data=data.data
            self.adjust()
        return str_method,bytes_method

def is_positive(number:int|float):
    if number>=0:
        return True
    return False