#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os #for time functions
from search import * #for search engines
from sokoban import SokobanState, Direction, PROBLEMS #for Sokoban specific classes and problems

def sokoban_goal_state(state):
  '''
  @return: Whether all boxes are stored.
  '''
  for box in state.boxes:
    if box not in state.storage:
      return False
  return True

def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #We want an admissible heuristic, which is an optimistic heuristic.
    #It must never overestimate the cost to get from the current state to the goal.
    #The sum of the Manhattan distances between each box that has yet to be stored and the storage point nearest to it is such a heuristic.
    #When calculating distances, assume there are no obstacles on the grid.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.
    heur_man_dis = 0
    for box_pos in state.boxes:
      old_distance = 1000
      for obj_pos in state.storage:
        new_distance = abs(box_pos[0]- obj_pos[0]) + abs(box_pos[1]- obj_pos[1])
        if(new_distance < old_distance):
          old_distance = new_distance
      heur_man_dis = heur_man_dis + old_distance

    return heur_man_dis


#SOKOBAN HEURISTICS
def trivial_heuristic(state):
  '''trivial admissible sokoban heuristic'''
  '''INPUT: a sokoban state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''
  count = 0
  for box in state.boxes:
    if box not in state.storage:
        count += 1
  return count

def heur_alternate(state):
#IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #heur_manhattan_distance has flaws.
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.

    #Calculate robot to box manhattan distance
    dis = 0
    for box in state.boxes:
      old_distance = float('inf')
      for robot in state.robots:
        new_distance = abs(box[0]- robot[0]) + abs(box[1]- robot[1])
        if(new_distance < old_distance):
          old_distance = new_distance
      dis = dis + old_distance

    #Check if there is obtacles or boxes just beside any unstored boxes
    for box in state.boxes:
      old_distance = float('inf')
      if box not in state.storage:
        for storage in state.storage:
          new_distance = abs(box[0]- storage[0]) + abs(box[1]- storage[1])
          for obj in state.obstacles:
            if abs(storage[0] - obj[0]) < abs(box[0]- storage[0]) and box[1] == obj[1]:
              new_distance = new_distance + 1
            elif abs(storage[1] - obj[1]) < abs(box[1]- storage[1]) and box[0] == obj[0]:
              new_distance = new_distance + 1
          for box2 in state.boxes:
            if abs(storage[0] - box2[0]) < abs(box[0]- storage[0]) and box[1] == box2[1]:
              new_distance = new_distance + 1
            elif abs(storage[1] - box2[1]) < abs(box[1]- storage[1]) and box[0] == box2[0]:
              new_distance = new_distance + 1
          if(new_distance < old_distance):
            old_distance = new_distance
        dis = dis + old_distance
  
    #Check if the box is at the cornor or on the edge where there is no storage point along the edge.
    for box in state.boxes:
      if (box[0] == 0) or (box[0] == state.width - 1):
        a = box[0]
        b = box[1] + 1
        c = box[1] - 1
        if (box[1] == 0) or (box[1] == state.height - 1):
          if box not in state.storage:
            return dis + float('inf')
        elif ((a,b)in state.obstacles) or ((a,c)in state.obstacles):
            if box not in state.storage:
              return dis + float('inf')
        else:
          found = False
          for storage in state.storage:
              if box[0] == storage[0]:
                found = True
                break 
          if(found != True):
            if box not in state.storage:
              return dis + float('inf')
      elif (box[1] == 0) or (box[1] == state.height - 1):
        a = box[1]
        b = box[0] + 1
        c = box[0] - 1
        if ((b,a)in state.obstacles) or ((c,a)in state.obstacles):
          if box not in state.storage:
            return dis + float('inf')
        else:
          found = False
          for storage in state.storage:
              if box[1] == storage[1]:
                found = True
                break 
          if(found != True):
            if box not in state.storage:
              return dis + float('inf')

    return dis

def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    return sN.gval+sN.hval*weight

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 10):
#IMPLEMENT
  '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''
  cost_bound = [float('inf'),float('inf'),0]
  final_result = False
  se = SearchEngine('custom')
  wapped_fval_function = (lambda sN: fval_function(sN, weight))
  se.init_search(initial_state, sokoban_goal_state, heur_fn, wapped_fval_function)

  cur_time = os.times()[0]
  stop_time = cur_time + timebound
  time_left = stop_time - cur_time
  old_cost = se.search(timebound)
  if old_cost:
    cost_bound[2] = old_cost.gval
    final_result = old_cost

  while (time_left > 0):
    cur_time = os.times()[0]
    time_left = stop_time - cur_time
    new_cost = se.search(time_left,cost_bound)
    if new_cost:
      if new_cost.gval < old_cost.gval:
        cost_bound[2] = new_cost.gval
        final_result = new_cost
      else:
        if(weight > 1):
          weight = weight/1.1
        else:
          weight = 2

  return final_result

def anytime_gbfs(initial_state, heur_fn, timebound = 10):
#IMPLEMENT
  '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''

  cost_bound = [0,float('inf'),float('inf')]
  final_result = False
  se = SearchEngine('best_first')
  se.init_search(initial_state, sokoban_goal_state, heur_fn)

  cur_time = os.times()[0]
  stop_time = cur_time + timebound
  
  time_left = stop_time - cur_time
  old_cost = se.search(timebound)
  if old_cost:
    cost_bound[0] = old_cost.gval
    final_result = old_cost

  while (time_left > 0):
    cur_time = os.times()[0]
    time_left = stop_time - cur_time
    new_cost = se.search(time_left,cost_bound)

    if new_cost:
      if new_cost.gval < old_cost.gval:
        cost_bound[0] = new_cost.gval
        final_result = new_cost

  return final_result
