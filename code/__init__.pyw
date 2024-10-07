print('\033c', end='')
from game_logic import *
quit_game=start()
if not quit_game:
    loop()
    print(game.level)
    print(player.xp)
pg.quit()