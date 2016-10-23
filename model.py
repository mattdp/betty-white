#!/usr/bin/env python
from classes import Demographic, Person, ResultHolder
import numpy as np
import matplotlib.pyplot as plt
import random
from copy import copy, deepcopy
from itertools import cycle
from six.moves import zip

#For a BAHfest 2016 speech - goal is a credible presentation on false, silly idea

def population_qalys(people):
  return [round(p.qalys(),2) for p in people]

#outputs a hash with three keys
#total: the total number of (QALYs after - QALYs before)
#scaled_total: the above total, scaled up for whole population
#details: a person by person QALY difference used for graphing
def compare_populations(before,after):
  output = {"total": 0, "details": []}
  before_qalys, after_qalys = population_qalys(before), population_qalys(after)
  for i in range (0,len(before)):
    difference = abs(after_qalys[i] - before_qalys[i])
    output["details"].append(difference)
  output["total"] = round(sum(output["details"]),0)
  output["scaled_total"] = output["total"] * scale_factor
  return output

# thanks to "tacaswell" on github!
# copied from https://gist.github.com/tacaswell/b1a35a27a7d73f7408d2
def stack_bar(ax, list_of_vals, **kwargs):
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
    color_cyle = cycle(['b', 'g', 'r']) #blue, green, red

    v0 = len(list_of_vals[0])
    if any(v0 != len(v) for v in list_of_vals[1:]):
           raise ValueError("All inputs must be the same length")

    edges = np.arange(v0)
    bottom = np.zeros(v0)
    for v, c in zip(list_of_vals, color_cyle):
        ax.bar(edges, v, bottom=bottom, color=c, **kwargs)
        bottom += np.asarray(v)

#TODO implement neg_change fully
def graph(base_qalys,pos_change,neg_change):

  #curious how to make this DRY. lack of pointers made this hard for me
  #since iterating on [pos,neg] didn't work out
  if pos_change == []:
    pos_change = [0 for b in base_qalys]
  if neg_change == []:
    neg_change = [0 for b in base_qalys]

  values = [base_qalys, pos_change, neg_change]

  plt.ylim(0,max_qalys_for_axis) #magic global number based on how high QALYs get
  plt.xlim(0,len(base_qalys))

  #stuff I'm mostly copying without understanding
  fig, ax = plt.subplots(1, 1)
  ax.get_xaxis().set_ticks([]) #added
  stack_bar(ax, values, width=1, edgecolor='None')
  plt.draw()

people = []
resultholders = []

def resultholders_guide(index):
  if index == 0: return "base case"
  if index == 1: return "with socialization and exercise"
  if index == 2: return "minus light snake deaths from initial condition"
  if index == 3: return "minus heavy snake deaths from initial condition"
  return "bad index"

#SOURCE: https://suburbanstats.org/population/how-many-people-live-in-florida
#ASSUMPTION: All FL residents 65 and up retired.
#ASSUMPTION: Modeling all FL residents under 95 to start model.
demographics = [
  Demographic("male",65,66,184668),
  Demographic("male",67,69,259120),
  Demographic("male",70,74,354152),
  Demographic("male",75,79,276041),
  Demographic("male",80,84,201086),
  Demographic("male",85,95,150291),
  Demographic("female",65,66,210152),
  Demographic("female",67,69,297833),
  Demographic("female",70,74,407016),
  Demographic("female",75,79,329435),
  Demographic("female",80,84,266334),
  Demographic("female",85,95,249861)]

total_retirees = sum([d.how_many for d in demographics]) #~3.18M
people_in_model = 318 #It's possible to have 318 bars in a readable histogram
scale_factor = 10000 #Thus, each person will represent about 10K other people.
random.seed(1914011105) #For repeatability when charting data
max_qalys_for_axis = 10 #Set max y of charts manually so scale same in each

#chance that person fits a given demographic should fit population distribution
probability_distribution = [1.0*d.how_many/total_retirees for d in demographics]

possible_range = np.arange(0, len(demographics))
for x in range (0,people_in_model):
  which_demographic = np.random.choice(possible_range, p = probability_distribution)
  demographic = demographics[which_demographic]

  start_age_interval = random.uniform(0,demographic.max_age - demographic.min_age)
  end_age_interval = random.uniform(1,8)
  exercised = random.choice([True,False])
  socialized = random.choice([True,True,False])
  person = Person(demographic,start_age_interval,end_age_interval,exercised,socialized)
  people.append(person)

people = sorted(people, key=Person.qalys)

#0: initial condition
resultholders.append(ResultHolder(people,[],[]))
graph(population_qalys(people),[],[])

#1: snakes help everyone be social and exercise!
for p in people:
  p.set_socialized(True)
  p.set_exercised(True)

#only positive changes, no negatives yet
pos_changes = compare_populations(resultholders[0].people,people)["details"]
newbie = ResultHolder(people,pos_changes,[])
graph(population_qalys(resultholders[0].people),pos_changes,[])
resultholders.append(newbie)

#set people to initial people, since we want negs related to initial
#condition, not off giving more QALYs then taking all away
people = deepcopy(resultholders[0].people) 

#2: snakes occasionally kill people :(
i = 1 #don't kill the first one
for p in people:
  if i % 100 == 0:
    p.set_end_age(p.start_age)
  i += 1

neg_changes = compare_populations(resultholders[0].people,people)["details"]
#for people with negative changes, we don't want any green on graph
for n in range(0,len(neg_changes)):
  if neg_changes[n] != 0: pos_changes[n] = 0

newbie = ResultHolder(people,pos_changes,neg_changes)
graph(population_qalys(people),pos_changes,neg_changes)
resultholders.append(newbie)

#3: snakes non-occasionally kill people :(
i = 1 #don't kill the first one
for p in people:
  if i % 5 == 0: #make sure this includes the divisor from earlier
    p.set_end_age(p.start_age)
  i += 1

neg_changes = compare_populations(resultholders[0].people,people)["details"]
#for people with negative changes, we don't want any green on graph
for n in range(0,len(neg_changes)):
  if neg_changes[n] != 0: pos_changes[n] = 0

newbie = ResultHolder(people,pos_changes,neg_changes)
graph(population_qalys(people),pos_changes,neg_changes)
resultholders.append(newbie)

#mysteriously, the last graph has axis problems. hence the duplicate
graph(population_qalys(people),pos_changes,neg_changes)

print sum(population_qalys(resultholders[0].people)) * scale_factor
for r in resultholders:
  print (sum(r.pos_changes) - sum(r.neg_changes)) * scale_factor

plt.show()