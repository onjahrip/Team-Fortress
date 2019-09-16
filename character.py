#!/usr/local/bin/python3
"""
Character.py - Class definition for RPG Characters

Written by Bruce Fuda for Intermediate Programming
Python RPG Assignment 2014

Modified with permission by Edwin Griffin for
Intermediate Programming Object-Oriented Assignment 2019
"""

# import required Python modules
import time
import random

######
### Define the attributes and methods available to all characters in the Character
### Superclass. All characters will be able to access these abilities.
### Note: All classes should inherit the 'object' class.
######

class Character:
  """ Defines the attributes and methods of the base Character class """
  
  def __init__(self, char_name, app):
    """ Parent constructor - called before child constructors """
    self.attack_mod = 1.0
    self.defense_mod = 1.0
    self.name = char_name
    self.shield = 0
    self.max_shield = 50
    self.app = app

  def __str__(self):
    """ string representation of character """
    return str("You are " + self.name + " the " + self.__class__.__name__)

  def move(self, player):
    """
    Defines any actions that will be attempted before individual
    character AI kicks in - applies to all children
    """
    move_complete = False
    if self.health < 50 and self.healings > 0:
      self.set_stance('d')
      self.use_healing()
      move_complete = True
    return move_complete

#### Character Attacking Actions ####

  def set_stance(self, stance_choice):
    """ sets the fighting stance based on given parameter """
    
    if stance_choice == "a":
      self.attack_mod = 1.3
      self.defense_mod = 0.6
      self.app.write(self.name + " chose aggressive stance.")

    elif stance_choice == "d":
      self.attack_mod = 0.6
      self.defense_mod = 1.3
      self.app.write(self.name + " chose defensive stance.")

    else:
      self.attack_mod = 1.0
      self.defense_mod = 1.0
      self.app.write(self.name + " chose balanced stance.")
    self.app.write("")

  def attack_enemy(self, target):
    ''' Attacks the targeted enemy. Accepts a Character object as the parameter (enemy
    to be targeted). Returns True if target killed, False if still alive.'''

    roll = random.randint(0,20)
    hit = int(roll * self.attack_mod * self.attack)
    self.app.write(self.name + " attacks " + target.name + ".")
    time.sleep(1)

    crit_roll = random.randint(1, 10)
    if crit_roll == 10:
      hit = hit*2
      self.app.write(self.name + " scores a critical hit! Double damage inflicted!!")
      time.sleep(1)

    kill = target.defend_attack(hit)
    time.sleep(1)

    if kill:
      self.app.write(self.name + " has killed " + target.name + ".")
      self.app.write("")
      time.sleep(1)
      return True      
    else:
      return False

  def defend_attack(self, att_damage):
    ''' Defends an attack from the enemy. Accepts the "hit" score of the attacking enemy as
    a parameter. Returns True is character dies, False if still alive.'''
    
    # defend roll
    roll = random.randint(1, 20)
    block = int(roll * self.defense_mod * self.defense)
        
    # Roll for dodge - must roll a 10 (10% chance)
    dodge_roll = random.randint(1, 10)
    if dodge_roll == 10:
      self.app.write(self.name + " successfully dodges the attack!")
      block = att_damage
      time.sleep(1)

    # Calculate damage from attack
    damage = att_damage - block
    if damage < 0:
      damage = 0

    # If character has a shield, shield is depleted, not health
    if self.shield > 0:
      # Shield absorbs all damage if shield is greater than damage
      if damage <= self.shield:
        self.app.write(self.name + "'s shield absorbs " + str(damage) + " damage.")
        time.sleep(1)
        self.shield = self.shield - damage
        damage = 0
      # Otherwise some damage will be sustained and shield will be depleted
      elif damage != 0:
        self.app.write(self.name + "'s shield absorbs " + str(self.shield) + " damage.")
        time.sleep(1)
        damage = damage - self.shield
        self.shield = 0
      
    # Reduce health
    self.app.write(self.name + " suffers " + str(damage) + " damage!")
    self.health = self.health - damage
    time.sleep(1)
      
    # Check to see if dead or not
    if self.health <= 0:
      self.health = 0
      self.app.write(self.name + " is dead!")
      self.app.write("")
      time.sleep(1)
      return True
    else:
      self.app.write(self.name + " has " + str(self.health) + " hit points left")
      self.app.write("")
      time.sleep(1)
      return False

#### Character Ability Actions ####

  def valid_ability(self, choice):
    ''' Checks to see if the ability being used is a valid ability i.e. can be used by
    that race and the character has enough energy '''

    valid = False

    # Determine this character's race
    # This is a built-in property we can use to work out the
    # class name of the object (i.e. their race)
    race = self.__class__.__name__
    
    if choice == 1:
      if race in ["Wizard","Cyborg"] and self.energy >= 10:
        valid = True
    elif choice == 2 and self.energy >= 20:
      valid = True
        
    return valid

  def use_ability(self, choice, target=False):
    ''' Uses the ability chosen by the character. Requires 2 parameters - the ability
    being used and the target of the ability (if applicable). '''

    kill = False

    if choice == 1:
      kill = self.throw(target)
    elif choice == 2:
      self.engage_shield()
    else:
      self.app.write("Invalid ability choice. Ability failed!")
      self.app.write("")

    return kill

  def punch(self, target):
    self.energy -= 10
    self.app.write(self.name + " punches " + target.name)
    time.sleep(1)
      
    roll = random.randint(1, 10)
    defense_roll = random.randint(1, 10)
    damage = int(roll * self.mind) - int(defense_roll * target.resistance)
    if damage < 0:
      damage = 0
      
    if target.shield > 0:
      if damage <= target.shield:
        self.app.write(target.name + "'s shield absorbs " + str(damage) + " damage.")
        time.sleep(1)
        target.shield = target.shield - damage
        damage = 0
      elif damage != 0:
        self.app.write(target.name + "'s shield absorbs " + str(target.shield) + " damage.")
        time.sleep(1)
        damage = damage - target.shield
        target.shield = 0
                        
    self.app.write(target.name + " takes " + str(damage) + " damage.")
    self.app.write("")
    time.sleep(1)
    target.health = target.health - damage
      
    if target.health <= 0:
      target.health = 0
      self.app.write(target.name + " is dead!")
      self.app.write("")
      time.sleep(1)
      return True

    else:
      self.app.write(target.name + " has " + str(target.health) + " hit points left")
      self.app.write("")
      time.sleep(1)
      return False

  def engage_shield(self):
    self.energy -= 20
    self.app.write(self.name + " engages a personal shield!")
    time.sleep(1)
    if self.shield <= self.max_shield:
      self.shield = self.max_shield
    self.app.write(self.name + " is shielded from the next " + str(self.shield) + " damage.")
    self.app.write("")
    time.sleep(1)

#### Character Item Actions ####

  def use_healing(self):
    """
    Uses a healing if the player has one. Returns True if has healing,
    false if hasn't
    """
    if self.healings >= 1:
      self.healings -= 1
      self.health += 250
      if self.health > self.max_health:
        self.health = self.max_health
      self.app.write(self.name + " use healing!")
      time.sleep(1)
      self.app.write(self.name + " has " + str(self.health) + " hit points.")
      self.app.write("")
      time.sleep(1)
      return True
    else:
      self.app.write("You have no more heals left!")
      self.app.write("")
      return False

#### Miscellaneous Character Actions ####

  def reset(self):
    ''' Resets the character to its initial state '''
    
    self.health = self.max_health
    self.energy = self.max_energy
    self.healings = self.starting_healings
    self.shield = 0
    
  def print_status(self):
    ''' Prints the current status of the character '''
    self.app.write(self.name + "'s Status:")
    time.sleep(0.5)
    
    health_bar = "Health: "
    health_bar += "|"
    i = 0
    while i <= self.max_health:
      if i <= self.health:
        health_bar += "#"
      else:
        health_bar += " "
      i += 25
    health_bar += "| " + str(self.health) + " hp (" + str(int(self.health*100/self.max_health)) +"%)"
    self.app.write(health_bar)
    time.sleep(0.5)
        
    if self.max_energy > 0:
      energy_bar = "energy: "
      energy_bar += "|"
      i = 0
      while i <= self.max_energy:
        if i <= self.energy:
          energy_bar += "*"
        else:
          energy_bar += " "
        i += 10
      energy_bar += "| " + str(self.energy) + " ap (" + str(int(self.energy*100/self.max_energy)) +"%)"
      self.app.write(energy_bar)
      time.sleep(0.5)
   
    if self.shield > 0:
      shield_bar = "Shield: "
      shield_bar += "|"
      i = 0
      while i <= 100:
        if i <= self.shield:
          shield_bar += "o"
        else:
          shield_bar += " "
        i += 10
      shield_bar += "| " + str(self.shield) + " sp (" + str(int(self.shield*100/self.max_shield)) +"%)"
      self.app.write(shield_bar)
      time.sleep(0.5)   

    self.app.write("heals remaining: " + str(self.healings))
    self.app.write("")
    time.sleep(0.5)

######
### Define the attributes specific to each of the Character Subclasses.
### This identifies the differences between each race.
######

class Soldier(Character):
  '''Defines the attributes of a Soldier in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Soldier class
  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app)
    self.max_health = 250
    self.max_energy = 40
    self.starting_healings = 1
    self.attack = 7
    self.defense = 8
    self.mind = 5
    self.resistance = 4
    self.health = self.max_health
    self.energy = self.max_energy
    self.healings = self.starting_healings

  def move(self, player):
    """ Defines the AI for the Soldier class """
    move_complete = Character.move(self, player)
    if not move_complete:
      if self.health*100 / self.max_health > 75:
        self.set_stance('a')
      elif self.health*100 / self.max_health > 30:
        self.set_stance('b')
      else:
        self.set_stance('d')
      if self.shield == 0 and self.energy >= 20:
        self.use_ability(2)
      else:
        return self.attack_enemy(player)
    return False

class Heavy(Character):
  '''Defines the attributes of a Heavy in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Heavy class
  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app)
    self.max_health = 300
    self.max_energy = 30
    self.starting_healings = 1
    self.attack = 9
    self.defense = 6
    self.mind = 4
    self.resistance = 5
    self.health = self.max_health
    self.energy = self.max_energy
    self.healings = self.starting_healings

  def move(self, player):
    """ Defines the AI for the Heavy class """
    move_complete = Character.move(self, player)
    if not move_complete:
      self.set_stance('a')
      return self.attack_enemy(player)
    return False
    
class Sniper(Character):
  '''Defines the attributes of a Sniper in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Sniper class
  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app)
    self.max_health = 300
    self.max_energy = 60
    self.starting_healings = 1
    self.attack = 6
    self.defense = 8
    self.mind = 8
    self.resistance = 8
    self.health = self.max_health
    self.energy = self.max_energy
    self.healings = self.starting_healings

  def move(self, player):
    """ Defines the AI for the Sniper class """
    move_complete = Character.move(self, player)
    if not move_complete:
      self.set_stance('d')
      if self.shield == 0 and self.energy >= 20:
        self.use_ability(2)
      else:
        return self.attack_enemy(player)
    return False

class Medic(Character):
  '''Defines the attributes of a Medic in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Medic class
  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app)
    self.max_health = 250
    self.max_energy = 40
    self.starting_healings = 2
    self.attack = 3
    self.defense = 9
    self.mind = 6
    self.resistance = 10
    self.health = self.max_health
    self.energy = self.max_energy
    self.healings = self.starting_healings

  def move(self, player):
    """ Defines the AI for the Medic class """
    move_complete = Character.move(self, player)
    if not move_complete:
      self.set_stance('d')
      # Medic soldiers shield if they don't have one
      if self.shield == 0 and self.energy >= 20:
        self.use_ability(2)
      else:
        return self.attack_enemy(player)
    return False

class Pyro(Character):
  '''Defines the attributes of a Pyro in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Pyro class
  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app)
    self.max_health = 100
    self.max_energy = 0
    self.starting_healings = 0
    self.attack = 3
    self.defense = 3
    self.mind = 0
    self.resistance = 0
    self.health = self.max_health
    self.energy = self.max_energy
    self.healings = self.starting_healings

  def move(self, player):
    """ Defines the AI for the Pyro class """
    move_complete = Character.move(self, player)
    if not move_complete:
      self.set_stance('d')
      return self.attack_enemy(player)
    return False

class Demo(Character):
  '''Defines the attributes of a Demo in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Demo class
  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app)
    self.max_health = 250
    self.max_energy = 0
    self.starting_healings = 0
    self.attack = 7
    self.defense = 5
    self.mind = 2
    self.resistance = 4
    self.health = self.max_health
    self.energy = self.max_energy
    self.healings = self.starting_healings

  def move(self, player):
    """ Defines the AI for the Demo class """
    move_complete = Character.move(self, player)
    if not move_complete:
      self.set_stance('b')
      return self.attack_enemy(player)
    return False

class Helix(Character):
  '''Defines the attributes of a Helix in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Helix class
  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app)
    self.max_health = 400
    self.max_energy = 20
    self.starting_healings = 1
    self.attack = 9
    self.defense = 7
    self.mind = 4
    self.resistance = 6
    self.health = self.max_health
    self.energy = self.max_energy
    self.healings = self.starting_healings

  def move(self, player):
    """ Defines the AI for the Helix class """
    move_complete = Character.move(self, player)
    if not move_complete:
      self.set_stance('a')
      return self.attack_enemy(player)
    return False

class Wizard(Character):
  '''Defines the attributes of an Wizard in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Wizard class
  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app)
    self.max_health = 150
    self.max_energy = 100
    self.starting_healings = 2
    self.attack = 5
    self.defense = 6
    self.mind = 10
    self.resistance = 10
    self.health = self.max_health
    self.energy = self.max_energy
    self.healings = self.starting_healings

  def move(self, player):
    """ Defines the AI for the Wizard class """
    move_complete = Character.move(self, player)
    if not move_complete:
      self.set_stance('b')
      if self.energy >= 10:
        return self.use_ability(1, player)
      else:
        return self.attack_enemy(player)
    return False

class Cyborg(Character):
  '''Defines the attributes of a Cyborg Soldier in the game. Inherits the constructor and methods
  of the Character class '''
  
  # Constructor for Cyborg class
  def __init__(self, char_name, app):
    Character.__init__(self, char_name, app)
    self.max_health = 150
    self.max_energy = 100
    self.starting_healings = 2
    self.attack = 5
    self.defense = 6
    self.mind = 10
    self.resistance = 10
    self.health = self.max_health
    self.energy = self.max_energy
    self.healings = self.starting_healings

  def move(self, player):
    """ Defines the AI for the Cyborg class """
    move_complete = Character.move(self, player)
    if not move_complete:
      self.set_stance('d')
      if self.shield == 0 and self.energy >= 20:
        self.use_ability(2)
      elif self.energy >= 10:
        return self.use_ability(1, player)
      else:
        return self.attack_enemy(player)
    return False
