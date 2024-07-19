## Imports
import sys
sys.path.append('/home/theogoix/Documents/code/Games/Projet_Othello')
sys.path.append('/home/theogoix/Documents/code/Games/Projet_Othello/Othello_image')
import tkinter as tk
from functools import partial
from Othello_game import Othello
from Othello_AI import minimax,negamax,alphabeta,f_alphabeta,f_alphabeta2,Stab_Eval,Mat_Eval,Case_Eval,Complex_Eval,Frontier_Eval,Switch_Eval
import time

## Interface graphique


class Othello_board():
    def __init__(self,game):
        self.g = game
        self.canvas = tk.Tk()
        self.load_images()
        self.setup_canvas()
        self.refresh_board()
    # setup de la fenêtre

    def setup_canvas(self):
        self.setup_squares()
        self.setup_AI()
        self.setup_turn_counter()
        self.setup_passturn_button()
        self.setup_reverse_button()
        self.setup_score_displayer()
        self.setup_restart_button()

    # load images


    def load_images(self):
        self.empty_square_image = tk.PhotoImage(file = '/home/theogoix/Documents/code/Games/Projet_Othello/Othello_image/empty_square.png')
        self.black_pawn_image = tk.PhotoImage(file = '/home/theogoix/Documents/code/Games/Projet_Othello/Othello_image/black_pawn.png')
        self.white_pawn_image = tk.PhotoImage(file = '/home/theogoix/Documents/code/Games/Projet_Othello/Othello_image/white_pawn.png')
        self.possible_square_image = tk.PhotoImage(file = '/home/theogoix/Documents/code/Games/Projet_Othello/Othello_image/possible_square.png')
        self.AI_next_move_image = tk.PhotoImage(file = '/home/theogoix/Documents/code/Games/Projet_Othello/Othello_image/AI_next_move.png')


    # widgets à setup



    def setup_squares(self):
        self.square = [[tk.Button(self.canvas,height=100,width=100,bd = 0) for _ in range(8)] for _ in range(8)]
        for x in range(8):
            for y in range(8):
                self.square[x][y].grid(column=x,row=y)
                self.square[x][y].configure(command=partial(self.play_player_move,(x,y)))

    def setup_passturn_button(self):
        self.passturn_button = tk.Button(self.canvas,text='passturn',height=4,width=20,command=partial(self.play_player_move,(-1,-1)))
        self.passturn_button.grid(column=8,row=3)

    def setup_turn_counter(self):
        self.turn_counter = tk.Label(self.canvas,text=self.g.turn_count,height = 2)
        self.turn_counter.grid(column=8,row=4)

    def setup_reverse_button(self):
        self.reverse_button = tk.Button(self.canvas,text='undo move',command=self.playback_move)
        self.reverse_button.grid(column=8,row=7)


    def setup_score_displayer(self):
        self.score_displayer = tk.Label(self.canvas,text = 0, height = 2)
        self.score_displayer.grid(column=10,row=1)


    def setup_restart_button(self):
        self.restart_button = tk.Button(self.canvas, text = 'restart', command = self.restart_game)
        self.restart_button.grid(column = 8, row = 10)

    def restart_game(self):
        self.g.initialize()
        self.refresh_board()


    # setup de l'IA

    def setup_AI(self):
        self.setup_AI_help_button()
        self.setup_AI_eval_label()
        self.setup_AI_eval_label2()
        self.setup_AI_help_button2()
        self.setup_AI_timer()
        self.setup_AI_timer2()
        self.setup_AI_choose_depth()
        self.setup_AI_eval_funcs()
        self.setup_AI_player_choice()
        self.setup_AI_customizer()

    def setup_AI_help_button(self):
        self.AI_help_button = tk.Button(self.canvas,text = 'Hint ?',bg='black',fg = 'white',command=self.ask_black_AI)
        self.AI_help_button.grid(column=8,row=5)

    def setup_AI_help_button2(self):
        self.AI_help_button2 = tk.Button(self.canvas,text = 'Hint ?',bg='white',command=self.ask_white_AI)
        self.AI_help_button2.grid(column=8,row=6)


    def setup_AI_eval_label(self):
        self.AI_eval_label = tk.Label(self.canvas,text=0,height = 2)
        self.AI_eval_label.grid(column=8,row=0)

    def setup_AI_eval_label2(self):
        self.AI_eval_label2 = tk.Label(self.canvas,text=0, height = 2)
        self.AI_eval_label2.grid(column=8,row=1)

    def setup_AI_timer(self):
        self.AI_timer = tk.Label(self.canvas,height=2,width=20)
        self.AI_timer.grid(column=9,row=0)

    def setup_AI_timer2(self):
        self.AI_timer2 = tk.Label(self.canvas,height=2,width=20)
        self.AI_timer2.grid(column=9,row=1)

    def setup_AI_choose_depth(self):
        self.AI_depth = 10000
        self.AI_depth_var = tk.IntVar(self.canvas)
        self.AI_depth_var.set(self.AI_depth)
        self.AI_choose_depth = tk.OptionMenu(self.canvas,self.AI_depth_var,*[100,1000,10000,40000,100000],command = self.change_AI_depth)
        self.AI_choose_depth.grid(column = 12, row = 7)


    def setup_AI_choose_eval_func(self):
        self.AI_eval_func_key_var = tk.StringVar(self.canvas)
        self.AI_eval_func_key_var.set("Stab based")
        self.AI_choose_eval_func = tk.OptionMenu(self.canvas,self.AI_eval_func_key_var, *self.eval_func_list,
        command = self.select_eval_func)
        self.AI_choose_eval_func.grid(column = 11, row = 7)




    def change_AI_depth(self,depth):
        if self.black_is_under_custom:
            self.black_depth = depth
        else:
            self.white_depth = depth

    # AI eval funcs

    def setup_AI_eval_funcs(self):
        self.eval_func_dict = {}
        self.eval_func_list = []
        self.setup_stab_eval()
        self.setup_mat_eval()
        self.setup_case_eval()
        self.setup_frontier_eval()
        self.setup_switch_eval()
        self.setup_complex_eval()
        self.black_is_under_custom = True
        self.eval_func = self.stab_eval
        self.setup_AI_choose_eval_func()

    def setup_mat_eval(self):
        self.mat_eval = Mat_Eval(self.g).give_eval
        self.add_to_eval_func_dict("Materialistic",self.mat_eval)

    def setup_case_eval(self):
        self.case_eval = Case_Eval(self.g).give_eval
        self.add_to_eval_func_dict("Square based", self.case_eval)

    def setup_stab_eval(self):
        pond = [1,3,6,10]
        self.stab_eval = Stab_Eval(self.g,pond).give_eval
        self.add_to_eval_func_dict("Stab based", self.stab_eval)

    def setup_frontier_eval(self):
        self.frontier_eval = Frontier_Eval(self.g).give_frontier_eval
        self.add_to_eval_func_dict("Frontier",self.frontier_eval)

    def setup_switch_eval(self):
        self.switch_eval = Switch_Eval(self.g).give_eval
        self.add_to_eval_func_dict("Switch",self.switch_eval)


    def setup_complex_eval(self):
        self.complex_eval = Complex_Eval(self.g).give_eval
        self.add_to_eval_func_dict("Complex",self.complex_eval)

    def add_to_eval_func_dict(self,eval_func_key,eval_func):
        self.eval_func_list.append(eval_func_key)
        self.eval_func_dict[eval_func_key] = eval_func

    def select_eval_func(self,key):
        if self.black_is_under_custom:
            self.black_eval_func_key = key
            self.black_eval_func = self.eval_func_dict[key]
        else:
            self.white_eval_func_key = key
            self.white_eval_func = self.eval_func_dict[key]



    # Chose game mode


    def setup_AI_player_choice(self):
        self.setup_black_status_menu()
        self.setup_white_status_menu()
        self.initialize_to_player_status()

    def initialize_to_player_status(self):
        self.black_is_AI = False
        self.black_status_var.set("Human")
        self.white_is_AI = False
        self.white_status_var.set("Human")

    def setup_black_status_menu(self):
        self.black_status_var = tk.StringVar()
        self.black_status_menu = tk.OptionMenu(self.canvas,self.black_status_var,*["Human","AI"], command = self.update_black_status)
        self.black_status_menu.grid(row = 5, column = 9)

    def update_black_status(self,status):
        self.black_is_AI = (status == "AI")

    def setup_white_status_menu(self):
        self.white_status_var = tk.StringVar()
        self.white_status_menu = tk.OptionMenu(self.canvas,self.white_status_var,*["Human","AI"], command = self.update_white_status)
        self.white_status_menu.grid(row = 6, column = 9)

    def update_white_status(self,status):
        self.white_is_AI = (status == "AI")



    # AI customizer

    def setup_AI_customizer(self):
        self.initialize_AIs()
        self.create_AI_under_custom_menu()

    def initialize_AIs(self):
        self.black_eval_func = self.stab_eval
        self.black_eval_func_key = "Stab based"
        self.white_eval_func = self.stab_eval
        self.white_eval_func_key = "Stab based"
        self.black_depth = 10000
        self.white_depth = 10000

    def show_black_AI_custom(self):
        self.AI_eval_func_key_var.set(self.black_eval_func_key)
        self.AI_depth_var.set(self.black_depth)

    def show_white_AI_custom(self):
        self.AI_eval_func_key_var.set(self.white_eval_func_key)
        self.AI_depth_var.set(self.white_depth)


    def create_AI_under_custom_menu(self):
        self.AI_under_custom_var = tk.StringVar()
        self.AI_under_custom_var.set("Custom Black AI")
        self.AI_under_custom_dict = {"Custom Black AI" : True, "Custom White AI": False}
        self.AI_under_custom_menu = tk.OptionMenu(self.canvas, self.AI_under_custom_var, *['Custom Black AI','Custom White AI'],command = self.switch_AI_under_custom)
        self.AI_under_custom_menu.grid(row = 6, column = 11)

    def switch_AI_under_custom(self,AI_under_custom):
        if self.AI_under_custom_dict[AI_under_custom]:
            self.black_is_under_custom = True
            self.show_black_AI_custom()
        else:
            self.black_is_under_custom = False
            self.show_white_AI_custom()



    # interactions avec les widgets
    def play_player_move(self,move):
        if move in self.g.get_possible_moves():
            self.play_move(move)



    def play_move(self,move):
        self.g.play_move(move)
        self.refresh_board()
        self.canvas.update()
        self.demand_AI()

    def demand_AI(self):
        if not self.g.is_over():
            if self.g.get_cur_player() == 1:
                if self.black_is_AI:
                    self.ask_black_AI()
            else:
                if self.white_is_AI:
                    self.ask_white_AI()



    def ask_black_AI(self):
        debut = time.time()
        AI_eval,AI_best_move = f_alphabeta2(self.g,self.black_eval_func,self.black_depth)
        fin = time.time()
        self.AI_timer.configure(text=fin-debut)
        self.AI_eval_label.configure(text = AI_eval)
        self.apply_AI_move(AI_best_move)


    def ask_white_AI(self):
        debut=time.time()
        self.g.max_depth = 0
        self.g.depth = 0
        AI_eval,AI_best_move = f_alphabeta2(self.g,self.white_eval_func,self.white_depth)
        print(self.g.depth,self.g.max_depth)
        fin=time.time()
        self.AI_timer2.configure(text=fin-debut)
        self.AI_eval_label2.configure(text = AI_eval)
        self.apply_AI_move(AI_best_move)

    def apply_AI_move(self,move):
        self.show_recommandation(move)
        self.canvas.update()
        time.sleep(.5)
        self.play_move(move)



    def show_recommandation(self,move):
        x,y = move
        if (x,y) != (-1,-1):
            self.square[x][y].configure(image = self.AI_next_move_image)
        else:
            self.passturn_button.configure(bg='green2')

    def playback_move(self):
        if self.g.turn_count != 1:
            self.g.playback_move()
            self.refresh_board()


    # refresh tout

    def refresh_board(self):
        self.refresh_squares()
        self.refresh_passturn_button()
        self.refresh_turn_counter()
        self.refresh_score_displayer()

    # widgets à refresh

    def refresh_square(self,x,y):
        if self.g.get_cur_position((x,y)) == 1:
            photo = self.black_pawn_image
        elif self.g.get_cur_position((x,y)) == -1:
            photo = self.white_pawn_image
        elif (x,y) in self.g.get_possible_moves():
            photo = self.possible_square_image
        else:
            photo = self.empty_square_image
        self.square[x][y].configure(image = photo)

    def refresh_squares(self):
        for x in range(8):
            for y in range(8):
                self.refresh_square(x,y)

    def refresh_turn_counter(self):
        self.turn_counter.configure(text=self.g.turn_count)

    def refresh_passturn_button(self):
        if self.g.get_possible_moves() == [(-1,-1)]:
            color = 'yellow'
        else:
            color= 'white'
        self.passturn_button.configure(bg=color)

    def refresh_score_displayer(self):
        if not self.g.get_possible_moves():
            result = self.g.result()
            if result == 1:
                self.score = "Black player wins"
            elif result == -1:
                self.score = "White player wins"
            else:
                self.score = "Draw"
        else:
            player = self.g.get_cur_player()
            if player == 1:
                self.score = "Black player to move"
            else:
                self.score = "White player to move"
        self.score_displayer.configure( text = self.score + "     Score : {}-{}".format(*self.g.score()))



## Let's play !

def play():
    game=Othello()
    board=Othello_board(game)
    board.canvas.mainloop()

play()
