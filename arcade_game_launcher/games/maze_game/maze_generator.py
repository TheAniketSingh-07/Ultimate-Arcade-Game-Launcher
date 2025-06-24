"""
Maze Generator
Creates interesting mazes using recursive backtracking algorithm
"""

import random
from settings import MAZE_WIDTH, MAZE_HEIGHT

class MazeGenerator:
    """Generates mazes with good layouts"""
    
    def __init__(self, width=MAZE_WIDTH, height=MAZE_HEIGHT):
        self.width = width
        self.height = height
        self.maze = []
        self.visited = []
        
    def generate_maze(self):
        """Generate a new maze using recursive backtracking"""
        # Initialize maze with all walls
        self.maze = [[1 for _ in range(self.width)] for _ in range(self.height)]
        self.visited = [[False for _ in range(self.width)] for _ in range(self.height)]
        
        # Start from top-left corner
        self._carve_path(1, 1)
        
        # Ensure start and end are clear
        self.maze[1][1] = 0  # Start position
        self.maze[self.height-2][self.width-2] = 0  # End position
        
        # Add some extra paths for better gameplay
        self._add_extra_paths()
        
        return self.maze
    
    def _carve_path(self, x, y):
        """Recursively carve paths through the maze"""
        self.visited[y][x] = True
        self.maze[y][x] = 0  # 0 = path, 1 = wall
        
        # Get random directions
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Check bounds
            if (0 < nx < self.width-1 and 0 < ny < self.height-1 and 
                not self.visited[ny][nx]):
                
                # Carve the wall between current and next cell
                self.maze[y + dy//2][x + dx//2] = 0
                self._carve_path(nx, ny)
    
    def _add_extra_paths(self):
        """Add some extra paths to make the maze more interesting"""
        extra_paths = min(10, (self.width * self.height) // 20)
        
        for _ in range(extra_paths):
            x = random.randint(2, self.width-3)
            y = random.randint(2, self.height-3)
            
            # Randomly remove some walls to create loops
            if random.random() < 0.3:
                self.maze[y][x] = 0
    
    def get_valid_positions(self):
        """Get all valid (path) positions in the maze"""
        positions = []
        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y][x] == 0:  # Path
                    positions.append((x, y))
        return positions
    
    def is_valid_position(self, x, y):
        """Check if position is valid (within bounds and not a wall)"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.maze[y][x] == 0
        return False
