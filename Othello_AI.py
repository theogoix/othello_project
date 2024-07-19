import sys
import sys
#sys.path.append('C:/Users/User/Documents/PythonProjets')
from Othello_game import Othello
import copy


## Eval Mat

class Mat_Eval:
    def __init__(self,g):
        self.g = g

    def give_eval(self):
        score = 0
        for x in range(8):
            for y in range(8):
                score += self.g.get_cur_position((x,y))
        return score * self.g.get_cur_player()


## Eval Case

class Case_Eval:
    def __init__(self,g,corner_value = 100, far_edge_value = 1, mid_edge_value = 5, close_edge_value = 5, corner_middle_edge_value = 0, close_middle_edge_value = 1, far_middle_edge_value = 1, corners_ext_center_value = 2,edges_ext_center_value = 2, center_value = 2):
        self.g = g
        self.corner_value = corner_value
        self.far_edge_value = far_edge_value
        self.mid_edge_value = mid_edge_value
        self.close_edge_value = close_edge_value
        self.corner_middle_edge_value = corner_middle_edge_value
        self.close_middle_edge_value = close_middle_edge_value
        self.far_middle_edge_value = far_middle_edge_value
        self.corners_ext_center_value = corners_ext_center_value
        self.edges_ext_center_value = edges_ext_center_value
        self.center_value = center_value
        self.create_square_status_dict()


    def create_square_status_dict(self):
        self.square_value_dict = {}
        for square in self.g.corners:
            self.square_value_dict[square] = self.corner_value
        for square in self.g.far_edges:
            self.square_value_dict[square] = self.far_edge_value
        for square in self.g.mid_edges:
            self.square_value_dict[square] = self.mid_edge_value
        for square in self.g.close_edges:
            self.square_value_dict[square] = self.close_edge_value
        for square in self.g.corners_middle_edge:
            self.square_value_dict[square] = self.corner_middle_edge_value
        for square in self.g.close_middle_edge:
            self.square_value_dict[square] = self.close_middle_edge_value
        for square in self.g.far_middle_edge:
            self.square_value_dict[square] = self.far_middle_edge_value
        for square in self.g.corners_ext_center:
            self.square_value_dict[square] = self.corners_ext_center_value
        for square in self.g.edges_ext_center:
            self.square_value_dict[square] = self.edges_ext_center_value
        for square in self.g.centers:
            self.square_value_dict[square] = self.center_value



    def give_eval(self):
        score = 0
        for x in range(8):
            for y in range(8):
                score += self.square_value_dict[(x,y)] * self.g.get_cur_position((x,y))
        return score * self.g.get_cur_player()


## Eval Stab

class Stab_Eval:
    def __init__(self,g,pond = [1,3,6,10]):
       self.g = g
       self.directions = [(1,0),(0,1),(1,1),(-1,1)]
       self.pond = pond
       self.player = self.g.get_cur_player()


    def give_square_value(self,square):
        if self.g.get_cur_position(square) == 0:
            return 0
        else:
            return self.pond[self.give_square_status(square)] * self.square_player



    def give_square_status(self,square):
        status = 3
        self.square_player = self.g.get_cur_position(square)
        for dir in self.directions:
            status = min(status,self.give_status_dir(square,dir))
        return status




    def give_status_way(self,square,dir):
        dx,dy = dir
        x,y = square
        while self.g.get_cur_position((x,y)) == self.square_player:
            x += dx
            y += dy
        return self.g.get_cur_position((x,y))

    def give_status_dir(self,square,dir):
        dx,dy = dir
        s = (self.give_status_way(square,(dx,dy)),self.give_status_way(square,(-dx,-dy)))
        if 2 in s:
            return 3
        elif s == (-self.square_player,-self.square_player):
            return 2
        elif -self.square_player in s:
            return 0
        else:
            return 1

    def give_eval(self):
        score = 0
        self.player = self.g.get_cur_player()
        for x in range(8):
            for y in range(8):
                score += self.give_square_value((x,y))
        return score * self.player

## Frontier Eval

class Frontier_Eval:
    def __init__(self,g,square_value = 9, empty_value = -1, friend_value = 0, opponent_value = 0, border_value = 1):
        self.g = g
        self.square_value = square_value
        self.give_value = {0 : empty_value, 1 : friend_value, -1 : opponent_value, 2 : border_value, -2 : border_value}
        self.delta = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]

    def give_frontier_eval(self):
        player = self.g.get_cur_player()
        score = 0
        for x in range(8):
            for y in range(8):
                square_player = self.g.get_cur_position((x,y))
                score += self.square_value * square_player
                for dx,dy in self.delta:
                    score += self.give_value[square_player * self.g.get_cur_position((x+dx,y+dy))]
        return score * player


## Complex Eval Func

class Complex_Eval:
    def __init__(self,g, death_penalty = -10, corner_bonus = 5):
        self.g = g
        self.delta = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        self.stab_eval = Stab_Eval(self.g,[1,3,6,10]).give_eval
        self.corner_dead = [((0,0),(1,1)),((0,7),(1,6)),((0,7),(1,6)),((7,7),(6,6))]
        self.corner_bonus = corner_bonus
        self.death_penalty = death_penalty

    def give_bonus(self):
        bonus = 0
        for corner,dead in self.corner_dead:
            if self.g.get_cur_position(corner) == 0:
                bonus += self.death_penalty * self.g.get_cur_position(dead)
            else:
                bonus += self.corner_bonus * self.g.get_cur_position(corner)
        return bonus * self.g.get_cur_player()

    def give_eval(self):
        return self.stab_eval() + self.give_bonus()


## Switch Eval

class Switch_Eval:
    def __init__(self,g,switch_turn = 32):
        self.g = g
        self.switch_turn = switch_turn
        self.case_eval = Case_Eval(self.g).give_eval
        self.stab_eval = Stab_Eval(self.g).give_eval

    def give_eval(self):
        if self.g.turn_count <= self.switch_turn:
            return self.case_eval()
        else:
            return self.stab_eval()



## Minimax

def minimax(g,eval_func,rem_depth):
    if rem_depth == 0:
        return [eval_func(g),(-1,-1)]
    else:
        id_player = g.get_cur_player()
        cur_minmax = [-1000,(-1,-1)]
        for move in g.get_possible_moves():
            g.play_move(move)
            new_minmax = [minimax(g,eval_func,rem_depth-1)[0] * id_player,move]
            cur_minmax = max(new_minmax,cur_minmax)
            g.reverse_move()
        cur_minmax[0] *= id_player
        return cur_minmax

## Negamax

def negamax(g,eval_func,rem_depth):
    if rem_depth == 0:
        return [eval_func(g),(-1,-1)]
    else:
        best_move = [-1000,(-1,-1)]
        for move in g.get_possible_moves():
            g.play_move(move)
            best_move = max(best_move,[-negamax(g,eval_func,rem_depth-1)[0],move])
            g.reverse_move()
        return best_move

## Nega Alpha Beta

def neg_alphabeta(g,eval_func,rem_depth,cur_best):
    if rem_depth == 0:
        return [eval_func(g),(-1,-1)]
    else:
        best_move=[-255,(-1,-1)]
        for move in g.get_possible_moves():
            g.play_move(move)
            best_move = max(best_move,[-alphabeta(g,eval_func,rem_depth-1,best_move[0])[0],move])
            g.reverse_move()
            if -best_move[0] <= cur_best:
                return best_move
        return best_move

## AlphaBeta

def alphabeta(g,eval_func,rem_depth,cur_best):
    if rem_depth == 0:
        return [eval_func(),(-1,-1)]

    g.set_possible_moves()
    if g.is_over():
        g.del_possible_moves()
        return [10000 * g.result() * g.get_cur_player(),(-1,-1)]

    else:
        best_move=[-10000,(-1,-1)]
        for move in g.get_possible_moves():
            g.apply_move(move)
            best_move = max(best_move,[-alphabeta(g,eval_func,rem_depth-1,best_move[0])[0],move])
            g.reverse_move()
            if -best_move[0] <= cur_best:
                g.del_possible_moves()
                return best_move
        g.del_possible_moves()
        return best_move

## Formated alphabeta

def f_alphabeta(g,eval_func,max_depth):
    return alphabeta(g,eval_func,max_depth,-10000)

## New alphabeta

def f_alphabeta2(g,eval_func,max_depth):
    return alphabeta2(g,eval_func,max_depth,-10000)


def alphabeta2(g,eval_func,rem_depth,cur_best):
    g.max_depth = max(g.depth,g.max_depth)
    if rem_depth == 0:
        return [eval_func(),(-1,-1)]

    g.set_possible_moves()
    if g.is_over():
        g.del_possible_moves()
        return [10000 * g.result() * g.get_cur_player(),(-1,-1)]

    else:
        best_move=[-10000,(-1,-1)]
        new_depth = rem_depth // len(g.get_possible_moves())
        for move in g.get_possible_moves():
            g.apply_move(move)
            g.depth +=1
            best_move = max(best_move,[-alphabeta2(g,eval_func,new_depth,best_move[0])[0],move])
            g.depth -=1
            g.reverse_move()
            if -best_move[0] <= cur_best:
                g.del_possible_moves()
                return best_move
        g.del_possible_moves()
        return best_move