#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import random
from itertools import cycle
from six.moves import zip

todo = """
MAJOR
pick up at measuring QALYs across population, one general method 
  should compare two populations, so can have a before and after group
    this way stuff like exercise can be toggled

set age in initializer better
set death dates better

MINOR
might make sense to make population class for group methods on people
upgrade Python version
set exercise and socialized distributions in initial condition
annotate the classes
"""

what_graphing = """
persons stay in same location in array
want to have it total to:
  if lost QALYs, the old total (new QALYs in grey, lost in red)
  if gained QALYs, the new total (old QALYs in grey, gained in green)
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

  def qaly_per_year(self):
    qaly = 1.0
    if (self.socialized == False): qaly -= .33 
    if (self.exercise == False):   qaly -= .1 
    return qaly

# thanks to "tacaswell" on github!
# copied from https://gist.github.com/tacaswell/b1a35a27a7d73f7408d2
def stack_bar(ax, list_of_vals, color_cyle=None, **kwargs):
    """
    Generalized stacked bar graph.
    kwargs are passed through to the call to `bar`
    Parameters
    ----------
    ax : matplotlib.axes.Axes
       The axes to plot to
    list_of_vals : iterable
       An iterable of values to plot
    color_cycle : iterable, optional
       color_cycle is None, defaults
       to `cycle(['r', 'g', 'b', 'k'])`
    """
    if color_cyle is None:
        color_cyle = cycle(['r', 'g', 'b', 'k'])
    else:
        color_cycle = cycle(color_cycle)


    v0 = len(list_of_vals[0])
    if any(v0 != len(v) for v in list_of_vals[1:]):
           raise ValueError("All inputs must be the same length")

    edges = np.arange(v0)
    bottom = np.zeros(v0)
    for v, c in zip(list_of_vals, color_cyle):
        ax.bar(edges, v, bottom=bottom, color=c, **kwargs)
        bottom += np.asarray(v)

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
#Needed for graphs, haven't looked into why
fig, ax = plt.subplots(1, 1)

#chance that person fits a given demographic should fit population distribution
probability_distribution = [1.0*d.how_many/total_retirees for d in demographics]

people = []
possible_range = np.arange(0, len(demographics))
for x in range (0,people_in_model):
  #select which demographic the person will be
  which_demographic = np.random.choice(possible_range, p = probability_distribution)
  demographic = demographics[which_demographic]
  people.append(Person(demographic))

ages = [ p.start_age for p in people]

print people[0].qaly_per_year()

#test that graphing is working
# values = [ages]
# stack_bar(ax, values, width=1, edgecolor='None')
# plt.show()