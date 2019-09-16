#!/usr/local/bin/python3
"""
rpg.py - entry point for the RPG Game

Written by Bruce Fuda for Intermediate Programming
Python RPG Assignment 2015
Modified with permission by Edwin Griffin for
Intermediate Programming Object-Oriented Assignment 2018
"""

import time
import gui
import character
import battle

app = gui.simpleapp_tk(None)
app.title('Team Fortress')

app.write('''
  _____                        
 |_   _|__ __ _ _ __           
   | |/ -_) _` | '  \          
   |_|\___\__,_|_|_|_|         
  ___        _                 
 | __|__ _ _| |_ _ _ ___ ______
 | _/ _ \ '_|  _| '_/ -_|_-<_-<
 |_|\___/_|  \__|_| \___/__/__/
                                                                     
''')
app.write("You can exit the game at any time by typing in 'quit'")
app.write("")

def set_mode():
  """ Select the game mode """
  # This is an error checking version of reading user input
  # Understanding try/except cases is important for
  # verifying user input. See class module on Exception Handling.
  while True:
    try:
      app.write("Please select a side:")
      app.write("1. Good")
      app.write("2. Evil")
      app.write("")
      app.wait_variable(app.inputVariable)
      mode = app.inputVariable.get()
    
      if mode == 'quit':
        app.quit()
    
      mode = int(mode)
      if mode not in range(1,3):
        raise ValueError
      else:
       break
  
    except ValueError:
      app.write("You must enter a valid choice")
      app.write("")
  
  return mode

def set_race(mode):
  """ Set the player's race """
  if mode == 2: # Alien Mode
    app.write("Playing as the Blue Team.")
    app.write("")
  
    # race selection - evil
    while True:
      try:
        app.write("Please select your race:")
        app.write("1. Pyro")
        app.write("2. Demo")
        app.write("3. Helix")
        app.write("4. Wizard")
        app.write("")
        app.wait_variable(app.inputVariable)
        race = app.inputVariable.get()
      
        if race == 'quit':
          app.quit()
      
        race = int(race)
        if race not in range(1,5):
          raise ValueError
        else:
          break
    
      except ValueError:
        app.write("You must enter a valid choice")
        app.write("")

  else: # Good Mode
    app.write("Playing as the Earth Defence Forces.")
    app.write("")

    # race selection - good
    while True:
      try:
        app.write("Please select your soldier type:")
        app.write("1. Soldier")
        app.write("2. Heavy")
        app.write("3. Sniper")
        app.write("4. Medic")
        app.write("5. Cyborg")
        app.write("")
        app.wait_variable(app.inputVariable)
        race = app.inputVariable.get()
      
        if race == 'quit':
          app.quit()
        race = int(race)
      
        if race not in range(1,6):
          raise ValueError
        else:
          break
    
      except ValueError:
        app.write("You must enter a valid choice")
        app.write("")
  
  return race

def set_name():
  """ Set the player's name """
  while True:
    try:
      app.write("Please enter your Character Name:")
      app.write("")
      app.wait_variable(app.inputVariable)
      char_name = app.inputVariable.get()

      if char_name == 'quit':
        app.quit()

      if char_name == '':
        raise ValueError
      else:
        break

    except ValueError:
      app.write("")
      app.write("Your name cannot be blank")

  return char_name

def create_player(mode, race, char_name):
  """ Create the player's character """
  # Aliens
  if mode == 2:
    if race == 1:
      player = character.Pyro(char_name, app)
    elif race == 2:
      player = character.Demo(char_name, app)
    elif race == 3:
      player = character.Helix(char_name, app)
    else:
      player = character.Wizard(char_name, app)
  # Humans
  else:
    if race == 1:
      player = character.Soldier(char_name, app)
    elif race == 2:
      player = character.Heavy(char_name, app)
    elif race == 3:
      player = character.Sniper(char_name, app)
    elif race == 4:
      player = character.Medic(char_name, app)
    else:
      player = character.Cyborg(char_name, app)
  return player

def set_difficulty():
  """ Set the difficulty of the game """
  while True:
    try:
      app.write("Please select a difficulty level:")
      app.write("e - Easy")
      app.write("m - Medium")
      app.write("h - Hard")
      app.write("l - Legendary")
      app.write("")
      app.wait_variable(app.inputVariable)
      difficulty = app.inputVariable.get()

      if difficulty == 'quit':
        app.quit()

      if difficulty not in ['e','m','h','l'] or difficulty == '':
        raise ValueError
      else:
        break

    except ValueError:
      app.write("You must enter a valid choice")
      app.write("")

  return difficulty

def create_enemies(mode, difficulty):
  """ Create the enemies """
  if mode == 2: # Alien Mode - good enemies
    if difficulty == 'm':
      enemies = [character.Medic("Jensen", app), character.Medic("Marsh", app), character.Medic("Greenwood", app)]
    elif difficulty == 'h':
      enemies = [character.Heavy("Bear", app), character.Sniper("Eagle", app), character.Soldier("Jock", app)]
    elif difficulty == 'l':
      enemies = [character.Soldier("Jackson", app), character.Soldier("Maximus", app), character.Cyborg("Phoenix", app)]
    else:
      enemies = [character.Medic("Fox", app), character.Medic("Cheetah", app)]

  else: # Human Mode - evil enemies
    if difficulty == 'm':
      enemies = [character.Demo("Demo 1", app), character.Pyro("Pyro", app), character.Demo("Demo 2", app)]
    elif difficulty == 'h':
      enemies = [character.Demo("Demo 1", app), character.Demo("Demo 2", app), character.Helix("Helix", app)]
    elif difficulty == 'l':
      enemies = [character.Demo("Demo", app), character.Helix("Helix", app), character.Wizard("Wizard", app)]
    else:
      enemies = [character.Pyro("Pyro 1", app), character.Pyro("Pyro 2", app)]

  return enemies

def quit_game():
  """ Quits the game """
  while True:
    try:
      app.write("Play Again? (y/n)")
      app.write("")
      app.wait_variable(app.inputVariable)
      quit_choice = app.inputVariable.get()

      if quit_choice == 'quit':
        app.quit()

      if quit_choice not in ['y','n'] or quit_choice == '':
        raise ValueError
      else:
        break

    except ValueError:
      app.write("You must enter a valid choice")
      app.write("")

  return quit_choice

def print_results():
  app.write("Game Over!")
  app.write("No. Battles: {0}".format(str(battles)))
  app.write("No. Wins: {0}".format(wins))
  app.write("No. Kills: {0}".format(kills))
  app.write("Success Rate (%): {0:.2f}%".format(float(wins*100/battles)))
  app.write("Avg. kills per battle: {0:.2f}".format(float(kills)/battles))
  app.write("")

battles = 0
wins = 0
kills = 0

mode = set_mode()
race = set_race(mode)
char_name = set_name()
player = create_player(mode, race, char_name)
app.write(player)
app.write("")
difficulty = set_difficulty()
enemies = create_enemies(mode, difficulty)

while True:

  encounter = battle.Battle(player, enemies, app)
  battle_wins, battle_kills = encounter.play()

  battles += 1
  wins += battle_wins
  kills += battle_kills

  print_results()
    
  quit = quit_game()

  if quit == "n":
    app.write("Thank you for playing Team Fortress.")
    time.sleep(2)
    app.quit()

  else:
    # Playing again - reset all enemies and players
    player.reset()
    for enemy in enemies:
      enemy.reset()
