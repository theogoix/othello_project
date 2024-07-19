## Othello

class Othello:
    def __init__(self):
        self.initialize()

    # Initialize game

    def initialize(self):
        self.cur_position=[[0 for _ in range(8)] for _ in range(8)]
        for i in range(2):
            for j in range(2):
                self.cur_position[3+i][3+j]=(-1)**((i+j+1)%2)
        self.setup_list_squares()
        self.cur_player=1
        self.possible_moves = []
        self.set_possible_moves()
        self.turn_count = 1
        self.historic = [((-1,-1),[])]          # Une liste de (coup_joué,[case_modifiee_1,...,case_modifiee_n])

        self.depth = 0
        self.max_depth = 0

    # Setup list squares (order in which the possible moves would be displayed)

    def setup_list_squares(self):
        self.list_squares = [(0,0),(7,0),(0,7),(7,7),(0,3),(3,0),(0,4),(4,0),(3,7),(7,3),(4,7),(7,4),
                             (2,0),(0,2),(5,0),(0,5),(2,7),(7,2),(5,7),(7,5),(2,2),(2,5),(5,2),(5,5),
                             (2,3),(3,2),(2,4),(4,2),(3,5),(5,3),(4,5),(5,4),(1,0),(0,1),(6,0),(0,6),
                             (1,7),(7,1),(7,6),(6,7),(1,3),(3,1),(1,4),(4,1),(6,3),(3,6),(6,4),(4,6),
                             (1,2),(2,1),(1,5),(5,1),(2,6),(6,2),(5,6),(6,5),(1,1),(1,6),(6,1),(6,6)]
        self.corners = [(0,0),(0,7),(7,0),(7,7)]
        self.far_edges = [(0,3),(3,0),(0,4),(4,0),(3,7),(7,3),(4,7),(7,4)]
        self.mid_edges = [(0,2),(2,0),(0,5),(5,0),(2,7),(7,2),(5,7),(7,5)]
        self.close_edges = [(0,1),(1,0),(0,6),(6,0),(1,7),(7,1),(6,7),(7,6)]
        self.corners_middle_edge = [(1,1),(6,6),(1,6),(6,1)]
        self.close_middle_edge = [(1,2),(2,1),(1,5),(5,1),(6,2),(2,6),(5,6),(6,5)]
        self.far_middle_edge = [(1,3),(3,1),(1,4),(4,1),(6,3),(3,6),(4,6),(6,4)]
        self.corners_ext_center = [(2,2),(2,5),(5,2),(5,5)]
        self.edges_ext_center = [(3,2),(2,3),(4,5),(5,4),(4,2),(2,4),(5,3),(3,5)]
        self.centers = [(3,3),(3,4),(4,3),(4,4)]

    def get_list_squares(self):
        return self.list_squares

    # Get / Set

    def get_cur_player(self):
        return self.cur_player

    def change_cur_player(self):
        self.cur_player *= -1

    def get_cur_position(self,square):
        x,y=square
        if 0<=x<=7 and 0<=y<=7:
            return self.cur_position[x][y]
        else:
            return 2

    def set_cur_position(self,square,v):
        x,y = square
        self.cur_position[x][y]=v
        return

    def reverse_cur_position(self,square):
        x,y = square
        self.cur_position[x][y]  *= -1

    def get_possible_moves(self):
        return self.possible_moves[-1]

    def set_possible_moves(self):
        self.possible_moves.append(self.give_possible_moves())

    def del_possible_moves(self):
        self.possible_moves.pop()

    def get_turn_count(self):
        return self.turn_count

    def increase_turn_count(self):
        self.turn_count += 1

    def decrease_turn_count(self):
        self.turn_count -= 1

    def get_historic(self):
        return self.historic

    def add_to_historic(self,move,squares_changed):
        self.historic.append((move,squares_changed))

    # Check possible moves

    def is_valid_lign(self,square,dx,dy):
        x,y = square
        if self.get_cur_position((x+dx,y+dy)) != self.get_cur_player()*(-1):
            return False
        k=2
        while True:
            id_case = self.get_cur_position((x+k*dx,y+k*dy))
            if id_case == self.get_cur_player():
                return True
            elif id_case != self.get_cur_player()*(-1):
                return False
            else:
                k += 1



    def is_possible(self,move):
        if self.get_cur_position(move) != 0:
            return False

        d=((1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1))
        for dx,dy in d:
            if self.is_valid_lign(move,dx,dy):
                return True
        return False



    def give_possible_moves(self):
        available=[]
        for move in self.get_list_squares():
            if self.is_possible(move):
                available.append(move)
        if not available and self.get_historic()[-1][0] != (-1,-1):
            available.append((-1,-1))
        return available

    # Apply a move


    def change_lign(self,move,dx,dy):
        x,y = move
        change = True
        k=1
        while change:
            self.set_cur_position((x+k*dx,y+k*dy),self.get_cur_player())
            self.historic[-1][1].append((x+k*dx,y+k*dy))
            k+=1
            change = (self.get_cur_position((x+k*dx,y+k*dy)) == self.get_cur_player()*(-1))



    def apply_move(self,move):
        x,y = move
        self.historic.append((move,[]))
        if (x,y) != (-1,-1):
            self.set_cur_position(move,self.cur_player)
            d=((1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1))
            for dx,dy in d:
                if self.is_valid_lign(move,dx,dy):
                    self.change_lign(move,dx,dy)
        else:
            pass
        self.change_cur_player()
        self.increase_turn_count()

    # Play a move

    def play_move(self,move):
        self.apply_move(move)
        self.set_possible_moves()

    # Reverse a move

    def reverse_move(self):
        last_move,list_changed = self.historic.pop()
        if last_move != (-1,-1):
            self.set_cur_position(last_move,0)
            for square in list_changed:
                self.reverse_cur_position(square)
        self.change_cur_player()
        self.decrease_turn_count()

    def playback_move(self):
        self.del_possible_moves()
        self.reverse_move()


    # Endgame

    def is_over(self):
        return not self.get_possible_moves()

    def result(self):
        score = 0
        for x in range(8):
            for y in range(8):
                score += self.get_cur_position((x,y))
        if score > 0:
            return 1
        elif score == 0:
            return 0
        else:
            return -1

    def score(self):
        scores = [0,0]
        for x in range(8):
            for y in range(8):
                square_player = self.get_cur_position((x,y))
                if square_player == 1:
                    scores[0] += 1
                elif square_player == -1:
                    scores[1] +=1
                else:
                    pass
        return scores

    # Draw board (pour le debug)

    def draw_cur_state(self):
        for i in range(8):
            for j in range(8):
                print("{}|".format(self.cur_position[i][j]),end="")
            print()
