import math 

"""
Funcția heuristică utilizată pentru evaluarea stărilor în jocul Țintar (Nine Men's Morris) este concepută pentru a estima cât de favorabilă este o configurație a tablei pentru jucătorul MAX ('x'). 
Aceasta combină mai mulți factori considerați esențiali pentru succes în acest joc:

    Diferența de Piese: Cel mai fundamental factor este numărul de piese pe tablă. A avea mai multe piese decât adversarul oferă mai multe opțiuni strategice și un avantaj material direct. 
    Pierderea pieselor sub pragul de 3 duce la înfrângere. Euristica acordă un scor pozitiv pentru fiecare piesă în plus față de adversar.

    Morile Formate: Formarea unei mori (trei piese în linie) este crucială, deoarece permite eliminarea unei piese a adversarului. 
    Euristica acordă o pondere semnificativă diferenței dintre numărul de mori formate de 'x' și cele formate de 'o', reflectând avantajul strategic major obținut.

    Morile Potențiale: O linie care conține două piese proprii și un spațiu liber reprezintă o amenințare iminentă de a forma o moară. 
    Controlul acestor "mori potențiale" este important atât ofensiv (pentru a crea oportunități), cât și defensiv (pentru a bloca adversarul). 
    Euristica numără aceste configurații și le acordă o pondere pozitivă, deși mai mică decât morile complete.

    Mobilitatea: Numărul de mutări valide disponibile pentru un jucător (fie plasări în prima fază, fie mutări în a doua fază) reflectă flexibilitatea sa strategică. 
    Un jucător cu mobilitate mai mare poate reacționa mai ușor la acțiunile adversarului și poate iniția atacuri. Blocarea completă a mutărilor adversarului duce la victorie. 
    Euristica include diferența de mobilitate ca un factor pozitiv.

    Piesele Blocate (în faza de mutare): O piesă care nu are nicio poziție adiacentă liberă este blocată și inutilă temporar. 
    Euristica penalizează ușor stările în care jucătorul are piese blocate și recompensează stările în care adversarul are piese blocate.

Acești factori sunt combinați printr-o sumă ponderată, unde ponderile reflectă importanța relativă a fiecărui aspect (de exemplu, morile formate au o pondere mai mare decât mobilitatea). 
De asemenea, euristica tratează distinct fazele jocului (plasare vs. mutare) și include verificări pentru stările terminale (victorie/înfrângere), 
returnând valori foarte mari sau foarte mici pentru a ghida corect algoritmii Minimax/AlphaBeta. Această abordare multi-factorială oferă o estimare robustă a valorii unei stări de joc.
"""

class NineMensMorris:
    def __init__(self, board, remaining_pieces, parent=None):
        self.board = list(board)
        self.remaining_x, self.remaining_o = remaining_pieces
        self.parent = parent   

        self.adjacency = {
            0: [1, 9], 1: [0, 2, 4], 2: [1, 14],
            3: [4, 10], 4: [1, 3, 5, 7], 5: [4, 13],
            6: [7, 11], 7: [4, 6, 8], 8: [7, 12],
            9: [0, 10, 21], 10: [3, 9, 11, 18], 11: [6, 10, 15],
            12: [8, 13, 17], 13: [5, 12, 14, 20], 14: [2, 13, 23],
            15: [11, 16], 16: [15, 17, 19], 17: [12, 16],
            18: [10, 19], 19: [16, 18, 20, 22], 20: [13, 19],
            21: [9, 22], 22: [19, 21, 23], 23: [14, 22]
        }
        self.mills = [
            {0, 1, 2}, {3, 4, 5}, {6, 7, 8},
            {9, 10, 11}, {12, 13, 14}, {15, 16, 17},
            {18, 19, 20}, {21, 22, 23},
            {0, 9, 21}, {3, 10, 18}, {6, 11, 15},
            {1, 4, 7}, {16, 19, 22}, {8, 12, 17},  
            {5, 13, 20}, {2, 14, 23}
        ]
        self.x_pieces_count = self.board.count('x')
        self.o_pieces_count = self.board.count('o')

    def is_valid_placement(self, position):
        return self.board[position] == '.'

    def get_possible_placements(self, player):
        return [i for i, spot in enumerate(self.board) if spot == '.']

    def get_possible_moves(self, player):
        moves = []
        player_positions = [i for i, spot in enumerate(self.board) if spot == player]
        num_player_pieces = len(player_positions)  

        # if p has 3 pcs, move to any empty pos
        if num_player_pieces == 3:
            empty_positions = [i for i, spot in enumerate(self.board) if spot == '.']
            for from_pos in player_positions:
                for to_pos in empty_positions:
                    if from_pos != to_pos:  
                         moves.append((from_pos, to_pos))
        else:
            # move to adjacent empty pos
            for from_pos in player_positions:
                for to_pos in self.adjacency[from_pos]:
                    if self.board[to_pos] == '.':
                        moves.append((from_pos, to_pos))
        return moves

    def check_mill(self, position, player):
        for mill in self.mills:
            if position in mill:
                if all(self.board[pos] == player for pos in mill):
                    return True
        return False

    def get_possible_removals(self, opponent):
        opponent_positions = [i for i, spot in enumerate(self.board) if spot == opponent]
        opponent_pieces_in_mill = set()
        possible_removals = []

        # check for mill
        for mill in self.mills:
            if all(self.board[pos] == opponent for pos in mill):
                opponent_pieces_in_mill.update(mill)

        # prefer removing pieces not in a mill
        for pos in opponent_positions:
            if pos not in opponent_pieces_in_mill:
                possible_removals.append(pos)

        # if all are in mills, remove any
        if not possible_removals:
            return opponent_positions
        else:
            return possible_removals

    def place_piece(self, position, player):
        new_board = self.board[:] # Create a copy
        new_board[position] = player
        new_remaining_x = self.remaining_x
        new_remaining_o = self.remaining_o
        if player == 'x':
            new_remaining_x -= 1
        else:
            new_remaining_o -= 1
        return NineMensMorris(new_board, (new_remaining_x, new_remaining_o), self)

    def move_piece(self, from_pos, to_pos, player):
        new_board = self.board[:]  
        new_board[from_pos] = '.'
        new_board[to_pos] = player
        return NineMensMorris(new_board, (self.remaining_x, self.remaining_o), self)

    def remove_piece(self, position_to_remove):
        new_board = self.board[:]  
        if new_board[position_to_remove] != '.' and new_board[position_to_remove] != self.board[position_to_remove]:
             new_board[position_to_remove] = '.'
        return NineMensMorris(new_board, (self.remaining_x, self.remaining_o), self.parent) 
    
    def is_terminal(self):
        if self.remaining_x == 0 and self.remaining_o == 0:  
            if self.x_pieces_count < 3:
                return True # O wins
            if self.o_pieces_count < 3:
                return True # X wins

            if not self.get_possible_moves('x'):
                return True # O wins
            if not self.get_possible_moves('o'):
                return True # X wins
        return False

    def evaluate(self):
        """
        Heuristic evaluation function. Positive favors 'x' (MAX), negative favors 'o' (MIN).
        """
        if self.remaining_x == 0 and self.remaining_o == 0:  
            if self.x_pieces_count < 3: return -10000 # O wins 
            if self.o_pieces_count < 3: return 10000  # X wins 
            x_moves = self.get_possible_moves('x')
            o_moves = self.get_possible_moves('o')
            if not x_moves: return -10000 # O wins (X is blocked)
            if not o_moves: return 10000  # X wins (O is blocked)

        piece_diff = self.x_pieces_count - self.o_pieces_count

        x_mills = self._count_mills('x')
        o_mills = self._count_mills('o')
        mill_diff = x_mills - o_mills

        x_potential_mills = self._count_potential_mills('x')
        o_potential_mills = self._count_potential_mills('o')
        potential_mill_diff = x_potential_mills - o_potential_mills

        mobility_diff = 0
        if self.remaining_x > 0 or self.remaining_o > 0:  
             x_mobility = len(self.get_possible_placements('x')) if self.remaining_x > 0 else 0
             o_mobility = len(self.get_possible_placements('o')) if self.remaining_o > 0 else 0
             mobility_diff = x_mobility - o_mobility
        else:  
             if 'x_moves' not in locals(): x_moves = self.get_possible_moves('x')
             if 'o_moves' not in locals(): o_moves = self.get_possible_moves('o')
             mobility_diff = len(x_moves) - len(o_moves)

        blocked_diff = 0
        if self.remaining_x == 0 and self.remaining_o == 0:
            x_blocked = sum(1 for i in range(24) if self.board[i] == 'x' and not any(self.board[adj] == '.' for adj in self.adjacency[i]))
            o_blocked = sum(1 for i in range(24) if self.board[i] == 'o' and not any(self.board[adj] == '.' for adj in self.adjacency[i]))
            blocked_diff = o_blocked - x_blocked


        w_piece = 20
        w_mill = 50        
        w_potential = 5    
        w_mobility = 1
        w_blocked = 2      

        score = (w_piece * piece_diff +
                 w_mill * mill_diff +
                 w_potential * potential_mill_diff +
                 w_mobility * mobility_diff +
                 w_blocked * blocked_diff)

        if self.remaining_x > 0 or self.remaining_o > 0:
            score += (self.remaining_x - self.remaining_o) * 5  

        return score


    def _count_mills(self, player):
        count = 0
        for mill in self.mills:
            if all(self.board[pos] == player for pos in mill):
                count += 1
        return count

    def _count_potential_mills(self, player):
        count = 0
        for mill in self.mills:
            player_pieces = 0
            empty_spots = 0
            for pos in mill:
                if self.board[pos] == player:
                    player_pieces += 1
                elif self.board[pos] == '.':
                    empty_spots += 1
            if player_pieces == 2 and empty_spots == 1:
                count += 1
        return count

    def get_next_states(self, player):
        next_states = []
        opponent = 'o' if player == 'x' else 'x'

        if (player == 'x' and self.remaining_x > 0) or \
           (player == 'o' and self.remaining_o > 0):
            possible_placements = self.get_possible_placements(player)
            if not possible_placements and (self.remaining_x > 0 if player == 'x' else self.remaining_o > 0):
                 return []

            for pos in possible_placements:
                state_after_place = self.place_piece(pos, player)

                if state_after_place.check_mill(pos, player):
                    removals = state_after_place.get_possible_removals(opponent)
                    if not removals:  
                         next_states.append(state_after_place)
                    else:
                        for remove_pos in removals:
                            state_after_removal = state_after_place.remove_piece(remove_pos)
                            next_states.append(state_after_removal)
                else:
                    next_states.append(state_after_place)

        else:
            possible_moves = self.get_possible_moves(player)
            if not possible_moves:  
                return []  

            for from_pos, to_pos in possible_moves:
                state_after_move = self.move_piece(from_pos, to_pos, player)

                if state_after_move.check_mill(to_pos, player):
                    removals = state_after_move.get_possible_removals(opponent)
                    if not removals: 
                         next_states.append(state_after_move)
                    else:
                        for remove_pos in removals:
                            state_after_removal = state_after_move.remove_piece(remove_pos)
                            next_states.append(state_after_removal)
                else:
                    next_states.append(state_after_move)

        return next_states


    def minimax(self, depth, maximizing_player):
        if depth == 0 or self.is_terminal():
            return self.evaluate(), self

        player = 'x' if maximizing_player else 'o'
        next_states = self.get_next_states(player)

        if not next_states:  
             return (-10000 if maximizing_player else 10000), self

        best_state = None

        if maximizing_player:
            max_eval = -math.inf
            for state in next_states:
                eval_score, _ = state.minimax(depth - 1, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_state = state
            return max_eval, best_state
        else:  
            min_eval = math.inf
            for state in next_states:
                eval_score, _ = state.minimax(depth - 1, True)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_state = state
            return min_eval, best_state

    def alpha_beta(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_terminal():
            return self.evaluate(), self

        player = 'x' if maximizing_player else 'o'
        next_states = self.get_next_states(player)

        if not next_states:  
             return (-10000 if maximizing_player else 10000), self

        best_state = None  

        if maximizing_player:
            value = -math.inf
            for state in next_states:
                eval_score, _ = state.alpha_beta(depth - 1, alpha, beta, False)
                if eval_score > value:
                    value = eval_score
                    best_state = state  
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # Beta cutoff
            if best_state is None and next_states:
                 best_state = next_states[0]  
            return value, best_state
        else: 
            value = math.inf
            for state in next_states:
                eval_score, _ = state.alpha_beta(depth - 1, alpha, beta, True)
                if eval_score < value:
                    value = eval_score
                    best_state = state 
                beta = min(beta, value)
                if alpha >= beta:
                    break  # Alpha cutoff
            if best_state is None and next_states:
                 best_state = next_states[0]
            return value, best_state


    def find_best_move(self, algorithm, depth):
        if algorithm.lower() == "minmax":
            score, best_state = self.minimax(depth, True)  
        elif algorithm.lower() == "alphabeta":
            score, best_state = self.alpha_beta(depth, -math.inf, math.inf, True)  
        else:
            raise ValueError("Unknown algorithm. Use 'MinMax' or 'AlphaBeta'")

        if best_state is None:
             print("Warning: No best state found. Returning initial state.")
             return self, self.evaluate() 

        return best_state, score

    def print_board(self):
        b = self.board  
        visual_board = [
            f"{b[0]}-----{b[1]}-----{b[2]}",
            f"|     |     |",
            f"| {b[3]}---{b[4]}---{b[5]} |",
            f"| |   |   | |",
            f"| | {b[6]}-{b[7]}-{b[8]} | |",
            f"| | |   | | |",
            f"{b[9]}-{b[10]}-{b[11]}   {b[12]}-{b[13]}-{b[14]}",  
            f"| | |   | | |",
            f"| | {b[15]}-{b[16]}-{b[17]} | |",  
            f"| |   |   | |",
            f"| {b[18]}---{b[19]}---{b[20]} |", 
            f"|     |     |",
            f"{b[21]}-----{b[22]}-----{b[23]}",  
        ]

        info = f"Remaining pieces - x: {self.remaining_x}, o: {self.remaining_o}"
        pieces_on_board = f"Pieces on board - x: {self.x_pieces_count}, o: {self.o_pieces_count}"
        return "\n".join(visual_board) + "\n" + info + "\n" + pieces_on_board

    @staticmethod
    def parse_problem_input_list(input_list_str):
        try:
            board_list = eval(input_list_str)
            board = ['.' if item == '.' else ('x' if item == 'x' else 'o') for item in board_list]
            if len(board) != 24:
                raise ValueError("Input board list must have 24 elements.")
            return board
        except Exception as e:
            print(f"Error parsing input board list string: {e}")
            return ['.'] * 24


if __name__ == "__main__":
    initial_board_list_str = "['.', '.', '.', '.', '.', 'x', '.', '.', '.', 'o', '.', 'x', '.', 'x', '.', 'o', '.', 'x', '.', '.', '.', '.', 'o', '.']"
    remaining_pieces_input = (3, 4)
    algorithm_input = "AlphaBeta"
    depth_input = 3

    initial_board = NineMensMorris.parse_problem_input_list(initial_board_list_str)

    game = NineMensMorris(initial_board, remaining_pieces_input)

    print("--- Initial State ---")
    print(game.print_board())
    print(f"Initial heuristic value: {game.evaluate()}")
    print("-" * 20)

    best_move_state, best_score = game.find_best_move(algorithm_input, depth_input)

    print(f"--- Best Move Found (Depth: {depth_input}, Algorithm: {algorithm_input}) ---")
    if best_move_state:
        print(best_move_state.print_board())
        print(f"Heuristic value of best state: {best_score}")
        print("-" * 20)

        output_board_list = [str(p) for p in best_move_state.board]
        print(f"Outputul neformatat: {output_board_list}")

    else:
        print("No valid move found from the initial state.")