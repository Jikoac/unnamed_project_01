from mod_import_config import *

data_ranges={'format':(0,8),'max_hp':(8,16),'hp':(16,24),
            'damage':(24,32),'xp':(32,96),'x':(96,128),
            'y':(128,144),'speed':(144,160),'xp_boost':(160,168),
            'mob_count':(168,232),'armor':(232,240),'jump_height':(240,248),
            'range':(248,256),'reflection':(256,264),'strike':(264,280),
            'time':(284,348)
            }
data_keys={'can_shield':280,'debug':281,'photo':282,'photo_mode':283,'pos_x':348,'facing':349}

def binary_data():
    data=bitset(350)
    data[range]=data_ranges
    data[map]=data_keys
    data['format']='00000000'
    data['max_hp']=binary(player.max_hp)
    data['hp']=binary(player.hp)
    data['damage']=binary(player.damage)
    data['xp']=binary(player.xp,64)
    data['x']=binary(round(abs(player.x)),32)
    data['y']=binary(round(player.y),16)
    data['speed']=binary(round(player.speed*20),16)
    data['xp_boost']=binary(round(player.xp_boost*20))
    data['mob_count']=binary(game.mob_count,64)
    data['armor']=binary(player.armor)
    data['jump_height']=binary(player.jump_height)
    data['range']=binary(player.range)
    data['reflection']=binary(player.reflection)
    data['strike']=binary(round(player.attack.speed*2),16)
    data['can_shield']=player.can_shield
    data['debug']=game.mode.debug
    data['photo']=game.mode.photo
    data['photo_mode']=game.photo_mode
    data['time']=binary(game.time,64)
    data['pos_x']=is_positive(player.x)
    data['facing']=1 if player.facing=='right' else 0
    return int(repr(data), 2).to_bytes((len(repr(data)) + 7) // 8, byteorder='big')

def extract_from_binary(data:bitset):
    format_version=int(data['format'])
    if not format_version:
        player.max_hp=data.number('max_hp')
        player.hp=data.number('hp')
        player.damage=data.number('damage')
        player.xp=data.number('xp')
        if data['pos_x']:
            player.x=data.number('x')
        else:
            player.x=-data.number('x')
        player.y=data.number('y')
        player.speed=data.number('speed')/20
        player.xp_boost=data.number('xp_boost')/20
        game.mob_count=data.number('mob_count')
        player.armor=data.number('armor')
        player.jump_height=data.number('jump_height')
        player.range=data.number('range')
        player.reflection=data.number('reflection')
        player.attack.speed=data.number('strike')/2
        player.can_shield=data['can_shield']
        game.mode.debug=data['debug']
        game.mode.photo=data['photo']
        game.photo_mode=data['photo_mode']
        game.time=data.number('time')
        player.facing='right' if data['facing'] else 'left'
    return

def save_data(name:str):
    os.makedirs(path.data+name,exist_ok=True)
    data_path=path.data_path(name)
    with open(data_path.stat,'wb') as file:
        file.write(binary_data())
        file.close()
    with open(data_path.name,'w') as file:
        if player.name:
            file.write(player.name)
        else:
            file.write(os.getlogin())
        file.close()
    with open(data_path.loot,'w') as file:
        file.write(f'player.loot={player.loot}')
        file.close()
    with open(data_path.upgrade,'w') as file:
        file.write(f'{dict(zip(map(lambda x:x.id,upgrades),map(lambda x:x.max,upgrades)))}')
        file.close()
    with open(data_path.mob,'w') as file:
        file.write('\n'.join([format(mob,'data') for mob in game.mobs.values()]))
        file.close()

def load_data(name:str):
    data_path=path.data_path(name)
    with open(data_path.stat,'rb') as file:
        data=bitset.from_bytes(file.read())
        data[range]=data_ranges
        data[map]=data_keys
        if data.number('hp'):
            extract_from_binary(data)
        file.close()
    if data.number('hp'):
        with open(data_path.name,'r') as file:
            if not player.name:
                player.name=file.read()
            file.close()
        with open(data_path.loot,'r') as file:
            exec(file.read())
            file.close()
        with open(data_path.upgrade,'r') as file:
            upgrade_uses=eval(file.read())
            for upgrade in upgrades:
                if upgrade.id in upgrade_uses:
                    upgrade.max=upgrade_uses[upgrade.id]
            file.close()
        with open(data_path.mob,'r') as file:
            for line in file:
                line_data=eval(line)
                game.summon(*line_data)
            file.close()
    return