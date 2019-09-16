#!/usr/local/bin/python3
"""
rpg.py - entry point for the RPG Game

Written by Bruce Fuda for Intermediate Programming
Python RPG Assignment 2015
Modified with permission by Edwin Griffin for
Intermediate Programming Object-Oriented Assignment 2018
"""

# import modules
import sys
import time

class Battle:

  def __init__(self, player, enemies, app):
    """
    Instantiates a battle object between the players and enemies specified,
    sending output to the given gui instance
    """
    self.player = player
    self.enemies = enemies
    self.app = app
    self.turn = 1
    self.wins = 0
    self.kills = 0
    self.player_won = False
    self.player_lost = False
  
  def play(self):
    """
    Begins and controls the battle
    returns tuple of (win [1 or 0], no. kills)
    """
    
    while not self.player_won and not self.player_lost:
      
      self.app.write("Turn "+str(self.turn))
      self.app.write("")
      time.sleep(1)
      
      # This is where the bulk of the battle takes place
      self.do_player_actions()
      self.do_enemy_actions()
      
      # advance turn counter
      self.turn += 1
      
    return (self.wins, self.kills)

  def get_action(self):
    """ Gets the player's chosen action for their turn """
    while True:
      try:
        self.app.write(self.player.name + "'s Turn:")
        self.app.write("1. Attack Enemies")
        self.app.write("2. Use Abilities")
        self.app.write("3. Use Healing")
        self.app.write("")
        self.app.wait_variable(self.app.inputVariable)
        player_action = self.app.inputVariable.get()

        if player_action == 'quit':
          self.app.quit()

        player_action = int(player_action)
        if player_action not in range(1,4):
          raise ValueError
        else:
          break

      except ValueError:
        self.app.write("You must enter a valid choice")
        self.app.write("")
    
    return player_action

  def select_ability(self):
    """ Selects the ability the player would like to use """
    player_race = self.player.__class__.__name__

    while True:
      try:
        self.app.write("Select your ability:")
        if player_race in ["Wizard","Cyborg"] and self.player.energy >= 10:
          self.app.write("1. Punch (10 eg)")
        if self.player.energy >= 20:
          self.app.write("2. Shield (20 eg)")
        self.app.write("0. Cancel Ability")
        self.app.write("")
        self.app.wait_variable(self.app.inputVariable)
        ability_choice = self.app.inputVariable.get()

        if ability_choice == 'quit':
          self.app.quit()
        ability_choice = int(ability_choice)
        if ability_choice == 0:
          return False
        valid_ability = self.player.valid_ability(ability_choice)
        if not valid_ability:
          raise ValueError
        else:
          break
          
      except ValueError:
        self.app.write("You must enter a valid choice")
        self.app.write("")
    
    return ability_choice

  def choose_target(self):
    """ Selects the target of the player's action """
    while True:
      try:
        self.app.write("Choose your target:")
        # use j to give a number option
        j = 0
        while j < len(self.enemies):
          if self.enemies[j].health > 0:
            self.app.write(str(j) + ". " + self.enemies[j].name)
          j += 1
        self.app.write("")
        self.app.wait_variable(self.app.inputVariable)
        target = self.app.inputVariable.get()

        if target == 'quit':
          self.app.quit()

        target = int(target)
        if not (target < len(self.enemies) and target >= 0) or self.enemies[target].health <= 0:
          raise ValueError
        else:
          break
          
      except ValueError:
        self.app.write("You must enter a valid choice")
        self.app.write("")

    return target

  def choose_stance(self):
    while True:
      try:
        self.app.write("Choose your stance:")
        self.app.write("a - Aggressive")
        self.app.write("d - Defensive")
        self.app.write("b - Balanced")
        self.app.write("")
        self.app.wait_variable(self.app.inputVariable)
        stance_choice = self.app.inputVariable.get()

        if stance_choice == 'quit':
          self.app.quit()

        if stance_choice not in ['a','d','b'] or stance_choice == '':
          raise ValueError
        else:
          break

      except ValueError:
        self.app.write("You must enter a valid choice")
        self.app.write("")
    
    return stance_choice

  def do_player_actions(self):
    """ Performs the player's actions """
  
    turn_over = False
  
    while not self.player_won and not turn_over:

      self.player.print_status()
      stance_choice = self.choose_stance()
      self.player.set_stance(stance_choice)
      
      player_action = self.get_action()

      has_attacked = False
     
      if player_action == 3:
        has_attacked = self.player.use_healing()
    
      elif player_action == 2:
        ability_choice = self.select_ability()

        if ability_choice != 0:
          has_attacked = True
          if ability_choice == 1 or ability_choice == 3:
            target = self.choose_target()
            if self.player.use_ability(ability_choice, self.enemies[target]):
              self.kills += 1
          else:
            self.player.use_ability(ability_choice)
         
      else:
        target = self.choose_target()
        has_attacked = True

        if self.player.attack_enemy(self.enemies[target]):
          self.kills += 1
    
      turn_over = True
      if not has_attacked:
        turn_over = False
      else:      
        self.player_won = True
        for enemy in self.enemies:
          if enemy.health > 0:
            self.player_won = False
            break

        if self.player_won == True:
          self.app.write("Your enemies have been vanquished!!")
          self.app.write("")
          time.sleep(1)
          self.wins += 1

  def do_enemy_actions(self):
    """ Performs the enemies' actions """

    turn_over = False
    
    if not self.player_won:
      self.app.write("Enemies' Turn:")
      self.app.write("")
      time.sleep(1)
    
      for enemy in self.enemies:
        if enemy.health > 0 and not self.player_lost:

          if not self.player_lost:
            self.player_lost = enemy.move(self.player)

      if self.player_lost == True:
        self.app.write("You have been killed by your enemies.")
        self.app.write("")
        time.sleep(1)
