import math
import random

"""
În abordarea noastră simplificată, inspirată de Rețelele Bayesiene, nu construim explicit o rețea cu tabele de probabilități condiționale (CPT-uri), 
deoarece acest lucru ar necesita date de antrenament sau definirea manuală complexă a sute de probabilități. 
În schimb, folosim funcția heuristică existentă ca un proxy pentru scorul pe care o Rețea Bayesiană l-ar atribui unei stări. 
Această funcție combină liniar diverse caracteristici (features) ale stării de joc, iar ponderile asociate fiecărei caracteristici reflectă importanța relativă 
sau puterea de influență a acelei caracteristici asupra "probabilității" ca starea respectivă să fie favorabilă jucătorului 'x'.

Alegerea ponderilor se bazează pe cunoștințe despre strategia jocului Țintar:

    w_mill = 60 (Diferența de Mori): Aceasta are cea mai mare pondere. 
    Formarea unei mori este evenimentul cel mai important strategic, deoarece permite capturarea unei piese adverse și poate schimba dramatic cursul jocului. 
    O diferență pozitivă mare în numărul de mori indică un avantaj substanțial. Această pondere mare reflectă influența directă și puternică a morilor asupra câștigării jocului.

    w_piece = 25 (Diferența de Piese): Avantajul material (a avea mai multe piese) este fundamental. Oferă mai multe opțiuni, control asupra tablei și rezistență la capturi. 
    Este al doilea cel mai important factor, de aceea are o pondere semnificativă, dar mai mică decât morile, deoarece o moară poate anula rapid un avantaj numeric mic.

    w_potential = 7 (Diferența de Mori Potențiale): Controlul liniilor cu două piese proprii și un spațiu liber ("aproape mori") este important pentru a crea amenințări viitoare și a restricționa adversarul. 
    Este un factor strategic relevant, dar efectul său nu este la fel de imediat sau garantat ca o moară completă, deci ponderea este moderată.

    w_blocked = 3 (Diferența de Piese Blocate): A avea piese blocate reduce mobilitatea și eficiența. 
    Blocarea pieselor adversarului este un avantaj. Factorul are o pondere mică, deoarece situațiile de blocaj total sunt mai rare decât alte avantaje, dar contribuie la evaluarea fină a poziției în faza de mutare.

    w_mobility = 2 (Diferența de Mobilitate): Flexibilitatea de a muta piesele este utilă, permițând repoziționarea și exploatarea oportunităților. 
    O mobilitate mai mare este în general bună. Are cea mai mică pondere, deoarece numărul brut de mutări nu surprinde întotdeauna calitatea acelor mutări 
    (o singură mutare care formează o moară este mai valoroasă decât multe mutări pasive).

Aceste ponderi transformă caracteristicile observate ale stării de joc într-un scor unic, care aproximează cât de "bună" este starea respectivă. 
Abordarea selectează mutarea care duce la starea imediat următoare cu cel mai mare scor (cea mai mare "probabilitate" estimată de a fi bună), 
acționând ca un agent greedy bazat pe această evaluare inspirată de principiile combinării dovezilor din Rețelele Bayesiene.
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

        if num_player_pieces < 3:
             return []

        if num_player_pieces == 3 and (self.remaining_x == 0 and self.remaining_o == 0):
            empty_positions = [i for i, spot in enumerate(self.board) if spot == '.']
            for from_pos in player_positions:
                for to_pos in empty_positions:
                    if from_pos != to_pos:
                         moves.append((from_pos, to_pos))
        else:
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

        for mill in self.mills:
            if all(self.board[pos] == opponent for pos in mill):
                opponent_pieces_in_mill.update(mill)

        for pos in opponent_positions:
            if pos not in opponent_pieces_in_mill:
                possible_removals.append(pos)

        if not possible_removals and opponent_positions:
            return opponent_positions
        else:
            return possible_removals

    def place_piece(self, position, player):
        new_board = self.board[:]
        new_board[position] = player
        new_remaining_x = self.remaining_x
        new_remaining_o = self.remaining_o
        if player == 'x': new_remaining_x -= 1
        else: new_remaining_o -= 1
        return NineMensMorris(new_board, (new_remaining_x, new_remaining_o), self)

    def move_piece(self, from_pos, to_pos, player):
        new_board = self.board[:]
        new_board[from_pos] = '.'
        new_board[to_pos] = player
        return NineMensMorris(new_board, (self.remaining_x, self.remaining_o), self)

    def remove_piece(self, position_to_remove):
        new_board = self.board[:]
        opponent_player = '.'
        if 0 <= position_to_remove < 24 and new_board[position_to_remove] != '.':
             opponent_player = new_board[position_to_remove]
             new_board[position_to_remove] = '.'
        else:
             print(f"Warning: Attempted to remove invalid position {position_to_remove}")
             pass
        return NineMensMorris(new_board, (self.remaining_x, self.remaining_o), self.parent)

    def is_terminal(self):
        in_movement_phase = self.remaining_x == 0 and self.remaining_o == 0
        if in_movement_phase:
            if self.x_pieces_count < 3: return True
            if self.o_pieces_count < 3: return True
            if self.x_pieces_count >= 3 and not self.get_possible_moves('x'): return True
            if self.o_pieces_count >= 3 and not self.get_possible_moves('o'): return True
        return False

    def _get_current_player_from_state(self):
         total_placed = (9 - self.remaining_x) + (9 - self.remaining_o)
         if total_placed < 18:
              return 'x' if total_placed % 2 == 0 else 'o'
         else:
              return 'x'

    def evaluate(self):
        in_movement_phase = self.remaining_x == 0 and self.remaining_o == 0
        if in_movement_phase:
            if self.o_pieces_count < 3: return 10000
            if self.x_pieces_count < 3: return -10000
            x_can_move = True
            o_can_move = True
            if self.x_pieces_count >= 3:
                 x_moves = self.get_possible_moves('x')
                 if not x_moves: x_can_move = False
            if self.o_pieces_count >= 3:
                 o_moves = self.get_possible_moves('o')
                 if not o_moves: o_can_move = False

            if not x_can_move and o_can_move : return -10000
            if not o_can_move and x_can_move : return 10000


        piece_diff = self.x_pieces_count - self.o_pieces_count

        x_mills = self._count_mills('x')
        o_mills = self._count_mills('o')
        mill_diff = x_mills - o_mills

        x_potential_mills = self._count_potential_mills('x')
        o_potential_mills = self._count_potential_mills('o')
        potential_mill_diff = x_potential_mills - o_potential_mills

        mobility_diff = 0
        if self.remaining_x > 0 or self.remaining_o > 0:
             mobility_diff = self.remaining_x - self.remaining_o
        else:
             if 'x_moves' not in locals(): x_moves = self.get_possible_moves('x')
             if 'o_moves' not in locals(): o_moves = self.get_possible_moves('o')
             mobility_diff = len(x_moves) - len(o_moves)

        blocked_diff = 0
        if in_movement_phase:
             if self.x_pieces_count > 3:
                  x_blocked = sum(1 for i in range(24) if self.board[i] == 'x' and not any(self.board[adj] == '.' for adj in self.adjacency[i]))
             else: x_blocked = 0
             if self.o_pieces_count > 3:
                  o_blocked = sum(1 for i in range(24) if self.board[i] == 'o' and not any(self.board[adj] == '.' for adj in self.adjacency[i]))
             else: o_blocked = 0
             blocked_diff = o_blocked - x_blocked

        w_piece = 25
        w_mill = 60
        w_potential = 7
        w_mobility = 2
        w_blocked = 3

        score = (w_piece * piece_diff +
                 w_mill * mill_diff +
                 w_potential * potential_mill_diff +
                 w_mobility * mobility_diff +
                 w_blocked * blocked_diff)

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
                if self.board[pos] == player: player_pieces += 1
                elif self.board[pos] == '.': empty_spots += 1
            if player_pieces == 2 and empty_spots == 1:
                count += 1
        return count

    def get_next_states(self, player):
        next_states = []
        opponent = 'o' if player == 'x' else 'x'

        is_placement = (player == 'x' and self.remaining_x > 0) or \
                       (player == 'o' and self.remaining_o > 0)

        if is_placement:
            possible_placements = self.get_possible_placements(player)
            if not possible_placements: return []

            for pos in possible_placements:
                state_after_place = self.place_piece(pos, player)
                if any(all(state_after_place.board[p] == player for p in mill) for mill in state_after_place.mills if pos in mill):
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
            if not possible_moves: return []

            for from_pos, to_pos in possible_moves:
                state_after_move = self.move_piece(from_pos, to_pos, player)
                if any(all(state_after_move.board[p] == player for p in mill) for mill in state_after_move.mills if to_pos in mill):
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
        pass

    def alpha_beta(self, depth, alpha, beta, maximizing_player):
        pass

    def find_best_move_minimax_ab(self, algorithm, depth):
        print("Using Minimax/AlphaBeta (for comparison)")
        player = 'x'
        if algorithm.lower() == "minmax":
             raise NotImplementedError("Minimax not fully re-implemented here")
        elif algorithm.lower() == "alphabeta":
             raise NotImplementedError("AlphaBeta not fully re-implemented here")
        else:
            raise ValueError("Unknown algorithm")


    def find_best_move_bayesian_proxy(self):
        player = 'x'
        print(f"Finding best move for player '{player}' using BN Proxy (1-ply search)...")

        possible_next_states = self.get_next_states(player)

        if not possible_next_states:
            print("No possible moves found!")
            return None, -math.inf

        best_score = -math.inf
        best_states = []

        for state in possible_next_states:
            score = state.evaluate()

            if score > best_score:
                best_score = score
                best_states = [state]
            elif score == best_score:
                best_states.append(state)

        chosen_state = random.choice(best_states) if best_states else None

        if chosen_state:
             print(f"Chosen best state score: {best_score}")
        else:
             print("Could not determine a best state.")


        return chosen_state, best_score


    def print_board(self):
        b = self.board
        visual_board = [
            f"{b[0]}-----{b[1]}-----{b[2]}", f"|     |     |", f"| {b[3]}---{b[4]}---{b[5]} |",
            f"| |   |   | |", f"| | {b[6]}-{b[7]}-{b[8]} | |", f"| | |   | | |",
            f"{b[9]}-{b[10]}-{b[11]}   {b[12]}-{b[13]}-{b[14]}", f"| | |   | | |",
            f"| | {b[15]}-{b[16]}-{b[17]} | |", f"| |   |   | |", f"| {b[18]}---{b[19]}---{b[20]} |",
            f"|     |     |", f"{b[21]}-----{b[22]}-----{b[23]}",
        ]
        info = f"Remaining pieces - x: {self.remaining_x}, o: {self.remaining_o}"
        pieces_on_board = f"Pieces on board - x: {self.x_pieces_count}, o: {self.o_pieces_count}"
        return "\n".join(visual_board) + "\n" + info + "\n" + pieces_on_board

    @staticmethod
    def parse_problem_input_list(input_list_str):
        try:
            import ast
            board_list_raw = ast.literal_eval(input_list_str)
            board = []
            for item in board_list_raw:
                 if item == 'x': board.append('x')
                 elif item == '0': board.append('o')
                 else: board.append('.')
            if len(board) != 24:
                raise ValueError("Input board list must have 24 elements.")
            return board
        except Exception as e:
            print(f"Error parsing input board list string: {e}")
            return ['.'] * 24


if __name__ == "__main__":
    initial_board_list_str = "['.', '.', '.', '.', '.', 'x', '.', '.', '.', 'o', '.', 'x', '.', 'x', '.', 'o', '.', 'x', '.', '.', '.', '.', 'o', '.']"
    remaining_pieces_input = (3, 4)

    initial_board = NineMensMorris.parse_problem_input_list(initial_board_list_str)
    game = NineMensMorris(initial_board, remaining_pieces_input)

    print("--- Initial State ---")
    print(game.print_board())
    print(f"Initial heuristic value (for x): {game.evaluate()}")
    print("-" * 20)

    best_move_state, best_score = game.find_best_move_bayesian_proxy()

    print(f"\n--- Best Move Found (Bayesian Proxy) ---")
    if best_move_state:
        print(best_move_state.print_board())
        print(f"Heuristic value of best state: {best_score}")
        print("-" * 20)

        output_board_list = [str(p) if p != 'o' else '0' for p in best_move_state.board]
        print(f"Outputul neformatat: {output_board_list}")
    else:
        print("No valid move found from the initial state.")