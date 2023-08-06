#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Find global optimal path using a genetic algorithm
"""

import numpy as np
from numpy.random import randint, rand, choice

def get_shortest_path_ga(Q, *arg, **kwarg):
    # setup problem
    solver = GASolver(Q, *arg, **kwarg)
    
    # Check whether at least one path exists
    if 0 in solver.Q_size:
        return {'success': False}
    
    # run ga algorithm
    f_opt, path_index, fvec = solver.run()
    path = [ Q[i][path_index[i], :] for i in range(solver.n_path) ]
    return {'success': True, 'path': path, 'length': -f_opt}

#=============================================================================
# GA class
#=============================================================================

class GASolver():
  """ Find a shortest path in a discretized joint solution space Q using a
  genetic algorithm.
  
  Attributes
  ----------
  Q : list of numpy.ndarray of float
  n_path : int
    Number of path points, len(Q).
  Q_size : list of int
    Number of joint solutions for every path point in Q.
  cross_rate : float
    Crossover rate.
  mut_rate : float
    Mutation rate.
  gen : int
    The number of generations that the genetic algorithm goas through.
  """
  def __init__(self, Q, cross_rate=0.8, mut_rate=0.1, pop_size=30, gen=100):
    self.Q = Q
    self.n_path = len(Q)
    self.Q_size = [len(q) for q in Q]
    
    self.cross_rate = cross_rate
    self.mut_rate = mut_rate
    self.pop_size = pop_size
    self.generations = gen
  
  def run(self):
    cnt = self.generations
    pop = self.create_population()
    f_opt = -np.inf
    f_all = []
    while(cnt > 0):
        pop = self.sort_population(pop)
        
        f_cur = self.fitness(pop[0])
        f_all.append(f_cur)
        if f_cur > f_opt:
            f_opt = f_cur
        
        pop = self.new_generation(pop)
        cnt -= 1
    f_all = np.array(f_all)
    return f_opt, pop[0], f_all
  
  def create_chromosome(self):
    """ Create array of integers representing a joint trajectory in Q.
    
    Returns
    -------
    numpy.ndarray of int
      Array with shape (n_path,) where every element represents the index of
      a joint solution for the corresponding path point in Q.
    """
    return np.array([randint(0, self.Q_size[i]) for i in range(self.n_path)])

  def create_population(self):
    """ Create a array with a chromosome on every row
    
    Parameters
    ----------
    size : int
      Population size, the number of chromosomes in the array.
    
    Returns
    -------
    numpy.ndarray of int
      Array with shape (size, n_path) containing a chromosome on every row.
    """
    pop = [self.create_chromosome() for i in range(self.pop_size)]
    return np.array(pop)
  
  def fitness(self, c):
    """ Evaluate the cost of a chromosome, currently joint motion is minimised.
    """
    path = self.get_path(c)
    dp   = np.diff(path, axis=0)
    return -np.sum(np.abs(dp))
  
  def mutate(self, c, rate):
    """ Mutate a chromosome
    
    A random value in the chromosome is changed when a uniform random number
    is lower than rate, the given mutation rate.
    
    TODO Fix low mutation rate if the random replacement gene is the same
    as the original. Only relevant if there is a small number of joint
    solutions for a path point.
    
    Parameters
    ----------
    numpy.ndarray of int
      Array with shape (n_path,) where every element represents the index of
      a joint solution for the corresponding path point in Q.
    rate : float
      A number between 0 and 1 representing the probability that a chromosome
      will be mutated.
    """
    if rand() < rate:
        c_m = c.copy()
        m_i = randint(0, len(c))
        c_m[m_i] = randint(0, self.Q_size[m_i])
        return c_m
    else:
        return c
    
  def crossover(self, ch1, ch2, rate):
    """ Single point crossover between two chromosomes
    
    With a given rate, crossover two chromosomes by swapping the content
    op to a given random index. For example:
    [1, 2, 3, 4] and [10, 11, 12, 13] => [10, 11, 12, 4] and [1, 2, 3, 13]
    
    Parameters
    ----------
    ch1 : numpy.ndarray of int
      The first chromosome
    ch2 : numpy.ndarray of int
      The second chromosome
    rate : float
      A number between 0 and 1 representing the probability that crossover
      will occur.
    
    Returns
    -------
    tuple of numpy.ndarray of int
      A tuple containing the two crossed over chromosomes.
    """
    if rand() < rate:
        index = randint(0, len(ch1))
        c1 = np.hstack(( ch1[:index], ch2[index:] ))
        c2 = np.hstack(( ch2[:index], ch1[index:] ))
    else:
        c1 = ch1
        c2 = ch2
    return c1, c2
  
  def sort_population(self, pop):
    """ Sort the population from highest fitness to lowest fitness.
    """
    fit = [self.fitness(ci) for ci in pop]
    # change sign because argsort default to sort from small to big
    # and we want the biggest fitness at the first.
    fit = -np.array(fit)
    return pop[ fit.argsort() ]
  
  def new_generation(self, pop):
    """ Create a new population based on the previous one.
    """
    p_size = len(pop) # if an odd number, the next pop will have size+1
    current_size = 0
    new_pop = []
    while(current_size < p_size):
        # select couple
        # better one of the first elemens in pop, because they are ordered
        # based on fitness
        prob = np.linspace(1, 0, p_size)
        prob = prob / np.sum(prob)
        prob = list(prob)
        couple = choice(p_size, 2, p = prob)
        # mate couple
        c1, c2 = self.crossover(pop[couple[0]],
                                pop[couple[1]],
                                self.cross_rate)
        # mutate children
        c1 = self.mutate(c1, self.mut_rate)
        c2 = self.mutate(c2, self.mut_rate)
        # add children to new population
        new_pop.append(c1)
        new_pop.append(c2)
        current_size += 2
    return np.array(new_pop)
  
  def get_path(self, c):
    """ Get joint space path from data Q based on list of indices
    
    Parameters
    ----------
    c : list of int
      List of the index of the joint solution that should be selected for
      every path point in Q.
    
    Returns
    -------
    numpy.ndarray
      Array of shape (n_path, ndof) containing a discrete path in joint space.
    """
    return np.array([self.Q[i][c[i]] for i in range(self.n_path)])