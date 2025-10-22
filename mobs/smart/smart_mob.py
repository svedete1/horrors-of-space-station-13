
from collections import deque

from settings import *

import pygame
import math
import mobs
from pprint import pprint


class SmartMob(mobs.mob.Mob):
    path = list()
    has_task = False

    # здесь работает логика моба, эта функция вызывается каждый кадр
    def process(self):
        # Код писать тут
        if self.has_task:
            self.task_move()
        # НЕ ТРОГАТЬ ЭТО
        self.update_sprite()
        self.movement()

    def find_path(self, map_pos: tuple[int, int]):
        start_xy = self.map_pos
        goal_xy = map_pos
        grid = self.game.turfhandler.path_map
        diagonals = True
        rows, cols = len(grid), len(grid[0])

        # Build lookup: (x, y) -> (row, col)
        coord_to_index = {}
        for r in range(rows):
            for c in range(cols):
                val = grid[r][c]
                if val is not None:
                    coord_to_index[val] = (r, c)

        # Validate start and goal
        if start_xy not in coord_to_index:
            raise ValueError(f"Start {start_xy} not found or is an obstacle")
        if goal_xy not in coord_to_index:
            raise ValueError(f"Goal {goal_xy} not found or is an obstacle")

        start = coord_to_index[start_xy]
        goal = coord_to_index[goal_xy]

        # Directions (4 or 8)
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        if diagonals:
            dirs += [(1,1),(1,-1),(-1,1),(-1,-1)]

        queue = deque([start])
        came_from = {start: None}

        while queue:
            r, c = queue.popleft()
            if (r, c) == goal:
                break
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] is not None:
                    if (nr, nc) not in came_from:
                        came_from[(nr, nc)] = (r, c)
                        queue.append((nr, nc))

        if goal not in came_from:
            return None  # No path found

        # Reconstruct path in (x, y) coordinates
        path = []
        node = goal
        while node is not None:
            r, c = node
            path.append(grid[r][c])
            node = came_from[node]
        path.reverse()
        return path

    def move_to_map_pos(self, map_pos: tuple[int, int]):
        self.has_task = True
        self.path = self.find_path(map_pos)

    def task_move(self):
        if self.moving:
            return
        if not self.path:
            self.has_task = False
            return

        self.move(self.path.pop(0))


