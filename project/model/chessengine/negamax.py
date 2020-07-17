#!/usr/bin/env python
# -*- coding: utf-8 -*-

# node must be an object with the methods all_possible_nodes(self, color) and evaluate(self, color) 
# implemented.
#
# all_possible_nodes(self, color) should return a list of all possible nodes depending on 
# the value of color. color can be either 1 or -1 (player A or player B).
#
# evaluate(self) returns a number which is the nodes (heuristic) score, looking at it
# from the color==1 (player A) point of view.
#
# Move Ordering can be implemented in the all_possible_nodes(self, color) method at users
# discretion.



INF = 1000000.0


# NEGAMAX
#
# Initial call for player A's root node: 
# root_negamax_value, principal_variation = negamax(root_node, depth, 1)
#
# Initial call for player B's root node: 
# root_negamax_value, principal_variation = negamax(root_node, depth, -1)

def negamax(node, depth, color):

#   If search depth is reached or if there are no child nodes, return the
#   evaluation value of this node, and the node itself in a list. The latter
#   will construct the principal variation.

    if depth == 0:
        variation = []
        variation.append(node)
        return color * node.evaluate_node(), variation
    else:
        
        child_nodes = node.all_possible_nodes(color)
        
        if len(child_nodes) == 0:
            variation = []
            variation.append(node)
            return color * node.evaluate_node(), variation

    best_value = -INF
    for child in child_nodes:
        negated_candidate_value, candidate_variation = negamax(child, depth-1, -color)
        candidate_value = -negated_candidate_value

        if candidate_value > best_value:
            best_value = candidate_value
            principal_variation = candidate_variation

#   Return the best evaluation value, and insert the node that produced that value
#   first in the principal variation list.

    principal_variation.insert(0, node)
    return best_value, principal_variation





# ALPHABETA
#
# Initial call for player A's root node: 
# root_negamax_value, principal_variation = negamax(root_node, depth, -INF, INF, 1)
#
# Initial call for player B's root node: 
# root_negamax_value, principal_variation = negamax(root_node, depth, -INF, INF, -1)

def alphabeta(node, depth, alpha, beta, color, preferred_node = None, first_iteration = True):

#   If search depth is reached or if there are no child nodes, return the
#   evaluation value of this node, and the node itself in a list. The latter
#   will construct the principal variation.

    if depth == 0:
        variation = []
        variation.append(node)
        return color * node.evaluate_node(), variation

    else:
        
        child_nodes = node.all_possible_nodes(color)

        if first_iteration and preferred_node != None:
            

            #print child_nodes
            #print preferred_node
            
            child_nodes.remove(preferred_node)
            child_nodes.insert(0, preferred_node)
            
#            child_nodes.insert(0, preferred_node)       # This actually duplicates the preferred node :(


        if len(child_nodes) == 0:
            variation = []
            variation.append(node)
            return color * node.evaluate_node(), variation

    best_value = -INF
    for child in child_nodes:
        negated_candidate_value, candidate_variation = alphabeta(child, depth-1, 
                -beta, -alpha, -color, preferred_node = None, first_iteration = False)
        candidate_value = -negated_candidate_value

        if candidate_value > best_value:
            best_value = candidate_value
            principal_variation = candidate_variation

        alpha = max(alpha, best_value)
        if alpha >= beta:
            break

#   Return the best evaluation value, and insert the node that produced that value
#   first in the principal variation list.

    #print 'ab: returned value: ' + str(best_value)

    principal_variation.insert(0, node)
    return best_value, principal_variation










class Transposition_Table(object):

    def __init__(self):

        self._key_mask = 0b11111111111111111111
        self._table = [ [None, None] ] * (2 ** 20)

    @property
    def table(self):
        return self._table

    @property
    def key_mask(self):
        return self._key_mask

    def hash_key(self, node):
        return node.zobrist_number & self.key_mask


    def insert(self, node, time_stamp = None):
        self.table[self.hash_key(node)][0] = node


    def retrieve(self, node):
        possible_entries = self.table[self.hash_key(node)]  # This is a list of len(2)
        
        if possible_entries[0] == None:
            return None
        elif possible_entries[0].zobrist_number == node.zobrist_number:
            return possible_entries[0]
        else:
            return None

            


        



class PV_Table(object):

    def __init__(self):

        self._table = [None] * (2 ** 20)

    def insert(self, index, pv_list):
        self._table[index] = pv_list

    def retrieve(self, index):
        return self._table[index]











EXACT = 1
LOWERBOUND = 2
UPPERBOUND = 3

class Transposition_Table_Node(object):

    def __init__(self, zobrist_number = 0, depth = 0, value = 0, flag = 0, time_stamp = 0):
        self.zobrist_number = zobrist_number
        self.depth = depth
        self.value = value
        self.flag = flag
        self.time_stamp = time_stamp



transposition_table = Transposition_Table()
pv_table = PV_Table()





# ALPHABETA with TRANSPOSITION TABLE and PRINCIPAL VARIATION TABLE
#
# Initial call for player A's root node: 
# root_negamax_value, principal_variation = negamax(root_node, depth, -INF, INF, 1, preferred_move)
#
# If no first node is preferred, just leave it out.
#
# Initial call for player B's root node: 
# root_negamax_value, principal_variation = negamax(root_node, depth, -INF, INF, -1)


def alphabetamemory(node, depth, alpha, beta, color, preferred_node = None, first_iteration = True):
    
    #global transposition_table

    original_alpha = alpha

    tt_entry = transposition_table.retrieve( node )
    
    #if False:
    if tt_entry != None:

#        print 'tt_entry is not None'
        if tt_entry.depth >= depth:

#            print 'depth'
            if tt_entry.flag == EXACT:
                #print 'exact'
                #variation = []
                #variation.append(node)
                return tt_entry.value, pv_table.retrieve(transposition_table.hash_key(node)) 

            elif tt_entry.flag == LOWERBOUND:
#                print 'lowerbound'
                alpha = max(alpha, tt_entry.value)

            elif tt_entry.flag == UPPERBOUND:
#                print 'upperbound'
                beta = min(beta, tt_entry.value)

            if alpha >= beta:
                #print 'alpha >= beta'
                #variation = []
                #variation.append(node)
                return tt_entry.value, pv_table.retrieve(transposition_table.hash_key(node))

    if depth == 0:
        #print 'depth is zero'

        return color * node.evaluate_node(), [ node ]

    child_nodes = node.all_possible_nodes(color)
    
    if len(child_nodes) == 0:
        #print 'terminal node'

        return color * node.evaluate_node(), [ node ]
        

    if first_iteration and preferred_node != None:
        
        child_nodes.remove(preferred_node)
        child_nodes.insert(0, preferred_node)


    best_value = -INF
    
    # Some ordering of the moves here

    for child in child_nodes:
        negated_candidate_value, candidate_variation = alphabetamemory(child, depth-1, -beta, -alpha, -color)
        candidate_value = -negated_candidate_value

        if candidate_value > best_value:
            best_value = candidate_value

            principal_variation = candidate_variation
            #pv_table.insert(node.hash_)


        alpha = max(alpha, best_value)
        if alpha >= beta:
            #print 'Cutoff!!!'
            break

    new_entry = Transposition_Table_Node()

    new_entry.value = best_value

    if best_value <= original_alpha:
        new_entry.flag = UPPERBOUND
    elif best_value >= beta:
        new_entry.flag = LOWERBOUND
    else:
        new_entry.flag = EXACT

    new_entry.depth = depth

    new_entry.zobrist_number = node.zobrist_number

    transposition_table.insert( new_entry )

    principal_variation.insert(0, node)

    pv_table.insert(transposition_table.hash_key(node), principal_variation)

    return best_value, principal_variation





# ITERATIVE DEEPENING, with or without memory.
#
# Initial call for player A's root node: 
# root_iterdeep_value, principal_variation = iterativedeepening(max_depth, WHITE)
#
#
# Initial call for player B's root node: 
# root_iterdeep_value, principal_variation = iterativedeepening(max_depth, BLACK)


def iterativedeepeningalphabeta(node, max_depth, color):   

    for i in range(2, max_depth + 1):
        
        # First guess

        score, principal_variation = alphabeta(node, i-1, -INF, INF, color)

        # Now deepen the search

        score, principal_variation = alphabeta(node, i, -INF, INF, color, 
                preferred_node = principal_variation[1])

    return score, principal_variation



def iterativedeepeningalphabetamemory(node, max_depth, color):  

    for i in range(2, max_depth + 1):

        # First guess

        score, principal_variation = alphabetamemory(node, i-1, -INF, INF, color)

        # Deepen search

        score, principal_variation = alphabetamemory(node, i, 
                -INF, INF, color, preferred_node = principal_variation[1])

    return score, principal_variation






def mtdf(node, depth, color, first_guess = 0.0):

    guess = first_guess
    upperbound = INF
    lowerbound = -INF

    #value, principal_variation = alphabetamemory(node, 1, -INF, INF, color)

    while lowerbound < upperbound:
        if guess == lowerbound:
            beta = guess + 1
        else:
            beta = guess
        guess, principal_variation = alphabetamemory(node, depth, beta - 1, beta, color) #, preferred_node = principal_variation[1])
        if guess < beta:
            upperbound = guess
        else:
            lowerbound = guess

    return guess, principal_variation





def iterativedeepeningmtdf(node, depth, color):     # Wait with this one.

    first_guess = 0.0
    guess = first_guess

    for i in range(2, depth + 1):
        guess, principal_variation = mtdf(node, depth, color, guess)

    return guess, principal_variation




#function iterative_deepening(root : node_type) : integer;
# 
#      firstguess := 0;
#      for d = 1 to MAX_SEARCH_DEPTH do
#            firstguess := MTDF(root, firstguess, d);
#            if times_up() then break;
#      return firstguess;



#function MTDF(root : node_type; f : integer; d : integer) : integer;
#      g := f;
#      upperbound := +INFINITY;
#      lowerbound := -INFINITY;
#      repeat
#            if g == lowerbound then beta := g + 1 else beta := g;
#            g := AlphaBetaWithMemory(root, beta - 1, beta, d);
#            if g < beta then upperbound := g else lowerbound := g;
#      until lowerbound >= upperbound;
#      return g;





