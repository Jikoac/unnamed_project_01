'''An example mod'''
try:
    from other import *
except:
    try:
        from mobs import *
    except:
        try:
            from loot_tables import *
        except:
            try:
                from items import *
            except:
                None
        try:
            from projectiles import *
        except:
            try:
                from ai import *
            except:
                None
