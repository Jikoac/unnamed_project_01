print('\033c', end='')
from game_logic import *
quit_game=start()
if not quit_game:
    if select_load_data():
        activate_mods(True)
    else:
        activate_mods()
    from mod_imports import *
    generators+=mod_generators
    upgrades+=mod_upgrades
    import spawn_data
    generators+=spawn_data.generators
    import upgrade_data
    upgrades+=upgrade_data.upgrades
    loop()
    print(game.level)
    print(player.xp)
pg.quit()