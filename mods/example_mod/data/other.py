try:
    from mobs import *
except:
    from main import *
player.xp=10000
player.hp=1000
player.max_hp=1000
player.damage=15
player.can_shield=True
player.knockback=5
player.attack.speed=15
player.speed*=1.5
player.range*=10
player.power=2
player.jump_height*=2
pg.mixer.music.load("C:/Users/Public/Music/Griffin Armageddon/Zapolemos Quest (Deluxe Edition)/1/A Saga Begins.mp3")
game.music=True