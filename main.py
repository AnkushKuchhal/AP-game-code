import yaml
from player import Player
from getpass import getpass
import sys
import json
import os
from colorama import Fore, Style


settings: dict[str, list[str]] = yaml.load(open('config.yml'), Loader=yaml.FullLoader) #Loads config file

if __name__ == '__main__': 
  print(Fore.LIGHTCYAN_EX + "\n \n \n \n"
    f" __-----_________________[]]__________________________________________________\n"
    f"&&&&&&&#%%&#%&%&%&%&%#%&|[]]__________________________________________________\ \n"
    f"                         []]\n\n")
                                                    
  print(Fore.CYAN +  f"d  d  b d sss   d        sSSs.   sSSSs   d s   sb d sss        sss sssss   sSSSs        sss sssss d    d d sss\n"        
                     f"S  S  S S       S       S       S     S  S  S S S S                S      S     S           S     S    S S\n"            
                     f"S  S  S S       S      S       S       S S   S  S S                S     S       S          S     S    S S\n"           
                     f"S  S  S S sSSs  S      S       S       S S      S S sSSs           S     S       S          S     S sSSS S sSSs\n"      
                     f"S  S  S S       S      S       S       S S      S S                S     S       S          S     S    S S  \n"          
                     f"S  S  S S       S       S       S     S  S      S S                S      S     S           S     S    S S  \n"          
                     f"...ss`S P sSSss P sSSs   `sss`   `sss`   P      P P sSSss          P       `sss`            P     P    P P sSSss  \n"+ Style.RESET_ALL) 
  print( Fore.CYAN + 
    f"d       b d      sss sssss d d s   sb d s.   sss sssss d sss          sSSs. d      d s.     sss. d    d \n" 
    f"S       S S          S     S S  S S S S  ~O      S     S             S      S      S  ~O  d      S    S \n" 
    f"S       S S          S     S S   S  S S   `b     S     S            S       S      S   `b Y      S    S \n" 
    f"S       S S          S     S S      S S sSSO     S     S sSSs       S       S      S sSSO   ss.  S sSSS \n" 
    f"S       S S          S     S S      S S    O     S     S            S       S      S    O      b S    S \n" 
    f"S     S   S          S     S S      S S    O     S     S             S      S      S    O      P S    S \n" 
    f"`sss`     P sSSs     P     P P      P P    P     P     P sSSss        `sss` P sSSs P    P ` ss`  P    P \n" )

  print (Fore.CYAN + 
    f"   sSSSs   d sss       d  d  b d s.   d ss.  d ss.  d   sSSSs   d ss.    sss. \n" 
    f"  S     S  S           S  S  S S  ~O  S    b S    b S  S     S  S    b d     \n"  
    f" S       S S           S  S  S S   `b S    P S    P S S       S S    P Y      \n" 
    f" S       S S sSSs      S  S  S S sSSO S sS'  S sS'  S S       S S sS'    ss.  \n" 
    f" S       S S           S  S  S S    O S   S  S   S  S S       S S   S       b \n" 
    f"  S     S  S            S  S S S    O S    S S    S S  S     S  S    S      P \n" 
    f"   `sss`   P             `ss`S P    P P    P P    P P   `sss`   P    P ` ss  \n" )
                                                                             


  print (Fore.YELLOW + ' Play this game if you like medieval weapons. There are 25 levels in this game. '+ Style.RESET_ALL)
  print (Fore.LIGHTCYAN_EX + ' You can save your game and finish later. Once all 25 levels are completed, You can see your highscore. '+ Style.RESET_ALL)
  print (Fore.YELLOW + ' Pick Up a Weapon that belongs to your warrior class, Picking up wrong weapons will give you negative points.' + Style.RESET_ALL)

  options = ['Register', "Login"] #for login/register page
  print(Fore.LIGHTBLUE_EX + "Select from:", ", ".join(options) + Style.RESET_ALL)
  player = Player()
  if player.displayOptions(options).lower() == 'register': 
    while True:
      name = input(Fore.CYAN + "Warrior Name: " + Style.RESET_ALL)
      username = input(Fore.CYAN + "Username: " + Style.RESET_ALL)
      if name and username: #checks username and name are not empty
        player.name = name # saves the name when register
        player.username = username #saves the username when register
      else: 
        print('Username or Name cannot be empty') #error message when username/ name empty
        continue
      while True:
        password = getpass(Fore.CYAN + "Password: " + Style.RESET_ALL)
        confirm_password = getpass("Confirm password: ")
        if password and confirm_password: #checks password and confirm password are not empty
          if confirm_password == password: 
            player.password = password #Player variable
            player.hashPassword()
            player.registerPlayer()
            print(Fore.GREEN + '{0} is registered successfully'.format(player.username))
            break
          else:
            print(Fore.YELLOW +  'Passwords don\'t match, try again' + Style.RESET_ALL) #error message when password doesnot match
        else:
          print(Fore.YELLOW + 'Password cannot be blank or empty' + Style.RESET_ALL) #error message when username/ name empty
      break
  else:
    attempt = 0 #wrong password max 3 attempts
    while attempt < 3:
      player.username = input(Fore.CYAN + "Username: " + Style.RESET_ALL)
      player.password = getpass(Fore.CYAN + "Password: " + Style.RESET_ALL) 
      player.hashPassword() #hashing the password
      if player.authenticatePlayer(): #matching the hash from the database
        print(Fore.LIGHTMAGENTA_EX + 'Successfully logged in'+ Style.RESET_ALL)
        break
      else:
        attempt += 1
        print(Fore.YELLOW + 'Username or password incorrect' + Style.RESET_ALL )
    else:
      print(Fore.YELLOW + 'Max attempt reached' + Style.RESET_ALL)
      sys.exit('Bye!')

  while True:
    select_option: str = player.displayOptions(settings['start_list']) #shows contents of start list
    if select_option.lower() == 'high score':
      player.showHighscore() #shows high score
      select_option = player.displayOptions(['Go back'])
    elif select_option.lower() == 'logout':
      player.logoutPlayer() #logout player
      sys.exit('Bye!')
    elif select_option.lower() == 'load game':
      player.loadGame() #loads game
    else:
      if player.chooseWarrior(settings['warrior_list']): #shows contents of warrior list
        continue 
