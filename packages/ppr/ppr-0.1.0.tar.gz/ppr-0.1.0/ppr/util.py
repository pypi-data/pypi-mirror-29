#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Some classes for "virtual" storage, where variables in a virtual array
are calculated on the fly.
Applied to path to joint transformation for 2P 3R robot
"""

import numpy as np
from ppr.path import TolerancedNumber

def cp(array):
  """ Cumulative product
  """
  return np.cumprod(array)[-1]

def setup_ranges(trajectory_pt):
  """ Get discrete axis arrays from trajectory point
  """
  ranges = []
  for i in range(trajectory_pt.dim):
    if trajectory_pt.hasTolerance[i]:
      ranges.append(trajectory_pt.p[i].range)
    else:
      ranges.append(np.array([trajectory_pt.p[i]]))
  return ranges

class VirtualArray():
  """ Virtual version of an N D array to store big grids.
  
  By supplying the discretised individual axes of an N-dimensional space
  this class can calculate grid points on the fly, instead of calculating
  and storing the whole N-dimensional array at once.
  
  In essence this converts an single integer number from the range
  [0, n1*n2*n3-1] into a list of values from the range arrays.
  [range1[n1], range[1][n2], ...] in a deterministic way.
  
  Attributs
  ---------
  ranges : list of numpy.ndarray
  dim : int
    The number of dimensions of the virtual array, the length of the list
    ranges.
  sizes : list of int
    The size of the different discrete dimensions.
  total_size : int
    The total number of grid points that can be accesed.
  """
  def __init__(self, ranges):
    """ Create virtual array
    
    Paramters
    ---------
    ranges : list of numpy.ndarray
      Every element in the list represents a discretised axis in and
      n-dimensional space, where n is the list length.
    """
    self.ranges = ranges
    self.dim = len(ranges)
    self.sizes = [len(a) for a in self.ranges]
    self.total_size  = cp(self.sizes)
  
  def __getitem__(self, index):
    """ Implement index slicing
    
    The method get's the syntac object[i] working.
    Therefore the object acts as a 1D numpy array.
    """
    si = self.sample(index, self.sizes)
    return [self.ranges[k][si[k]] for k in range(self.dim)]

  def sample(self, I, l):
    a = [0] * len(l)
    l = np.array(l)
    
    # initial case i = 0
    D, R = divmod(I, l[0])
    a[0] = int(R)
    I   -= R
    for i in range(1, len(l) - 1):
        D, R = divmod(I, cp(l[0:i+1]))
        a[i] = int(R / cp(l[0:i]))
        I -= R
    # last element case
    a[-1] = int(D)
    
    return a

class VirtualJointSolutions():
  """ Virtual container of all possible joint solutions
  
  Currently implemented for the 2P 3R robot
  Calculated on the fly.
  
  Main problem: joint configuration.
  Should I check it or can a joint configuration index result in a different
  configuration on different occasions?
  """
  def __init__(self, robot, trajectory_pt, scene=None):
    # path tolerances
    ranges = setup_ranges(trajectory_pt)
    # ik redundancy, use default joint limits
    q1 = np.linspace(0, 1, robot.ik_samples[0])
    q2 = np.linspace(0, 1, robot.ik_samples[1])
    ranges.append(q1)
    ranges.append(q2)
    # robot configurations
    ranges.append(np.array([0, 1]))
    self.ranges = ranges
    self.va = VirtualArray(ranges)
    self.size = self.va.total_size
    self.scene = scene
    self.robot = robot

  def __getitem__(self, index):
    data = self.va[index]
    pee = [data[0], data[1], data[2]] # end-effector pose
    qf  = [data[3], data[4]]          # fixed joint values
    jc  = int(data[5])                # joint configuration index
    sol = self.robot.ik_fixed_joints(pee, qf)
    if sol['success']:
      qs = sol['q']
      if jc == 0:
        if self.scene is not None:
          if self.robot.check_collision(qs[0], self.scene):
            return {'success': False}
        return {'success': True, 'q': qs[0]}
      elif jc == 1 and len(qs) > 1:
        if self.scene is not None:
          if self.robot.check_collision(qs[1], self.scene):
            return {'success': False}
        return {'success': True, 'q': qs[1]}
      else:
        return {'success': False}
    else:
      return {'success': False}
  
  def __len__(self):
    return self.size
