import pygame
import sys
from typing import List, Tuple, Optional
import copy

# Initialisation de Pygame
pygame.init()

# Constantes
WIDTH, HEIGHT = 800, 900
BOARD_SIZE = 8
CELL_SIZE = 80
BOARD_OFFSET_X = (WIDTH - BOARD_SIZE * CELL_SIZE) // 2
BOARD_OFFSET_Y = 100

# Couleurs
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
BLUE = (70, 130, 180)
PURPLE = (147, 112, 219)

# Joueurs
EMPTY = 0
BLACK_PLAYER = 1
WHITE_PLAYER = 2

# Poids des cases pour l'heuristique
WEIGHTS = [
    [100, -20, 10,  5,  5, 10, -20, 100],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [ 10,  -2, 16,  3,  3, 16,  -2,  10],
    [  5,  -2,  3,  3,  3,  3,  -2,   5],
    [  5,  -2,  3,  3,  3,  3,  -2,   5],
    [ 10,  -2, 16,  3,  3, 16,  -2,  10],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [100, -20, 10,  5,  5, 10, -20, 100]
]

class OthelloGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Othello - Projet IA USTHB 2025")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.reset_game()
        self.game_mode = None  # None = menu, 'human', 'computer'
        self.depth = 2
        self.thinking = False
        
    def reset_game(self):
        """Initialiser le plateau de jeu"""
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.board[3][3] = WHITE_PLAYER
        self.board[3][4] = BLACK_PLAYER
        self.board[4][3] = BLACK_PLAYER
        self.board[4][4] = WHITE_PLAYER
        
        self.current_player = BLACK_PLAYER
        self.valid_moves = self.find_valid_moves(self.board, self.current_player)
        self.pass_count = 0
        self.game_over = False
        self.winner = None
        
    def find_captures_in_direction(self, board: List[List[int]], row: int, col: int, 
                                   player: int, direction: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Trouver les pions à capturer dans une direction"""
        opponent = WHITE_PLAYER if player == BLACK_PLAYER else BLACK_PLAYER
        captures = []
        dr, dc = direction
        r, c = row + dr, col + dc
        
        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == opponent:
            captures.append((r, c))
            r += dr
            c += dc
            
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player and captures:
            return captures
        return []
    
    def find_all_captures(self, board: List[List[int]], row: int, col: int, 
                         player: int) -> List[Tuple[int, int]]:
        """Trouver tous les pions à capturer pour un coup"""
        if board[row][col] != EMPTY:
            return []
        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                     (-1, -1), (-1, 1), (1, -1), (1, 1)]
        all_captures = []
        
        for direction in directions:
            captures = self.find_captures_in_direction(board, row, col, player, direction)
            all_captures.extend(captures)
            
        return all_captures
    
    def find_valid_moves(self, board: List[List[int]], player: int) -> List[Tuple[int, int]]:
        """Trouver tous les coups valides pour un joueur"""
        moves = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] == EMPTY:
                    captures = self.find_all_captures(board, row, col, player)
                    if captures:
                        moves.append((row, col))
        return moves
    
    def make_move(self, board: List[List[int]], row: int, col: int, 
                  player: int) -> Optional[List[List[int]]]:
        """Effectuer un coup et retourner le nouveau plateau"""
        captures = self.find_all_captures(board, row, col, player)
        if not captures:
            return None
        
        new_board = copy.deepcopy(board)
        new_board[row][col] = player
        
        for r, c in captures:
            new_board[r][c] = player
            
        return new_board
    
    def count_pieces(self, board: List[List[int]]) -> Tuple[int, int]:
        """Compter les pions noirs et blancs"""
        black_count = sum(row.count(BLACK_PLAYER) for row in board)
        white_count = sum(row.count(WHITE_PLAYER) for row in board)
        return black_count, white_count
    
    def evaluate_board(self, board: List[List[int]], player: int) -> int:
        """Évaluation heuristique pondérée"""
        score = 0
        opponent = WHITE_PLAYER if player == BLACK_PLAYER else BLACK_PLAYER
        
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] == player:
                    score += WEIGHTS[row][col]
                elif board[row][col] == opponent:
                    score -= WEIGHTS[row][col]
        
        return score
    
    def minimax(self, board: List[List[int]], depth: int, is_maximizing: bool, 
                player: int, alpha: float = float('-inf'), 
                beta: float = float('inf')) -> Tuple[int, Optional[Tuple[int, int]]]:
        """Algorithme MinMax avec élagage alpha-beta"""
        opponent = WHITE_PLAYER if player == BLACK_PLAYER else BLACK_PLAYER
        moves = self.find_valid_moves(board, player if is_maximizing else opponent)
        
        # Cas terminal
        if depth == 0 or not moves:
            return self.evaluate_board(board, player), None
        
        if is_maximizing:
            max_score = float('-inf')
            best_move = moves[0] if moves else None
            
            for move in moves:
                new_board = self.make_move(board, move[0], move[1], player)
                if new_board:
                    score, _ = self.minimax(new_board, depth - 1, False, player, alpha, beta)
                    if score > max_score:
                        max_score = score
                        best_move = move
                    alpha = max(alpha, max_score)
                    if beta <= alpha:
                        break  # Élagage alpha-beta
            
            return max_score, best_move
        else:
            min_score = float('inf')
            best_move = moves[0] if moves else None
            
            for move in moves:
                new_board = self.make_move(board, move[0], move[1], opponent)
                if new_board:
                    score, _ = self.minimax(new_board, depth - 1, True, player, alpha, beta)
                    if score < min_score:
                        min_score = score
                        best_move = move
                    beta = min(beta, min_score)
                    if beta <= alpha:
                        break  # Élagage alpha-beta
            
            return min_score, best_move
    
    def handle_click(self, pos: Tuple[int, int]):
        """Gérer les clics de souris"""
        x, y = pos
        
        # Clic sur le plateau
        if BOARD_OFFSET_Y <= y < BOARD_OFFSET_Y + BOARD_SIZE * CELL_SIZE:
            col = (x - BOARD_OFFSET_X) // CELL_SIZE
            row = (y - BOARD_OFFSET_Y) // CELL_SIZE
            
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                if (row, col) in self.valid_moves and not self.game_over:
                    if self.game_mode == 'computer' and self.current_player == WHITE_PLAYER:
                        return
                    
                    new_board = self.make_move(self.board, row, col, self.current_player)
                    if new_board:
                        self.board = new_board
                        self.current_player = WHITE_PLAYER if self.current_player == BLACK_PLAYER else BLACK_PLAYER
                        self.valid_moves = self.find_valid_moves(self.board, self.current_player)
                        self.pass_count = 0
                        
                        if not self.valid_moves:
                            self.handle_pass()
    
    def handle_pass(self):
        """Gérer le passage de tour"""
        self.pass_count += 1
        if self.pass_count >= 2:
            self.game_over = True
            black_count, white_count = self.count_pieces(self.board)
            if black_count > white_count:
                self.winner = "Noir"
            elif white_count > black_count:
                self.winner = "Blanc"
            else:
                self.winner = "Égalité"
        else:
            self.current_player = WHITE_PLAYER if self.current_player == BLACK_PLAYER else BLACK_PLAYER
            self.valid_moves = self.find_valid_moves(self.board, self.current_player)
    
    def ai_move(self):
        """Tour de l'IA"""
        if not self.thinking and self.game_mode == 'computer' and self.current_player == WHITE_PLAYER and not self.game_over:
            self.thinking = True
            score, best_move = self.minimax(self.board, self.depth, True, WHITE_PLAYER)
            
            if best_move:
                new_board = self.make_move(self.board, best_move[0], best_move[1], WHITE_PLAYER)
                if new_board:
                    self.board = new_board
                    self.current_player = BLACK_PLAYER
                    self.valid_moves = self.find_valid_moves(self.board, self.current_player)
                    self.pass_count = 0
                    
                    if not self.valid_moves:
                        self.handle_pass()
            else:
                self.handle_pass()
            
            self.thinking = False
    
    def draw_menu(self):
        """Dessiner le menu de sélection"""
        self.screen.fill(WHITE)
        
        # Titre
        title = self.font.render("OTHELLO", True, BLACK)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        
        subtitle = self.small_font.render("Projet IA - USTHB 2025", True, GRAY)
        self.screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 150))
        
        # Bouton Humain vs Humain
        button1_rect = pygame.Rect(WIDTH // 2 - 200, 250, 400, 80)
        pygame.draw.rect(self.screen, BLUE, button1_rect, border_radius=10)
        text1 = self.font.render("Partie 1: Humain vs Humain", True, WHITE)
        self.screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, 275))
        
        # Bouton Humain vs Ordinateur
        button2_rect = pygame.Rect(WIDTH // 2 - 200, 360, 400, 80)
        pygame.draw.rect(self.screen, PURPLE, button2_rect, border_radius=10)
        text2 = self.font.render("Partie 2: Humain vs IA", True, WHITE)
        self.screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, 385))
        
        # Sélecteur de profondeur
        depth_text = self.small_font.render(f"Profondeur MinMax (np): {self.depth}", True, BLACK)
        self.screen.blit(depth_text, (WIDTH // 2 - depth_text.get_width() // 2, 480))
        
        # Boutons +/-
        minus_rect = pygame.Rect(WIDTH // 2 - 100, 520, 40, 40)
        plus_rect = pygame.Rect(WIDTH // 2 + 60, 520, 40, 40)
        pygame.draw.rect(self.screen, GRAY, minus_rect, border_radius=5)
        pygame.draw.rect(self.screen, GRAY, plus_rect, border_radius=5)
        
        minus_text = self.font.render("-", True, WHITE)
        plus_text = self.font.render("+", True, WHITE)
        self.screen.blit(minus_text, (WIDTH // 2 - 90, 520))
        self.screen.blit(plus_text, (WIDTH // 2 + 70, 520))
        
        return button1_rect, button2_rect, minus_rect, plus_rect
    
    def draw_board(self):
        """Dessiner le plateau de jeu"""
        self.screen.fill(WHITE)
        
        # Scores
        black_count, white_count = self.count_pieces(self.board)
        
        # Score Noir
        pygame.draw.rect(self.screen, BLACK if self.current_player == BLACK_PLAYER else LIGHT_GRAY, 
                        (50, 20, 200, 60), border_radius=10)
        black_text = self.font.render(f"Noir: {black_count}", True, WHITE)
        self.screen.blit(black_text, (90, 35))
        
        # Score Blanc
        pygame.draw.rect(self.screen, BLACK if self.current_player == WHITE_PLAYER else LIGHT_GRAY, 
                        (WIDTH - 250, 20, 200, 60), border_radius=10)
        white_text = self.font.render(f"Blanc: {white_count}", True, BLACK if self.current_player == WHITE_PLAYER else WHITE)
        self.screen.blit(white_text, (WIDTH - 220, 35))
        
        # Statut
        if self.game_over:
            status_text = self.font.render(f"Partie terminée! {self.winner} gagne!", True, BLACK)
        elif self.thinking:
            status_text = self.font.render("IA réfléchit...", True, PURPLE)
        elif not self.valid_moves:
            status_text = self.small_font.render("Aucun coup - Appuyez ESPACE pour passer", True, BLACK)
        else:
            player_name = "Noir" if self.current_player == BLACK_PLAYER else "Blanc"
            status_text = self.font.render(f"Tour: {player_name}", True, BLACK)
        
        self.screen.blit(status_text, (WIDTH // 2 - status_text.get_width() // 2, 45))
        
        # Plateau
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x = BOARD_OFFSET_X + col * CELL_SIZE
                y = BOARD_OFFSET_Y + row * CELL_SIZE
                
                # Case
                color = DARK_GREEN if (row + col) % 2 == 0 else GREEN
                pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
                
                # Pion
                if self.board[row][col] == BLACK_PLAYER:
                    pygame.draw.circle(self.screen, BLACK, 
                                      (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 30)
                elif self.board[row][col] == WHITE_PLAYER:
                    pygame.draw.circle(self.screen, WHITE, 
                                      (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 30)
                
                # Coups possibles
                if (row, col) in self.valid_moves:
                    pygame.draw.circle(self.screen, YELLOW, 
                                      (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 8)
        
        # Boutons
        reset_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 60, 200, 40)
        pygame.draw.rect(self.screen, BLUE, reset_rect, border_radius=5)
        reset_text = self.small_font.render("Nouvelle Partie", True, WHITE)
        self.screen.blit(reset_text, (WIDTH // 2 - reset_text.get_width() // 2, HEIGHT - 50))
        
        return reset_rect
    
    def run(self):
        """Boucle principale du jeu"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_mode is None:
                        button1, button2, minus, plus = self.draw_menu()
                        if button1.collidepoint(event.pos):
                            self.game_mode = 'human'
                            self.reset_game()
                        elif button2.collidepoint(event.pos):
                            self.game_mode = 'computer'
                            self.reset_game()
                        elif minus.collidepoint(event.pos) and self.depth > 1:
                            self.depth -= 1
                        elif plus.collidepoint(event.pos) and self.depth < 6:
                            self.depth += 1
                    else:
                        reset_button = self.draw_board()
                        if reset_button.collidepoint(event.pos):
                            self.game_mode = None
                            self.reset_game()
                        else:
                            self.handle_click(event.pos)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.valid_moves and not self.game_over:
                        self.handle_pass()
                    if event.key == pygame.K_ESCAPE:
                        self.game_mode = None
                        self.reset_game()
            
            # Dessin
            if self.game_mode is None:
                self.draw_menu()
            else:
                self.draw_board()
                
                # Tour de l'IA
                if self.game_mode == 'computer' and self.current_player == WHITE_PLAYER and not self.game_over:
                    pygame.time.wait(500)
                    self.ai_move()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = OthelloGame()
    game.run()