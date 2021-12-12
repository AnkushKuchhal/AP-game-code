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
        self.loggedIn: bool = True #shows user is online or offline
        self.stage: int = 1 #initial stage will be 1
        self.score: int = 0 #innitial score will be zero

    def __repr__(self) -> str:
        return f'Player: {self.username} PlayerName: {self.name} Status: {"Online" if self.loggedIn else "Offline"}'

    def hashPassword(self): #hash the password using sha256
        sha256 = hashlib.sha256() 
        sha256.update(self.password.encode('utf-8'))
        self.password = sha256.hexdigest()

    
    def registerPlayer(self):
        db = shelve.open('playerdb') #opens a database
        while True: #runs until valid credentials is given
            if self.username in db: #Check if username is taken
                username = input(Fore.YELLOW +  f'"{self.username}" is taken try a different username: ' + Style.RESET_ALL) 
                if username:
                    self.username = username
                else: print('Username cannot be blank')
            else:
                db[self.username] = self #saves user in db while registering 
                db.close()
                break
    
    def authenticatePlayer(self) -> bool:
        db = shelve.open('playerdb')
        if self.username in db: #username exists in the db
            if self.password == db[self.username].password: #compares the user entered password from db password
                player: Player = db[self.username] 
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
        db = shelve.open('playerdb') #opens db
        print(Fore.WHITE + 'Highscorer List' + Style.RESET_ALL)
        for c, users in enumerate(db, start=1): #shows the highscore fetching from db
            print(Fore.LIGHTMAGENTA_EX + "{0}) {1} {2}".format(c, db[users].username, db[users].highscore)+ Style.RESET_ALL) 
        db.close()


    def logoutPlayer(self) -> None:
        db = shelve.open('playerdb', writeback=True)
        self.loggedIn = False #changes the loggedin entry in DB
        try:
            db[self.username].loggedIn = False 
            db[self.username].highscore = self.highscore #save the highscore 
        except Exception as e:
            pass
        finally:   
            db.close()

    def displayOptions(self, option_list: Union[list[int], list[str], list[dict[str, Union[str, int]]]]) -> Union[int, str, dict[str, Union[str, int]]]: #displays and gives option to enter numeric values (1/2) for every list printed
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
                if int(warriorOption) in range(1, len(option_list) + 1): #starts from the 1 to the length of the list
                    option = option_list[int(warriorOption) - 1] #reduces the user input by 1 so code selects the correct option
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

    def chooseWarrior(self, option_list): #helps select the warrior type  
        warrior = self.displayOptions(option_list)
        if warrior == 'Viking': self.warrior = Viking()
        elif warrior == 'Samurai': self.warrior = Samurai()
        elif warrior == 'Maratha': self.warrior = Maratha()
        elif warrior == 'Knight': self.warrior = Knight()  
        else: return 'back'
        print(Fore.YELLOW + "Welcome {0} the {1}".format(self.name,self.warrior) + Style.RESET_ALL)
        self.startLevel()

    def checkWeapon(self, selected_weapon: dict[str, int]) -> bool:
        if selected_weapon in self.warrior.getWeapons(): return True #helps adding or subtracting the score from the current score
        else: return False

    def loadGame(self): #loads game from the .txt file
        if os.path.isfile(os.path.join('saves','savedgame_%s.txt' %(self.username))): #checks if username matches in the text file folder
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


    def saveGame(self): #saves game 
        while True:
            selected = input('Your existing save will be overwritten, Do you want to continue?[y/n]: ')
            if selected.lower() in ('y', ):
                D = {}
                D[self.username] = {
                    "stage": self.stage, 
                    "score": self.score,
                    "previous_save": True,
                    "warrior": repr(self.warrior)
                    }
                json.dump(D, open(os.path.join('saves','savedgame_%s.txt' %(self.username)), 'w'), indent=4)
                print(Fore.CYAN + 'Game successully saved. You were on level {0} and your score was {1}'.format(self.stage, self.score) + Style.RESET_ALL)
                return True
            elif selected.lower() in ('n', ): return False
            
            else: print(Fore.LIGHTBLUE_EX + 'Invalid option provided, press "y" for yes and "n" for no' + Style.RESET_ALL)

    def startLevel(self): #prints next levels while picked a weapon or manually changing the level
        
        while self.stage <= 25: #total levels 25
            print (Fore.YELLOW + 'Hi {0},there are 25 levels in this game. Please pick up a weapon that belongs to your warrior class {1} to get points'.format(self.name,self.warrior)+ Style.RESET_ALL)
            print(Fore.LIGHTMAGENTA_EX + 'Starting {1} level {0}'.format(self.stage, self.warrior) + Style.RESET_ALL)
            selected_option = self.displayOptions(['List Weapon on current level', 'Show current Score', 'List Next 3 Level', 'Save Game'])
            if selected_option.lower() == 'save game': 
                self.saveGame() #Save game
            elif selected_option.lower() == 'list weapon on current level': #will list the weapons on every level 
                weapons_from1, weapons_from2 = random.choices([Viking(), Maratha(), Samurai(), Knight()], k=2)
                weapons = random.choices(weapons_from1.getWeapons()) + random.choices(weapons_from2.getWeapons()) + ['Go back'] #incase user doesnt pick up a weapon
                selected_weapon = self.displayOptions(weapons) 
                if isinstance(selected_weapon, dict):
                    if self.checkWeapon(selected_weapon): 
                        self.score +=  selected_weapon["value"] #adds the value of choosen weapon if belongs to the same class
                    else:
                        self.score += (-abs(selected_weapon["value"]))  #subtracts the value of doesnt belong to the same class as warrior
                    self.stage += 1 #moves to next stage when a weapon is picked
                else: continue
            elif selected_option.lower() == 'show current score': #shows player current score while playing the game
                print(Fore.CYAN + "Your score is {}".format(self.score) + Style.RESET_ALL)
            elif selected_option.lower() == "list next 3 level": #lists lext 3 levels
                print(Fore.CYAN +  f"Which level do you want to jump to?[max 25][current level [{self.stage}]]" + Style.RESET_ALL)
                if self.stage < 25: 
                    if self.stage < 23: #prints next 3 levels, 23,24,25
                        newoptions = list(range(self.stage+1, self.stage + 4)) 
                    elif (self.stage == 24) or (self.stage == 23): #if user on level 24, prints only 1 level to change manually
                        newoptions = list(range(self.stage+1, 26)) 
                    selected_stage = self.displayOptions(newoptions) 
                    self.stage = selected_stage #type: ignore
                else:
                    print(Fore.YELLOW + 'You are at max level cannot jump to anymore level' + Style.RESET_ALL) #at level 25
        else: 
            print(Fore.CYAN + f'Your final score is {self.score}' + Style.RESET_ALL)
            if self.highscore < self.score: #updates the high score if greater than previos value
                self.highscore = self.score
            self.logoutPlayer()
            sys.exit()
