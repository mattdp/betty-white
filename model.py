#!/usr/bin/env python
from classes import Demographic, Person
import numpy as np
import matplotlib.pyplot as plt
import random
from copy import copy, deepcopy
from itertools import cycle
from six.moves import zip

#For a BAHfest 2016 speech - goal is a credible presentation on false, silly idea

todo = """
MAJOR
get to final numbers that i like - should be net + at 10/20 percent attrition
make a one-chart comparison for ups and downs vs initial
  could do with having black/green/red in all charts, and sending all
  negs to red an pos to green

MINOR
annotate the classes
check out repo and kill extraneous files
add a README
eliminate these notes
"""

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
    difference = after_qalys[i] - before_qalys[i]
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
def graph(base_qalys,pos_change,neg_change=0):
  if neg_change == 0: neg_change = pos_change #temp, for intermediate compatibility
  values = [base_qalys, pos_change, neg_change]

  plt.ylim(0,max_qalys_for_axis) #magic global number based on how high QALYs get
  plt.xlim(0,len(base_qalys))

  #stuff I'm mostly copying without understanding
  fig, ax = plt.subplots(1, 1)
  ax.get_xaxis().set_ticks([]) #added
  stack_bar(ax, values, width=1)#edgecolor='None')
  plt.draw()

people = []
results = [0,0,0,0,0]

def results_guide(index):
  if index == 0: return "base case"
  if index == 1: return "with socialization"
  if index == 2: return "with socialization and exercise"
  if index == 3: return "minus 90 year old male socialization"
  if index == 4: return "minus snake deaths"
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

  start_age_interval = random.randint(0,demographic.max_age - demographic.min_age)
  end_age_interval = random.randint(1,7)
  exercised = random.choice([True,False])
  socialized = random.choice([True,True,False])
  person = Person(demographic,start_age_interval,end_age_interval,exercised,socialized)
  people.append(person)

people = sorted(people, key=Person.qalys)
results[0] = deepcopy(people)

#snakes help everyone be social!
for p in people:
  p.set_socialized(True)

results[1] = deepcopy(people)

#snakes help everyone exercise!
for p in people:
  p.set_exercised(True)

results[2] = deepcopy(people)

#Presentation says they are fully socialized, so this gives us a
#correction for falsely giving them social QALYs earlier
for p in people:
  if p.sex == "male" and p.start_age >= 90:
    p.set_socialized(False)

results[3] = deepcopy(people)

#Snakes occasionally kill people :(
i = 1
for p in people:
  if i % 100 == 0:
    p.set_end_age(p.start_age)
  i += 1

results[4] = deepcopy(people)

#first, graph the baseline QALYs alone
changes = compare_populations(results[0],results[0])["details"]
graph(population_qalys(results[0]),changes)

for i in range(0,len(results)-1): #since doing a +1 in body
  changes = compare_populations(results[i],results[i+1])["details"]
  graph(population_qalys(results[i]),changes)
  op_string = "Population QALYs for " + results_guide(i) + ": "
  op_string += str(compare_populations(results[0], results[i]))
  print op_string

#last, graph the final state alone. yes, this is not DRY
changes = compare_populations(results[4],results[4])["details"]
graph(population_qalys(results[4]),changes)
op_string = "Population QALYs for " + results_guide(4) + ": "
op_string += str(compare_populations(results[0], results[4]))
print op_string

plt.show()