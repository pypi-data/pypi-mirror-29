#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Function to define and proccess robot end-effector paths.
"""

import numpy as np
from matplotlib.patches import Wedge
from ppr.cpp.graph import Graph

class TolerancedNumber:
    """ A range on the numner line used to define path constraints
    
    It also has a nominal value in the range which can be used in cost
    functions of some sort in the future. For example, if it is preffered
    that the robot end-effector stays close to an optimal pose, but can
    deviate if needed to avoid collision.
    
    Attributes
    ----------
    n : float
        Nominal / preffered value for this number
    u : float
        Upper limit.
    l : float
        lower limit
    s : int
        Number of samples used to produce descrete version of this number.
    range : numpy.ndarray of float
        A sampled version of the range on the number line, including limits.
        The nominal value is not necessary included.
    
    Notes
    -----
    Sampling for orientation is done uniformly at the moment.
    In 3D this is no good and special sampling techniques for angles should be
    used.
    The sampled range is now an attribute, but memory wise it would be better
    if it is a method. Then it is only descritized when needed.
    But it the number of path points will probably be limited so I preffer this
    simpler implementation for now.
    """
    def __init__(self, nominal, lower_bound, upper_bound, samples=10):
        """ Create a toleranced number
        
        Nominal does not have to be in the middle,
        it is the preffered value when we ever calculate some kind of cost.
        
        Parameters
        ----------
        nominal : float
            Nominal / preffered value for this number
        lower_bound : float
        upper_bound : float
        samples : int
            The number of samples taken when a sampled version of the number
            is returned in the range attribute. (default = 10)
        
        Examples
        --------
        >>> a = TolerancedNumber(0.7, 0.0, 1.0, samples = 6)
        >>> a.range
        array([ 0. ,  0.2,  0.4,  0.6,  0.8,  1. ])
        """
        if nominal < lower_bound or nominal > upper_bound:
            raise ValueError("nominal value must respect the bounds")
        self.n = nominal
        self.u = upper_bound
        self.l = lower_bound
        self.s = samples
        self.range = np.linspace(self.l, self.u, self.s)

class TrajectoryPt:
    """ Trajectory point for a desired end-effector pose in cartesian space
    
    This object bundles the constraints on the end-effector for one point
    of a path.
    
    Attributes
    ----------
    dim : int
        Pose dimensions, 3 for 2D planning, 6 for 3D planning.
    p : list of numpy.ndarray of float or ppr.path.TolerancedNumber
        Pose constraints for the end-effector (x, y, orientation).
        Can be a fixed number (a float) or a TolerancedNumber
    hasTolerance : list of bool
        Indicates which elements of the pose are toleranced (True) and
        fixed (False).
    p_nominal : list of float
        Same as p for fixed poses, the nominal value for a TolerancedNumber.
    timing : float
        Time in seconds it should be executed relative to the previous path
        point. Not used in current version.
    
    Examples
    --------
    Create a trajectory point at position (1.5, 3.1) with a symmetric
    tolerance of 0.4 on the x position.
    The robot orientation should be between 0 and pi / 4.
    (No preffered orientation, so assumed in the middle, pi / 8)

    >>> x = TolerancedNumber(1.5, 1.0, 2.0)
    >>> y = 3.1
    >>> angle = TolerancedNumber(np.pi / 8, 0.0, np.pi / 4)
    >>> tp = TrajectoryPt([x, y, angle])
    >>> tp.p_nominal
    [1.5, 3.1, 0.39269908169872414]
    
    A path is created by putting several trajectory points in a list.
    For example a vertical path with tolerance along the x-axis:
    
    >>> path = []
    >>> path.append(TrajectoryPt([TolerancedNumber(1.5, 1.0, 2.0), 0.0, 0]))
    >>> path.append(TrajectoryPt([TolerancedNumber(1.5, 1.0, 2.0), 0.5, 0]))
    >>> path.append(TrajectoryPt([TolerancedNumber(1.5, 1.0, 2.0), 1.0, 0]))
    >>> for p in path: print(p)
    [1.5, 0.0, 0]
    [1.5, 0.5, 0]
    [1.5, 1.0, 0]
    """
    def __init__(self, pee):
        """ Create a trajectory point from a given pose
        
        [x_position, y_position, angle last joint with x axis]
        
        Parameters
        ----------
        pee : list or numpy.ndarray of float or ppr.path.TolerancedNumber
            Desired pose of the end-effector for this path point,
            every value can be either a float or a TolerancedNumber
        """
        self.dim = len(pee)
        self.p = pee
        self.hasTolerance = [isinstance(pee[i], TolerancedNumber) for i in range(self.dim)]
        self.p_nominal = []
        for i in range(self.dim):
            if self.hasTolerance[i]:
                self.p_nominal.append(self.p[i].n)
            else:
                self.p_nominal.append(self.p[i])
        self.timing = 0.1 # with respect to previous point
    
    def __str__(self):
        """ Returns string representation for printing
        
        Returns
        -------
        string
            List with nominal values for x, y and orientation.
        """
        return str(self.p_nominal)

    def plot(self, axes_handle, show_tolerance=True):
        """ Visualize the path on given axes
        
        Parameters
        ----------
        axes_handle : matplotlib.axes.Axes
        show_tolerance : bool
            If True, the range for a TolerancedNumber is showed.
            A bar for x or y position, A wedge for orientation tolerance.
            (default True)
        """
        pn = self.p_nominal
        axes_handle.plot(pn[0], pn[1], 'k*')
        if show_tolerance:
            if self.hasTolerance[0]:
                do = -self.p[0].l + pn[0]
                du =  self.p[0].u - pn[0]
                axes_handle.errorbar(pn[0], pn[1], xerr=[[do], [du]], color=(0.5, 0.5, 0.5))
            if self.hasTolerance[1]:
                do = -self.p[1].l + pn[1]
                du =  self.p[1].u - pn[1]
                axes_handle.errorbar(pn[0], pn[1], yerr=[[do], [du]], color=(0.5, 0.5, 0.5))
            if self.hasTolerance[2]:
                # scale radius relative to trajectory point position
                radius = (pn[0] + pn[1]) / 20
                do = self.p[2].l * 180 / np.pi
                du = self.p[2].u * 180 / np.pi
                arc = Wedge((pn[0], pn[1]), radius, do, du, facecolor=(0.5, 0.5, 0.5, 0.5))
                axes_handle.add_patch(arc)

def create_grid(r):
    """ Create an N dimensional grid from N arrays
    
    Based on N lists of numbers we create an N dimensional grid containing
    all possible combinations of the numbers in the different lists.
    An array can also be a single float if their is now tolerance range.
    
    Parameters
    ----------
    r : list of numpy.ndarray of float
        A list containing numpy vectors (1D arrays) representing a sampled
        version of a range along an axis.
    
    Returns
    -------
    numpy.ndarray
        Array with shape (M, N) where N is the number of input arrays and
        M the number of different combinations of the data in the input arrays.
    
    Examples
    --------
    >>> a = [np.array([0, 1]), np.array([1, 2, 3]), 99]
    >>> create_grid(a)
    array([[ 0,  1, 99],
           [ 1,  1, 99],
           [ 0,  2, 99],
           [ 1,  2, 99],
           [ 0,  3, 99],
           [ 1,  3, 99]])
    """
    grid = np.meshgrid(*r)
    grid = [ grid[i].flatten() for i in range(len(r)) ]
    grid = np.array(grid).T
    return grid

def discretise(pt):
    """ Returns a discrete version of the range of a trajectory point
    
    Based on the sampled range in the Toleranced Numbers, a 3 dimensional grid
    representing end-effector poses that obey the trajectory point constraints.
    
    Parameters
    ----------
    pt : ppr.path.TrajectoryPt
    
    Returns
    -------
    numpy.ndarray
        Array with shape (M, 3) containing M possible poses for the robot
        end-effector that  obey the trajectory point constraints.
    
    Examples
    --------
    >>> x = TolerancedNumber(1, 0.5, 1.5, samples=3)
    >>> y = TolerancedNumber(0, -1, 1, samples=2)
    >>> pt = TrajectoryPt([x, y, 0])
    >>> discretise(pt)
    array([[ 0.5, -1. ,  0. ],
           [ 1. , -1. ,  0. ],
           [ 1.5, -1. ,  0. ],
           [ 0.5,  1. ,  0. ],
           [ 1. ,  1. ,  0. ],
           [ 1.5,  1. ,  0. ]])
    """
    r = []
    for i in range(pt.dim):
        if pt.hasTolerance[i]:
            r.append(pt.p[i].range)
        else:
            r.append(pt.p[i])
    grid = create_grid(r)
    return grid

def cart_to_joint(robot, traj_points, check_collision = False, scene=None):
    """ Convert a path to joint space by descretising and ik.
    
    Every trajectory point in the path is descretised, then for all these
    poses the inverse kinematics are solved.
    
    Parameters
    ----------
    robot : ppr.robot.Robot
    traj_points : list of ppr.path.TrajectoryPt
    check_collision : bool
        If True, a joint solution is only accepted if it does not collide
        with the objects in the scene. (default false)
        Self collision is not checked but assumed to be ensured by the joint
        limits.
    scene : list of ppr.geometry.Rectangle
        A list of objects with which the robot could collide.
    
    Returns
    -------
    list of numpy.ndarray of floats
        A list of arrays with shape (M, ndof) representing possible joint
        positions for every trajectory point.
        The arrays in this list could be very big!
    """
    # input validation
    if check_collision:
        if scene == None:
            raise ValueError("scene is needed for collision checking")
    
    # get discrete version of trajectory points
    cart_traj = []
    for pt in traj_points:
        cart_traj.append(discretise(pt))

    # solve inverse kinematics for every samples traj point
    # I could add some print statements to have info on unreachable points
    joint_traj = []
    for cart_vec in cart_traj:
        qi = []
        for cart_pt in cart_vec:
            sol = robot.ik(cart_pt)
            if sol['success']:
                for qsol in sol['q']:
                    if check_collision:
                        if not robot.check_collision(qsol, scene):
                            qi.append(qsol)
                    else:
                        qi.append(qsol)
        joint_traj.append(np.array(qi))
    return joint_traj

def get_shortest_path(Q):
    """ Calculate the shortest path from joint space data
    
    When the path with trajectory points is converted to joint space,
    this data can be used to construct a graph and look for the shortest path.
    The current distance metrix is the l1-norm of joint position difference
    between two points.
    
    I still have to implement maximum joint movement and acceleration limits.
    So technically this will always find a shortest path for now.
    
    Parameters
    ----------
    Q : list of nympy.ndarrays of float
        A list with the possible joint positions for every trajectory point
        along a path.
    
    Returns
    -------
    dict
        A dictionary with a key 'success' to indicate whether a path was found.
        If success is True, then the key 'path' contains a list with the joint
        position for every trajectory point that gives the shortest path.
    
    Notes
    -----
    I have a problem with swig type conversions. Therefore the type of the
    input data is checked and changed from float64 to float32.
    """
    Q = _check_dtype(Q)

    n_path = len(Q)
    # initialize graph
    g = Graph()
    for c in Q:
        if len(c) == 0:
            # one of the trajectory points is not reachable
            return {'success': False}
        g.add_data_column(c)
    g.init_dijkstra()

    # run shortest path algorithm
    g.run_dijkstra()

    # print result
    # g.print_graph()
    g.print_path()

    # get joint values for the shortest path
    p_i = g.get_path(n_path)
    print(p_i)

    if p_i[0] == -1:
        return {'success': False}
    else:
        res = []
        for k, i in zip(range(n_path), p_i):
            # TODO ugly all the "unsave" typecasting
            qki = Q[k][i].astype('float64')
            res.append(qki)
        
        return {'success': True, 'path': res}

def _check_dtype(Q):
    """ Change type if necessary to float32
    
    Due to an unresolved issue with swig and numpy, I have to convert the type.
    
    Parameters
    ----------
    Q : list of nympy.ndarrays of float
        A list with the possible joint positions for every trajectory point
        along a path.
    
    Returns
    -------
    list of nympy.ndarrays of float32
    """
    if Q[0].dtype != 'float32':
        print("converting type of Q")
        for i in range(len(Q)):
            Q[i] = Q[i].astype('float32')
    
    return Q
