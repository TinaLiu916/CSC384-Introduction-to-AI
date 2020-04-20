#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = futoshiki_csp_model_1(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the Futoshiki puzzle.

1. futoshiki_csp_model_1 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only 
      binary not-equal constraints for both the row and column constraints.

2. futoshiki_csp_model_2 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only n-ary 
      all-different constraints for both the row and column constraints. 

'''
from cspbase import *
import itertools

def check_operator(a, op, b):
  if op == '>':
    return a > b
  elif op == '<':
    return a < b
  elif op == '.':
    return a != b

def futoshiki_csp_model_1(futo_grid):

  dom_size = int((len(futo_grid[0]) + 1) / 2)
  i = 0
  dom = []
  for i in range(dom_size):
    dom.append(i+1)

  vars = []
  var_size = dom_size*dom_size
  for i in range(var_size):
    var_index = i+1
    mod = var_index % dom_size
    if mod > 0:
      var_row = int(var_index / dom_size) + 1
      var_col = mod * 2 - 1
    else:
      var_row = int(var_index / dom_size)
      var_col = dom_size * 2 - 1
    if futo_grid[var_row-1][var_col-1] != 0:
      domm = [futo_grid[var_row-1][var_col-1]]
      vars.append(Variable('F{}'.format(i+1), domm))
    else:
      vars.append(Variable('F{}'.format(i+1), dom))
  

  cons = [] 
  for var in range(var_size):
    var_index = var+1
    mod = var_index % dom_size
    if mod > 0:
      var_row = int(var_index / dom_size) + 1
      var_col = mod * 2 - 1
    else:
      var_row = int(var_index / dom_size)
      var_col = dom_size * 2 - 1
    
    right_col = var_col + 1
    if right_col < dom_size * 2 - 1:
      if futo_grid[var_row-1][right_col-1] != '.':
        con = Constraint("C(F{},F{})".format(var_index,var_index+1),[vars[var_index-1], vars[var_index+1-1]])
        sat_tuples = []
        for t in itertools.product(dom, dom):
          if check_operator(t[0], futo_grid[var_row-1][right_col-1], t[1]):
            sat_tuples.append(t)
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)
  
    var_range = []
    small_num = (var_row - 1)*dom_size+1
    large_num = small_num + dom_size - 1
    small_num = var_index
    while small_num <= large_num:
      if small_num != var_index:
        var_range.append(small_num)
      small_num = small_num + 1
    for samerow in var_range:
      con = Constraint("C(F{},F{})".format(var_index,samerow),[vars[var_index-1], vars[samerow-1]])
      sat_tuples = []
      for t in itertools.product(dom, dom):   
        if check_operator(t[0], '.', t[1]):
          sat_tuples.append(t)
      con.add_satisfying_tuples(sat_tuples)
      cons.append(con)

    var_range = []
    if mod == 0:
      small_num = dom_size
    else:
      small_num = mod
    large_num = (dom_size - 1)*dom_size + small_num
    small_num = var_index
    while small_num <= large_num:
      if small_num != var_index:
        var_range.append(small_num)
      small_num = small_num + dom_size
    for samecol in var_range:
      con = Constraint("C(F{},F{})".format(var_index,samecol),[vars[var_index-1], vars[samecol-1]])
      sat_tuples = []
      for t in itertools.product(dom, dom):   
        if check_operator(t[0], '.', t[1]):
          sat_tuples.append(t)
      con.add_satisfying_tuples(sat_tuples)
      cons.append(con)
    var_array = []
    for i in range(dom_size):
      var_array.append([])
      for j in range(dom_size):
        var_array[i].append(vars[i*dom_size+j])

    csp = CSP("{}-Futoshiki".format(dom_size), vars)
    for c in cons:
        csp.add_constraint(c)
    
  return csp, var_array

def futoshiki_csp_model_2(futo_grid):

  dom_size = int((len(futo_grid[0]) + 1) / 2)
  i = 0
  dom = []
  for i in range(dom_size):
    dom.append(i+1)

  vars = []
  var_size = dom_size*dom_size
  for i in range(var_size):
    var_index = i+1
    mod = var_index % dom_size
    if mod > 0:
      var_row = int(var_index / dom_size) + 1
      var_col = mod * 2 - 1
    else:
      var_row = int(var_index / dom_size)
      var_col = dom_size * 2 - 1
    if futo_grid[var_row-1][var_col-1] != 0:
      domm = [futo_grid[var_row-1][var_col-1]]
      vars.append(Variable('F{}'.format(i+1), domm))
    else:
      vars.append(Variable('F{}'.format(i+1), dom))
  # print(vars)
  cons = [] 
  for var in range(var_size):
    var_index = var+1
    mod = var_index % dom_size
    if mod > 0:
      var_row = int(var_index / dom_size) + 1
      var_col = mod * 2 - 1
    else:
      var_row = int(var_index / dom_size)
      var_col = dom_size * 2 - 1
    
    right_col = var_col + 1
    if right_col < dom_size * 2 - 1:
      if futo_grid[var_row-1][right_col-1] != '.':
        con = Constraint("C(F{},F{})".format(var_index,var_index+1),[vars[var_index-1], vars[var_index+1-1]])
        sat_tuples = []
        for t in itertools.product(dom, dom):
          if check_operator(t[0], futo_grid[var_row-1][right_col-1], t[1]):
            sat_tuples.append(t)
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)

    if(mod == 1):
      var_range = []
      small_num = (var_row - 1)*dom_size+1
      large_num = small_num + dom_size - 1
      while small_num <= large_num:
        var_range.append(small_num)
        small_num = small_num + 1
      formatstring = "C("
      para_array = []
      for i in range(len(var_range)):
        if i == len(var_range)-1:
          formatstring = formatstring + "F{})"
        else:
          formatstring = formatstring + "F{},"
      for samerow in var_range:
        para_array.append(vars[samerow-1])

      con = Constraint(formatstring.format(*var_range),para_array)
      sat_tuples = []
      for t in itertools.permutations(dom):   
        sat_tuples.append(t)
      con.add_satisfying_tuples(sat_tuples)
      #print("---------row")
      #print(con)
      cons.append(con)

    if(var_index <= dom_size):
      var_range = []
      if mod == 0:
        small_num = dom_size
      else:
        small_num = mod
      large_num = (dom_size - 1)*dom_size + small_num
      while small_num <= large_num:
        var_range.append(small_num)
        small_num = small_num + dom_size

      formatstring = "C("
      para_array = []
      for i in range(len(var_range)):
        if i == len(var_range)-1:
          formatstring = formatstring + "F{})"
        else:
          formatstring = formatstring + "F{},"
      for samerow in var_range:
        para_array.append(vars[samerow-1])
      con = Constraint(formatstring.format(*var_range),para_array)
      sat_tuples = []
      for t in itertools.permutations(dom): 
        sat_tuples.append(t)
      con.add_satisfying_tuples(sat_tuples)
      #print("---------col")
      #print(con)
      cons.append(con)

    var_array = []
    for i in range(dom_size):
      var_array.append([])
      for j in range(dom_size):
        var_array[i].append(vars[i*dom_size+j])
 
    csp = CSP("{}-Futoshiki".format(dom_size), vars)
    for c in cons:
        csp.add_constraint(c)
    
  return csp, var_array
