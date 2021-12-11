import shelve
import hashlib
from typing import Union, Optional, Any
import sys
from warrior import Knight, Maratha, Viking, Samurai
import random
from colorama import Fore, Back, Style
import os, json

class Player:
    def __init__(self, highscore:int=0, username: str="", password: str="", name: str="") -> None:
        
        self.name = name
        self.highscore = highscore
        self.username = username
        self.password =  password
        self.loggedIn: bool = True
        self.stage: int = 1
        self.score: int = 0

    def __repr__(self) -> str:
        return f'Player: {self.username} PlayerName: {self.name} Status: {"Online" if self.loggedIn else "Offline"}'

    def hashPassword(self):
        sha256 = hashlib.sha256()
        sha256.update(self.password.encode('utf-8'))
        self.password = sha256.hexdigest()

    
    def registerPlayer(self):
        db = shelve.open('playerdb') #opens a database
        while True: #runs until valid username is given
            if self.username in db: #Check if username is taken
                self.username = input(Fore.YELLOW +  f'"{self.username}" is taken try a different username: ' + Style.RESET_ALL) 
                
            else:
                db[self.username] = self #type: ignore
                db.close()
                break
    
    def authenticatePlayer(self) -> bool:
        db = shelve.open('playerdb')
        if self.username in db:
            if self.password == db[self.username].password: #type: ignore
                player: Player = db[self.username] #type: ignore
                player.loggedIn = True
                self.username = player.username
                self.loggedIn = player.loggedIn
                self.name = player.name
                self.highscore = player.highscore
                
                db.close()
                return True
            else: 
                db.close()
                return False
        else: 
            db.close()
            return False

    def showHighscore(self):
        db = shelve.open('playerdb')
        print(Fore.WHITE + 'Highscorer List' + Style.RESET_ALL)
        for c, users in enumerate(db, start=1):
            print(Fore.LIGHTMAGENTA_EX + "{0}) {1} {2}".format(c, db[users].username, db[users].highscore)+ Style.RESET_ALL) #type: ignore
        db.close()


    def logoutPlayer(self) -> None:
        db = shelve.open('playerdb', writeback=True)
        self.loggedIn = False
        try:
            db[self.username].loggedIn = False #type: ignore
            db[self.username].highscore = self.highscore #type: ignore 
        except Exception as e:
            pass
        finally:   
            db.close()

    def displayOptions(self, option_list: Union[list[int], list[str], list[dict[str, Union[str, int]]]]) -> Union[int, str, dict[str, Union[str, int]]]:
        print(Fore.YELLOW + 'Type "q" or "quit" to quit anytime and "?" for help' + Style.RESET_ALL)
        while True:
            print(Fore.LIGHTMAGENTA_EX + 'Select from following options' + Style.RESET_ALL)
            for c, start_menu in enumerate(option_list, start=1):
                if isinstance(start_menu, str):
                    print(Fore.LIGHTBLUE_EX + "{0!s}) {1}".format(c, start_menu) + Style.RESET_ALL)
                elif isinstance(start_menu, int): print("{0!s}) Level {1}".format(c, start_menu))
                else:
                    print(Fore.LIGHTBLUE_EX + "{0!s}) {1[name]}".format(c, start_menu) + Style.RESET_ALL)
            warriorOption: Optional[Union[int, str]] = input(Fore.LIGHTMAGENTA_EX + "Select option: " + Style.RESET_ALL)
            try:
                if int(warriorOption) in range(1, len(option_list) + 1):
                    option = option_list[int(warriorOption) - 1]
                    if isinstance(option, dict):
                        print(Fore.YELLOW + 'You selected: {[name]}'.format(option) + Style.RESET_ALL)
                    elif isinstance(option, int):
                        print(Fore.LIGHTCYAN_EX +  f'You selected level: {option}' + Style.RESET_ALL)
                    else: print(Fore.LIGHTBLUE_EX +  f'You selected: {option}' + Style.RESET_ALL)
                    return option
                else:
                    print(Fore.YELLOW + 'Invalid option selected'  + Style.RESET_ALL)
            except Exception as e:
              if warriorOption.lower() in ('q', 'quit'): 
                  self.logoutPlayer()
                  sys.exit('Goodbye!') 
              elif "?" == warriorOption.lower(): 
                  print(Fore.YELLOW + "Pick Up a Weapon that belongs to your warrior class to win the game" + Style.RESET_ALL)
                  continue 
              elif not isinstance(warriorOption, dict):
                  if warriorOption.lower() == 'go back': 
                      return warriorOption 
              else: print(Fore.MAGENTA + 'Invalid option selected' + Style.RESET_ALL)

    def chooseWarrior(self, option_list):
        warrior = self.displayOptions(option_list)
        if warrior == 'Viking': self.warrior = Viking()
        elif warrior == 'Samurai': self.warrior = Samurai()
        elif warrior == 'Maratha': self.warrior = Maratha()
        elif warrior == 'Knight': self.warrior = Knight()   #changed [viking > knight ]
        else: return 'back'
        print(Fore.YELLOW + "Welcome {0} the {1}".format(self.name,self.warrior) + Style.RESET_ALL)
        self.startLevel()

    def checkWeapon(self, selected_weapon: dict[str, int]) -> bool:
        if selected_weapon in self.warrior.getWeapons(): return True
        else: return False

    def loadGame(self):
        if os.path.isfile(os.path.join('saves','savedgame_%s.txt' %(self.username))):
            D = json.load(open(os.path.join('saves','savedgame_%s.txt' %(self.username))))
            if D[self.username] and D[self.username]['previous_save']: 
                self.stage, self.score = D[self.username]["stage"], D[self.username]["score"]
                if D[self.username]["warrior"] == 'Viking': self.warrior = Viking()
                elif D[self.username]["warrior"] == 'Samurai': self.warrior = Samurai()
                elif D[self.username]["warrior"] == 'Maratha': self.warrior = Maratha()
                elif D[self.username]["warrior"] == 'Knight': self.warrior = Knight()
                print(Fore.YELLOW + 'Game loaded successfully' + Style.RESET_ALL)
                print(Fore.CYAN + 'You were on level {0} and your score was {1}'.format(self.stage, self.score) + Style.RESET_ALL)
                self.startLevel()
            else: print('You don\'t have any saved games')
        else: print('You don\'t have any saved games')


    def saveGame(self):
        with open(os.path.join('saves','savedgame_%s.txt' %(self.username)), 'w') as game_file:
            while True:
                selected = input('Your existing save will be overwritten, Do you want to continue?[y]: ')
                if selected in 'y':
                    D = {}
                    D[self.username] = {
                        "stage": self.stage, 
                        "score": self.score,
                        "previous_save": True,
                        "warrior": repr(self.warrior)
                        }
                    json.dump(D, game_file, indent=4)
                    print(Fore.CYAN + 'Game successully saved. You were on level {0} and your score was {1}'.format(self.stage, self.score) + Style.RESET_ALL)
                    game_file.close()
                    return True
                
                else: print(Fore.LIGHTBLUE_EX + 'Invalid option provided, press "y" for yes' + Style.RESET_ALL)

    def startLevel(self):
        
        while self.stage <= 25: #type: ignore
            print (Fore.YELLOW + ' Hi {0},there are 25 levels in this game. Please pick up a weapon that belongs to your warrior class {1} to get points'.format(self.name,self.warrior)+ Style.RESET_ALL)
            print(Fore.LIGHTMAGENTA_EX + 'Starting {1} level {0}'.format(self.stage, self.warrior) + Style.RESET_ALL)
            selected_option = self.displayOptions(['List Weapon on current level', 'Show current Score', 'List Next 3 Level', 'Save Game'])
            if selected_option.lower() == 'save game': #type: ignore
                self.saveGame() #Save game
            elif selected_option.lower() == 'list weapon on current level': #type: ignore
                weapons_from1, weapons_from2 = random.choices([Viking(), Maratha(), Samurai(), Knight()], k=2)
                weapons = random.choices(weapons_from1.getWeapons()) + random.choices(weapons_from2.getWeapons()) + ['Go back'] #type: ignore
                selected_weapon = self.displayOptions(weapons) #type: ignore
                if isinstance(selected_weapon, dict):
                    if self.checkWeapon(selected_weapon): #type: ignore
                        self.score +=  selected_weapon["value"] #type: ignore
                    else:
                        self.score += (-abs(selected_weapon["value"]))  #type: ignore
                    self.stage += 1 #type: ignore
                else: continue
            elif selected_option.lower() == 'show current score': #type: ignore
                print(Fore.CYAN + "Your score is {}".format(self.score) + Style.RESET_ALL)
            elif selected_option.lower() == "list next 3 level": #type: ignore
                print(Fore.CYAN +  f"Which level do you want to jump to?[max 25][current level [{self.stage}]]" + Style.RESET_ALL)
                if self.stage < 25: #type: ignore
                    if self.stage < 23: #type: ignore
                        newoptions = list(range(self.stage+1, self.stage + 4)) #type: ignore
                    elif (self.stage == 24) or (self.stage == 23): 
                        newoptions = list(range(self.stage+1, 26)) #type: ignore
                    selected_stage = self.displayOptions(newoptions) #type: ignore
                    self.stage = selected_stage #type: ignore
                else:
                    print(Fore.YELLOW + 'You are at max level cannot jump to anymore level' + Style.RESET_ALL)
        else:
            print(Fore.CYAN + f'Your final score is {self.score}' + Style.RESET_ALL)
            if self.highscore < self.score:
                self.highscore = self.score
            self.logoutPlayer()
