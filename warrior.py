#Defines warriors


from typing import Union
class Warrior:
    def __init__(self) -> None:
        self.weapons: dict[str, list[dict[str, Union[str, int]]]] = {'Knight': [{'name': 'Long Sword', 'value': 7},
            {'name': 'Light Shield', 'value': 6},
            {'name': 'Dagger', 'value': 5},
            {'name': 'Chain mail', 'value': 6},
            {'name': 'Saint George’s blade', 'value': 10},
            {'name': 'Sir William Wallace’s boots', 'value': 8},
            {'name': 'Mighty Mace', 'value': 7},
            {'name': 'Double-edged blade', 'value': 8},
            {'name': 'Sir Michael’s axe', 'value': 8},
            {'name': 'Adam’s blade', 'value': 9},
            {'name': 'King Arthur’s helm', 'value': 5},
            {'name': 'Knight’s Crossbow', 'value': 6}],
 'Maratha': [{'name': 'Tega', 'value': 7},
             {'name': 'Maratha Sword', 'value': 6},
             {'name': 'Tiger’s claws', 'value': 8},
             {'name': 'Mughal’s blade', 'value': 7},
             {'name': 'Rajput Long Sword', 'value': 8},
             {'name': 'Nayar’s double blade', 'value': 7},
             {'name': 'Royal silver sword', 'value': 6},
             {'name': 'Ankush', 'value': 10},
             {'name': 'Katar', 'value': 5},
             {'name': 'Flex Sword', 'value': 8},
             {'name': 'Indian Axe', 'value': 9},
             {'name': 'Maharaja’s Helm', 'value': 6}],
 'Samurai': [{'name': 'Chokutō', 'value': 5},
             {'name': 'Kunai', 'value': 7},
             {'name': 'Katana', 'value': 7},
             {'name': 'Shinogi-Zukuri', 'value': 9},
             {'name': 'Shobu-Zukuri', 'value': 8},
             {'name': 'Kissaki-Moroha-Zukuri', 'value': 8},
             {'name': 'Kodachi', 'value': 6},
             {'name': 'Odachi', 'value': 6},
             {'name': 'Tachi', 'value': 7},
             {'name': 'Shinogi', 'value': 8},
             {'name': 'Shuriken', 'value': 5},
             {'name': 'Ishida Mitsunari Armour', 'value': 10},
             {'name': 'Onimaru Kunitsuna', 'value': 6}],
 'Viking': [{'name': 'Viking Axe', 'value': 5},
            {'name': 'Varin’s axe', 'value': 7},
            {'name': 'Loki’s Knife', 'value': 7},
            {'name': 'Thor’s hammer', 'value': 8},
            {'name': 'Thor’s Helm', 'value': 5},
            {'name': 'Stormbreaker', 'value': 9},
            {'name': 'Odin’s staff', 'value': 10},
            {'name': 'Freya’s Wings', 'value': 8},
            {'name': 'Baldur’s Blade', 'value': 6},
            {'name': 'Heimdall’s sword', 'value': 8},
            {'name': 'Valkyrie’s blade', 'value': 6},
            {'name': 'Tyr’s Helm', 'value': 6},
            {'name': 'Valkiri helm', 'value': 7}]}

    def getWeapons(self, warrior_name):
        return self.weapons[warrior_name]
class Viking(Warrior):
    def __init__(self) -> None:
        Warrior.__init__(self)
    
    def getWeapons(self):
        return super().getWeapons(repr(self))    #ask
    def __repr__(self) -> str:
        return 'Viking'

class Samurai(Warrior):
    def __init__(self) -> None:
        Warrior.__init__(self)
    def getWeapons(self):
        return super().getWeapons(repr(self))

    def __repr__(self) -> str:
        return 'Samurai'
class Maratha(Warrior):
    def __init__(self) -> None:
        Warrior.__init__(self)
    def getWeapons(self):
        return super().getWeapons(repr(self))
    def __repr__(self) -> str:
        return 'Maratha'
class Knight(Warrior):
    def __init__(self) -> None:
        Warrior.__init__(self)
    def getWeapons(self):
        return super().getWeapons(repr(self))
    def __repr__(self) -> str:
        return 'Knight'
