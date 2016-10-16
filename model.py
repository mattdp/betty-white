#!/usr/bin/env python
import numpy
import random

todo = """
MAJOR
set age in initializer better
set death dates better

MINOR
set exercise and socialized distributions in initial condition
annotate the classes
"""

#ASSUMPTION: All FL residents 65 and up retired.
#ASSUMPTION: Modeling all FL residents under 92 to start model.

class Demographic:
  def __init__(self, sex, min_age, max_age,how_many):
    #super fragile according to SO, but works for this purpose
    self.__dict__.update(locals())

class Person:
  def __init__(self, demographic):
    self.sex = demographic.sex
    self.start_age = demographic.min_age

    self.current_death_age = self.start_age + random.randint(1,7)
    self.previous_death_age = self.current_death_age
    self.exercise = False
    self.socialized = False

  def __repr__(self):
    return "Sex: " + self.sex + " Age: " + str(self.start_age)

#SOURCE: https://suburbanstats.org/population/how-many-people-live-in-florida
demographics = [
  Demographic("male",65,66,184668),
  Demographic("male",67,69,259120),
  Demographic("male",70,74,354152),
  Demographic("male",75,79,276041),
  Demographic("male",80,84,201086),
  Demographic("male",85,92,150291),
  Demographic("female",65,66,210152),
  Demographic("female",67,69,297833),
  Demographic("female",70,74,407016),
  Demographic("female",75,79,329435),
  Demographic("female",80,84,266334),
  Demographic("female",85,92,249861)]

#~3.18M
total_retirees = sum([d.how_many for d in demographics])
#Based on graphical testing, it's possible to have 318 bars in a readable histogram
people_in_model = 318
#Thus, each person will represent about 10K other people.
scale_factor = 10000

#chance that person fits a given demographic should fit population distribution
probability_distribution = [1.0*d.how_many/total_retirees for d in demographics]

people = []
possible_range = numpy.arange(0, len(demographics))
for x in range (0,people_in_model):
  #select which demographic the person will be
  which_demographic = numpy.random.choice(possible_range, p = probability_distribution)
  demographic = demographics[which_demographic]
  people.append(Person(demographic))

print people