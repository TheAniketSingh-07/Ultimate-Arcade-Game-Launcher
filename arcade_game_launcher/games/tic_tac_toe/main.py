#!/usr/bin/env python3
"""
Tic Tac Toe - Strategic X's and O's Game
Classic strategy game with AI opponent!
"""

import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700
BOARD_SIZE = 450
CELL_SIZE = BOARD_SIZE // 3
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 200)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_BLUE = (0, 50, 100)

class TicTacToeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("⭕ Tic Tac Toe - Strategic Game!")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # X is human, O is AI
        self.game_over = False
        self.winner = None
        self.player_score = 0
        self.ai_score = 0
        self.ties = 0
        
        # UI
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        # Board position
        self.board_x = (WINDOW_WIDTH - BOARD_SIZE) // 2
        self.board_y = 100
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if self.game_over:
                        # Check if clicked on restart button
                        restart_rect = pygame.Rect(WINDOW_WIDTH // 2 - 75, 600, 150, 40)
                        if restart_rect.collidepoint(event.pos):
                            self.reset_game()
                    else:
                        self.handle_click(event.pos)
        return True
    
    def handle_click(self, pos):
        if self.current_player != 'X' or self.game_over:
            return
        
        # Convert click position to board coordinates
        x, y = pos
        if (self.board_x <= x <= self.board_x + BOARD_SIZE and
            self.board_y <= y <= self.board_y + BOARD_SIZE):
            
            col = (x - self.board_x) // CELL_SIZE
            row = (y - self.board_y) // CELL_SIZE
            
            if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == '':
                self.make_move(row, col, 'X')
    
    def make_move(self, row, col, player):
        self.board[row][col] = player
        
        if self.check_winner():
            self.game_over = True
            self.winner = player
            if player == 'X':
                self.player_score += 1
            else:
                self.ai_score += 1
        elif self.is_board_full():
            self.game_over = True
            self.winner = 'Tie'
            self.ties += 1
        else:
            self.current_player = 'O' if player == 'X' else 'X'
    
    def ai_move(self):
        if self.current_player != 'O' or self.game_over:
            return
        
        # AI strategy: Try to win, then block, then random
        move = self.find_winning_move('O')
        if move is None:
            move = self.find_winning_move('X')  # Block player
        if move is None:
            move = self.find_random_move()
        
        if move:
            row, col = move
            self.make_move(row, col, 'O')
    
    def find_winning_move(self, player):
        # Check all possible moves for a winning position
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    # Try this move
                    self.board[row][col] = player
                    if self.check_winner() == player:
                        self.board[row][col] = ''  # Undo move
                        return (row, col)
                    self.board[row][col] = ''  # Undo move
        return None
    
    def find_random_move(self):
        empty_cells = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    empty_cells.append((row, col))
        
        if empty_cells:
            return random.choice(empty_cells)
        return None
    
    def check_winner(self):
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != '':
                return row[0]
        
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != '':
                return self.board[0][col]
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return self.board[0][2]
        
        return None
    
    def is_board_full(self):
        for row in self.board:
            for cell in row:
                if cell == '':
                    return False
        return True
    
    def reset_game(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
    
    def draw_board(self):
        # Draw board background
        board_rect = pygame.Rect(self.board_x, self.board_y, BOARD_SIZE, BOARD_SIZE)
        pygame.draw.rect(self.screen, WHITE, board_rect)
        pygame.draw.rect(self.screen, BLACK, board_rect, 3)
        
        # Draw grid lines
        for i in range(1, 3):
            # Vertical lines
            x = self.board_x + i * CELL_SIZE
            pygame.draw.line(self.screen, BLACK, (x, self.board_y), (x, self.board_y + BOARD_SIZE), 3)
            
            # Horizontal lines
            y = self.board_y + i * CELL_SIZE
            pygame.draw.line(self.screen, BLACK, (self.board_x, y), (self.board_x + BOARD_SIZE, y), 3)
        
        # Draw X's and O's
        for row in range(3):
            for col in range(3):
                if self.board[row][col] != '':
                    self.draw_symbol(row, col, self.board[row][col])
    
    def draw_symbol(self, row, col, symbol):
        center_x = self.board_x + col * CELL_SIZE + CELL_SIZE // 2
        center_y = self.board_y + row * CELL_SIZE + CELL_SIZE // 2
        
        if symbol == 'X':
            # Draw X
            offset = CELL_SIZE // 3
            pygame.draw.line(self.screen, RED, 
                           (center_x - offset, center_y - offset),
                           (center_x + offset, center_y + offset), 8)
            pygame.draw.line(self.screen, RED,
                           (center_x + offset, center_y - offset),
                           (center_x - offset, center_y + offset), 8)
        else:  # O
            # Draw O
            radius = CELL_SIZE // 3
            pygame.draw.circle(self.screen, BLUE, (center_x, center_y), radius, 8)
    
    def draw_ui(self):
        # Title
        title_text = self.font_medium.render("⭕ Tic Tac Toe", True, DARK_BLUE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 30))
        self.screen.blit(title_text, title_rect)
        
        # Score
        score_text = f"Player (X): {self.player_score}  AI (O): {self.ai_score}  Ties: {self.ties}"
        score_surface = self.font_small.render(score_text, True, BLACK)
        score_rect = score_surface.get_rect(center=(WINDOW_WIDTH // 2, 65))
        self.screen.blit(score_surface, score_rect)
        
        # Current player or game status
        if self.game_over:
            if self.winner == 'Tie':
                status_text = "It's a Tie!"
                color = GRAY
            elif self.winner == 'X':
                status_text = "You Win! 🎉"
                color = GREEN
            else:
                status_text = "AI Wins! 🤖"
                color = RED
            
            status_surface = self.font_medium.render(status_text, True, color)
            status_rect = status_surface.get_rect(center=(WINDOW_WIDTH // 2, 570))
            self.screen.blit(status_surface, status_rect)
            
            # Restart button
            restart_rect = pygame.Rect(WINDOW_WIDTH // 2 - 75, 600, 150, 40)
            pygame.draw.rect(self.screen, GREEN, restart_rect)
            pygame.draw.rect(self.screen, BLACK, restart_rect, 2)
            
            restart_text = self.font_small.render("Play Again", True, WHITE)
            restart_text_rect = restart_text.get_rect(center=restart_rect.center)
            self.screen.blit(restart_text, restart_text_rect)
            
        else:
            if self.current_player == 'X':
                status_text = "Your Turn (X)"
                color = RED
            else:
                status_text = "AI Thinking... (O)"
                color = BLUE
            
            status_surface = self.font_medium.render(status_text, True, color)
            status_rect = status_surface.get_rect(center=(WINDOW_WIDTH // 2, 570))
            self.screen.blit(status_surface, status_rect)
        
        # Controls
        controls = [
            "Click to place X",
            "R: Restart game",
            "ESC: Exit"
        ]
        
        for i, control in enumerate(controls):
            control_surface = self.font_small.render(control, True, GRAY)
            self.screen.blit(control_surface, (10, 600 + i * 25))
    
    def draw(self):
        self.screen.fill(LIGHT_GRAY)
        self.draw_board()
        self.draw_ui()
        pygame.display.flip()
    
    def run(self):
        print("⭕ Tic Tac Toe - Strategic Game Started!")
        print("🎮 Click to place X, compete against AI!")
        
        running = True
        ai_delay = 0
        
        while running:
            running = self.handle_events()
            
            # AI move with delay for better UX
            if self.current_player == 'O' and not self.game_over:
                ai_delay += 1
                if ai_delay > 60:  # 1 second delay
                    self.ai_move()
                    ai_delay = 0
            else:
                ai_delay = 0
            
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    game = TicTacToeGame()
    game.run()

if __name__ == "__main__":
    main()
