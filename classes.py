from copy import copy, deepcopy

#snapshot of moment in time in model
class ResultHolder:
  def __init__(self,people,pos_changes,neg_changes):
    self.people = deepcopy(people)
    self.pos_changes = deepcopy(pos_changes)
    self.neg_changes = deepcopy(neg_changes)

class Demographic:
  def __init__(self, sex, min_age, max_age,how_many):
    #super fragile according to SO, but works for this purpose
    self.__dict__.update(locals())

class Person:
  #passing in intervals so I can use consistant 
  #random seed across runs
  def __init__(self, demographic,start_age_interval,end_age_interval,exercised,socialized):
    self.sex = demographic.sex
    self.start_age = demographic.min_age + start_age_interval
    self.end_age = self.start_age + end_age_interval
    self.exercised = exercised
    self.socialized = socialized

  def __repr__(self):
    return "Sex: " + self.sex + " Age: " + str(self.start_age)

  #ASSUMPTION: QALY falls to 2/3 if not fully socialized. Impact
  #of low exercise less (though exercise affects lifespan elsewhere)
  def qaly_per_year(self):
    qaly = 1.0
    if (self.socialized == False): qaly -= .33 
    if (self.exercised == False):  qaly -= .1 
    return qaly

  def qalys(self):
    return self.qaly_per_year() * (self.end_age - self.start_age)

  #ASSUMPTION: Python-based exercise extends life 1 year
  def set_exercised(self,val):
    if val == True and self.exercised == False:
      self.end_age = self.end_age + 1
    self.exercised = val

  def set_socialized(self,val):
    self.socialized = val    

  def set_end_age(self,val):
    self.end_age = val 