import yaml
from weapons import Weapon
from player import Player
from getpass import getpass
import sys
import json
import os
from colorama import Fore, Style


settings: dict[str, list[str]] = yaml.load(open('config.yml'), Loader=yaml.FullLoader) #Loads config file

if __name__ == '__main__': 

  print(Fore.CYAN + '#' * 8, "Welcome to the ULTIMATE CLASH OF WARRIORS", '#' * 8 + Style.RESET_ALL) 
  print (Fore.YELLOW + ' Play this game if you like medieval weapons. There are 25 levels in this game. '+ Style.RESET_ALL)
  print (Fore.LIGHTCYAN_EX + ' You can save your game and finish later. Once all 25 levels are completed, You can see your highscore. '+ Style.RESET_ALL)
  print (Fore.YELLOW + ' Pick Up a Weapon that belongs to your warrior class, Picking up wrong weapons will give you negative points.' + Style.RESET_ALL)
  options = ['Register', "Login"]
  print(Fore.LIGHTBLUE_EX + "Select from:", ", ".join(options) + Style.RESET_ALL)
  player = Player()
  if player.displayOptions(options).lower() == 'register': #type: ignore
    while True:
      name = input(Fore.CYAN + "Warrior Name: " + Style.RESET_ALL)
      username = input(Fore.CYAN + "Username: " + Style.RESET_ALL)
      if name and username: 
        player.name = name
        player.username = username
      else: 
        print('Username or Name cannot be empty')
        continue
      while True:
        password = getpass(Fore.CYAN + "Password: " + Style.RESET_ALL)
        confirm_password = getpass("Confirm password: ")
        if password and confirm_password:
          if confirm_password == password: 
            player.password = password #Player variable
            player.hashPassword()
            player.registerPlayer()
            print(Fore.GREEN + '{0} is registered successfully'.format(player.username))
            break
          else:
            print(Fore.YELLOW +  'Passwords don\'t match, try again' + Style.RESET_ALL)
        else:
          print(Fore.YELLOW + 'Password cannot be blank or empty' + Style.RESET_ALL)
      break
  else:
    attempt = 0
    while attempt < 3:
      player.username = input(Fore.CYAN + "Username: " + Style.RESET_ALL)
      player.password = getpass(Fore.CYAN + "Password: " + Style.RESET_ALL) 
      player.hashPassword()
      if player.authenticatePlayer(): 
        print(Fore.LIGHTMAGENTA_EX + 'Successfully logged in'+ Style.RESET_ALL)
        break
      else:
        attempt += 1
        print(Fore.YELLOW + 'Username or password incorrect' + Style.RESET_ALL )
    else:
      print(Fore.YELLOW + 'Max attempt reached' + Style.RESET_ALL)
      sys.exit('Bye!')

  while True:
    select_option: str = player.displayOptions(settings['start_list']) #type: ignore
    if select_option.lower() == 'high score':
      player.showHighscore()
      select_option = player.displayOptions(['Go back']) #type: ignore
    elif select_option.lower() == 'logout':
      player.logoutPlayer()
      sys.exit('Bye!')
    elif select_option.lower() == 'load game':
      player.loadGame()
    else:
      if player.chooseWarrior(settings['warrior_list']): #select Warrior
        continue 
