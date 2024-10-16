from base import *

data_ranges={'format':(0,8),'max_hp':(8,16),'hp':(16,24),
            'damage':(24,32),'xp':(32,96),'x':(96,128),
            'y':(128,144),'speed':(144,160),'xp_boost':(160,168),
            'mob_count':(168,232),'armor':(232,240),'jump_height':(240,248),
            'range':(248,256)
            }
data_keys={'can_shield':280,'debug':281,'photo':282,'photo_mode':283}

def binary_data():
    data=bitset(284)
    data[range]=data_ranges
    data[map]=data_keys
    data['format']='00000000'
    data['max_hp']=binary(player.max_hp)
    data['hp']=binary(player.hp)
    data['damage']=binary(player.damage)
    data['xp']=binary(player.xp,64)
    data['x']=binary(round(player.x),32)
    data['y']=binary(round(player.y),16)
    data['speed']=binary(round(player.speed*20),16)
    data['xp_boost']=binary(round(player.xp_boost*20))
    data['mob_count']=binary(game.mob_count,64)
#    data['armor']=binary(player.armor)
    data['jump_height']=binary(player.jump_height)
    data['range']=binary(player.range)
    return int(repr(data), 2).to_bytes((len(repr(data)) + 7) // 8, byteorder='big')

def save_data(name:str):
    os.makedirs(path.data+name,exist_ok=True)
    data_path=path.data_path(name)
    with open(data_path.stat,'wb') as file:
        file.write(binary_data())
        file.close()
    with open(data_path.name,'w') as file:
        file.write(player.name)
        file.close()

def load_data(name:str):
    data_path=path.data_path(name)
    return

save_data('test')