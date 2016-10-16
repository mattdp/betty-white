#!/usr/bin/env python

#ASSUMPTION: All FL residents 65 and up retired.
#ASSUMPTION: Modeling all FL residents under 92 to start model.

class Demographic:
  def __init__(self, sex, min_age, max_age,how_many):
    self.sex = sex
    self.min_age = min_age
    self.max_age = max_age
    self.how_many = how_many

#SOURCE: https://suburbanstats.org/population/how-many-people-live-in-florida
demos = [
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
total_retirees = sum([d.how_many for d in demos])
#Based on graphical testing, it's possible to have 318 bars in a readable histogram
people_in_model = 318
#Thus, each person will represent about 10K other people.
scale_factor = 10000