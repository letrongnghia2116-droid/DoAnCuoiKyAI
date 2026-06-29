import heapq
import math
import random
from collections import deque

# Hằng số lưới mê cung
ROWS = 20
COLS = 20

# Lớp Node đại diện cho một trạng thái trong không gian tìm kiếm
class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state        # (row, col)
        self.parent = parent
        self.action = action      # "up", "down", "left", "right"
        self.path_cost = path_cost

    def __lt__(self, other):
        # Hỗ trợ hàng đợi ưu tiên so sánh chi phí khi có cùng giá trị
        return self.path_cost < other.path_cost

def heuristic(a, b):
    # Manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def actions(state, maze):
    row, col = state
    move = []
    # up
    if row > 0 and maze[row - 1][col] == 0:
        move.append("up")
    # down
    if row < ROWS - 1 and maze[row + 1][col] == 0:
        move.append("down")
    # left
    if col > 0 and maze[row][col - 1] == 0:
        move.append("left")
    # right
    if col < COLS - 1 and maze[row][col + 1] == 0:
        move.append("right")
    return move

def result(state, action):
    row, col = state
    if action == "up":
        return (row - 1, col)
    elif action == "down":
        return (row + 1, col)
    elif action == "left":
        return (row, col - 1)
    elif action == "right":
        return (row, col + 1)
    return state

def goal_test(state, goal):
    return state == goal

def solution(node):
    path = []
    curr = node
    while curr is not None:
        path.append(curr.state)
        curr = curr.parent
    path.reverse()
    return path

# CÁC THUẬT TOÁN TÌM ĐƯỜNG (AI TEXTBOOK NODE-BASED STYLE)

class BFS:
    label = "BFS"
    def __init__(self, maze, start, goal):
        self.maze = maze
        self.start = start
        self.goal = goal

    def solve(self):
        root = Node(self.start)
        if goal_test(root.state, self.goal):
            return {"path": [root.state], "visited": [root.state], "found": True}

        frontier = deque([root])
        reached = {root.state}
        Visited = []

        while frontier:
            node = frontier.popleft()
            Visited.append(node.state)

            if goal_test(node.state, self.goal):
                return {"path": solution(node), "visited": Visited, "found": True}

            for action in actions(node.state, self.maze):
                child_state = result(node.state, action)
                if child_state not in reached:
                    reached.add(child_state)
                    child = Node(child_state, node, action, node.path_cost + 1)
                    if goal_test(child.state, self.goal):
                        return {"path": solution(child), "visited": Visited , "found": True}
                    frontier.append(child)

        return {"path": [], "visited": Visited, "found": False}

class DFS:
    label = "DFS"
    def __init__(self, maze, start, goal):
        self.maze = maze
        self.start = start
        self.goal = goal

    def solve(self):
        root = Node(self.start)
        if goal_test(root.state, self.goal):
            return {"path": [root.state], "visited": [root.state], "found": True}

        frontier = deque([root])
        reached = {root.state}
        Visited = []

        while frontier:
            node = frontier.pop()
            Visited.append(node.state)

            if goal_test(node.state, self.goal):
                return {"path": solution(node), "visited": Visited, "found": True}

            for action in actions(node.state, self.maze):
                child_state = result(node.state, action)
                if child_state not in reached:
                    reached.add(child_state)
                    child = Node(child_state, node, action, node.path_cost + 1)
                    if goal_test(child.state, self.goal):
                        return {"path": solution(child), "visited": Visited , "found": True}
                    frontier.append(child)

        return {"path": [], "visited": Visited, "found": False}

import heapq

class AStar:
    label = "A*"

    def __init__(self, maze, start, goal):
        self.maze = maze
        self.start = start
        self.goal = goal

    def solve(self):
        root = Node(self.start)

        f_score = heuristic(root.state, self.goal) # f(n) = g(n) + h(n) / g(n) được khởi tạo bằng 0, còn h(n) là khoảng cách Manhattan

        frontier = [(f_score, root)]

        cost = {root.state: 0} # dùng theo dõi giá trị g
        visited = []
        closed = set()

        while frontier:
            f, node = heapq.heappop(frontier)

            if node.state in closed:
                continue

            closed.add(node.state) # nếu node đã nằm trong frontier thì không đuyệt lại
            visited.append(node.state)

            if goal_test(node.state, self.goal):
                return { "path": solution(node), "visited": visited, "found": True }

            for action in actions(node.state, self.maze):
                child_state = result(node.state, action)
                new_cost = node.path_cost + 1

                if child_state not in cost or new_cost < cost[child_state]:

                    cost[child_state] = new_cost

                    child = Node(
                        child_state,
                        node,
                        action,
                        new_cost
                    )

                    f = new_cost + heuristic( child_state, self.goal )

                    heapq.heappush(frontier, (f, child))

        return { "path": [], "visited": visited, "found": False }
    
class Greedy:
    label = "Greedy Best-First"
    def __init__(self, maze, start, goal):
        self.maze = maze
        self.start = start
        self.goal = goal

    def solve(self):
        root = Node(self.start)
        h = heuristic(root.state, self.goal)
        frontier = [(h, root)]
        reached = {root.state}
        Visited = []

        while frontier:
            node = heapq.heappop(frontier)
            Visited.append(node.state)

            if goal_test(node.state, self.goal):
                return {"path": solution(node), "visited": Visited, "found": True}

            for action in actions(node.state, self.maze):
                child_state = result(node.state, action)
                if child_state not in reached:
                    reached.add(child_state)
                    child = Node(child_state, node, action, node.path_cost + 1)
                    heapq.heappush(frontier, (heuristic(child_state, self.goal), child))

        return {"path": [], "visited": Visited, "found": False}

class SteepestAscent:
    label = "Steepest Ascent"
    def __init__(self, maze, start, goal):
        self.maze = maze
        self.start = start
        self.goal = goal
    
    def solve(self):
        current_state = Node(self.start)
        Visited = []
        while True:
            Visited.append(current_state.state)
            if goal_test(current_state.state, self.goal):
                return {"path": solution(current_state), "visited": Visited, "found": True}
            
            h_current = heuristic(current_state.state, self.goal)
            best_neighbors = []
            min_h = float('inf')
            for action in actions(current_state.state, self.maze):
                child_state = result(current_state.state, action)
                h_child = heuristic(child_state, self.goal)

                if h_child < min_h:
                    min_h = h_child
                    best_neighbors = [Node(child_state, parent=current_state, action=action, path_cost=current_state.path_cost + 1)]
                elif h_child == min_h:
                    best_neighbors.append(Node(child_state, parent=current_state, action=action, path_cost=current_state.path_cost + 1))
            
            if min_h >= h_current or not best_neighbors:
                return {"path": solution(current_state), "visited": Visited, "found": False}
            current_state = best_neighbors[0]

class LocalBeamSearch:
    label = "Local Beam Search"

    def __init__(self, maze, start, goal, k=3):
        self.maze = maze
        self.start = start
        self.goal = goal
        self.k = k

    def solve(self):
        current_state = [Node(self.start)]
        reached = set()
        Visited = []

        while True:
            neighbors_state = []

            for node in current_state:
                if node.state not in reached:
                    Visited.append(node.state)
                    reached.add(node.state)

                if goal_test(node.state, self.goal):
                    return { "path": solution(node), "visited": Visited, "found": True }

                for action in actions(node.state, self.maze):
                    child_state = result(node.state, action)
                    if child_state not in reached:
                        child = Node(
                            child_state,
                            parent=node,
                            action=action,
                            path_cost=node.path_cost + 1
                        )
                        if goal_test(child_state, self.goal):
                            return { "path": solution(child), "visited": Visited, "found": True }
                        neighbors_state.append(child)

            if not neighbors_state:
                return {
                    "path": [],
                    "visited": Visited,
                    "found": False
                }

            unique_candidates = {}
            for c in neighbors_state:
                if c.state not in unique_candidates or c.path_cost < unique_candidates[c.state].path_cost:
                    unique_candidates[c.state] = c

            candidates_list = list(unique_candidates.values())
            candidates_list.sort(key=lambda x: heuristic(x.state, self.goal))

            current_state = candidates_list[:self.k]

class BeliefStateSearch:
    label = "Belief State Search"
    def __init__(self, maze, start, goal):
        self.maze = maze
        # Trong môi trường này, 'start' có thể là 1 danh sách các vị trí
        # Nếu người dùng chỉ truyền vào 1 tọa độ tuple, ta bọc nó thành frozenset.
        if isinstance(start, tuple) and isinstance(start[0], int):
            self.start_belief = frozenset([start])
        else:
            self.start_belief = frozenset(start)
        self.goal = goal

    def belief_result(self, belief, action):
        new_belief = set()
        for state in belief:
            # Kiểm tra xem action này có hợp lệ với state hiện tại không
            if action in actions(state, self.maze):
                # Nếu không vướng tường, di chuyển bình thường
                next_state = result(state, action)
            else:
                # Nếu vướng tường, tác tử bị chặn lại và đứng im
                next_state = state
            new_belief.add(next_state)
        return frozenset(new_belief)

    def solve(self):
        root = Node(self.start_belief)
        # Định vị (Localization) - Gộp các ô lại làm 1
        if len(root.state) == 1:
            localization_node = root
            loc_visited = [root.state]
            loc_path = [root.state]
        else:
            frontier = deque([root])
            reached = {root.state}
            loc_visited = []
            localization_node = None
            while frontier:
                node = frontier.popleft()
                loc_visited.append(node.state)
                if len(node.state) == 1:
                    localization_node = node
                    break
                for action in ["up", "down", "left", "right"]:
                    child_state = self.belief_result(node.state, action)
                    if child_state not in reached:
                        reached.add(child_state)
                        child = Node(child_state, node, action, node.path_cost + 1)
                        frontier.append(child)
            if localization_node is not None:
                loc_path = solution(localization_node)
            else:
                loc_path, loc_visited = [root.state], [root.state]

        # Chạy BFS từ vị trí đơn lẻ đã gộp tới đích
        single_cell = list(loc_path[-1])[0]
        bfs = BFS(self.maze, single_cell, self.goal)
        bfs_res = bfs.solve()
        if not bfs_res["found"]:
            return {"path": [], "visited": loc_visited, "found": False}
        # Gộp kết quả của 2 pha
        combined_path = loc_path + [frozenset([cell]) for cell in bfs_res["path"][1:]]
        combined_visited = loc_visited + [frozenset([cell]) for cell in bfs_res["visited"]]
        return {"path": combined_path, "visited": combined_visited, "found": True}

class FogOfWarSearch:
    label = "Fog Of War (Online) Search"
    
    def __init__(self, maze, start, goal=None):
        self.maze = maze
        if isinstance(start, tuple) and isinstance(start[0], int):
            self.current_pos = start
        else:
            self.current_pos = list(start)[0] if start else (0, 0)
            
        self.goal = goal
        self.ROWS = len(maze)
        self.COLS = len(maze[0])
        self.belief_map = [[-1 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        
        self.belief_map[self.current_pos[0]][self.current_pos[1]] = 0
        self.goal_found = False

    def get_neighbors(self, pos):
        r, c = pos
        neighbors = []
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.ROWS and 0 <= nc < self.COLS:
                neighbors.append((nr, nc))
        return neighbors

    def sense_and_update_belief(self, visited_history):
        cells_to_scan = [self.current_pos] + self.get_neighbors(self.current_pos)
        for (nr, nc) in cells_to_scan:
            real_value = self.maze[nr][nc]
            if real_value == 1 or real_value == '#':
                self.belief_map[nr][nc] = 1
            elif self.goal and (nr, nc) == self.goal:
                self.belief_map[nr][nc] = 2
                self.goal_found = True
            else:
                self.belief_map[nr][nc] = 0
                
            if (nr, nc) not in visited_history:
                visited_history.append((nr, nc))

    def find_frontiers(self):
        frontiers = []
        for r in range(self.ROWS):
            for c in range(self.COLS):
                if self.belief_map[r][c] == 0:
                    for nr, nc in self.get_neighbors((r, c)):
                        if self.belief_map[nr][nc] == -1:
                            frontiers.append((r, c))
                            break
        return frontiers

    def local_bfs(self, start, target_condition_func):
        queue = deque([[start]])
        visited = {start}
        
        while queue:
            path = queue.popleft()
            curr = path[-1]
            
            if target_condition_func(curr):
                return path
                
            for nr, nc in self.get_neighbors(curr):
                if (self.belief_map[nr][nc] in [0, 2]) and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append(path + [(nr, nc)])
        return None

    def solve(self):
        full_path = [self.current_pos]
        visited_history = []
        
        max_steps = self.ROWS * self.COLS * 2
        steps = 0
        
        while steps < max_steps:
            steps += 1
            self.sense_and_update_belief(visited_history)
            
            if self.goal and self.current_pos == self.goal:
                return {"path": full_path, "visited": visited_history, "found": True}
                
            if self.goal_found:
                path_to_goal = self.local_bfs(self.current_pos, lambda pos: pos == self.goal)
                if path_to_goal and len(path_to_goal) > 1:
                    next_step = path_to_goal[1]
                else:
                    return {"path": full_path, "visited": visited_history, "found": False}
            else:
                frontiers = self.find_frontiers()
                if not frontiers:
                    return {"path": full_path, "visited": visited_history, "found": False}
                
                path_to_frontier = self.local_bfs(self.current_pos, lambda pos: pos in frontiers)
                
                if path_to_frontier and len(path_to_frontier) > 1:
                    next_step = path_to_frontier[1]
                else:
                    return {"path": full_path, "visited": visited_history, "found": False}
            
            self.current_pos = next_step
            full_path.append(self.current_pos)
            
        return {"path": full_path, "visited": visited_history, "found": False}

class Backtracking:
    label = "Backtracking (Hamiltonian Path)"
    def __init__(self, maze, start, goal):
        self.maze = maze
        self.start = start
        self.goal = goal
        # Đếm tổng số ô trống (đường đi hợp lệ có giá trị 0) trong mê cung
        self.total_empty = sum(1 for r in range(len(maze)) for c in range(len(maze[0])) if maze[r][c] == 0)

    def solve(self):
        reached = {self.start}
        path = [self.start]
        Visited = []
        found = self._backtrack(self.start, reached, path, Visited)
        if found:
            return {"path": path, "visited": Visited, "found": True}
        return {"path": [], "visited": Visited, "found": False}

    def _backtrack(self, current_state, reached, path, Visited):
        Visited.append(current_state)
        if current_state == self.goal:
            if len(path) == self.total_empty:
                return True
            else:
                return False
        for action in actions(current_state, self.maze):
            child_state = result(current_state, action)
            if child_state not in reached :
                reached.add(child_state)
                path.append(child_state)
                # Đi sâu vào nhánh đó
                if self._backtrack(child_state, reached, path, Visited):
                    return True
                # Backtrack Hoàn tác trạng thái nếu nhánh này không dẫn tới đích hợp lệ
                reached.remove(child_state)
                path.pop()
        return False

class AlphaBeta:
    label = "Alpha-Beta (Agent vs Monster)"
    def __init__(self, maze, start, goal, monster_start=None, max_depth=8):
        self.maze = maze
        self.start = start
        self.goal = goal
        self.max_depth = max_depth
        if monster_start is None:
            self.monster_start = (len(maze) // 2, len(maze[0]) // 2)
        else:
            self.monster_start = monster_start

    def evaluate(self, player_pos, monster_pos, player_visited_count=None, monster_visited_count=None):
        if player_pos == self.goal: return 10000
        if player_pos == monster_pos: return -10000
        pr, pc = player_pos
        gr, gc = self.goal
        d_goal = abs(pr - gr) + abs(pc - gc)
        mr, mc = monster_pos
        d_monster = abs(pr - mr) + abs(pc - mc)
        if d_monster < 3:
            val = -(d_goal * 10) + (d_monster * 50)
        else:
            val = -(d_goal * 100) + d_monster
        if player_visited_count:
            p_visits = player_visited_count.get(player_pos, 0)
            if p_visits > 0: val -= p_visits * 200
        if monster_visited_count:
            m_visits = monster_visited_count.get(monster_pos, 0)
            if m_visits > 0: val += m_visits * 200       
        return val

    def minmax(self, player_pos, monster_pos, depth, alpha, beta, is_max, player_visited_count=None, monster_visited_count=None):
        if depth == 0 or player_pos == self.goal or player_pos == monster_pos:
            return self.evaluate(player_pos, monster_pos, player_visited_count, monster_visited_count), None
        if is_max: # Lượt của Agent, tối đa hóa điểm
            max_eval = -math.inf
            best_act = None
            valid_moves = actions(player_pos, self.maze)
            if not valid_moves: return self.evaluate(player_pos, monster_pos, player_visited_count, monster_visited_count), None
            
            # Xếp nước đi ưu tiên theo heuristic (sắp xếp giảm dần vì Agent muốn tối đa hóa)
            valid_moves.sort(key=lambda act: self.evaluate(result(player_pos, act), monster_pos, player_visited_count, monster_visited_count), reverse=True)
            
            for act in valid_moves:
                next_p = result(player_pos, act)
                eval_val, _ = self.minmax(next_p, monster_pos, depth - 1, alpha, beta, False, player_visited_count, monster_visited_count)
                if eval_val > max_eval:
                    max_eval = eval_val
                    best_act = act
                alpha = max(alpha, eval_val)
                if beta <= alpha: break # Cắt tỉa Alpha
            return max_eval, best_act
        else: # Lượt của Quái vật -> Tối thiểu hóa điểm
            min_eval = math.inf
            best_act = None
            valid_moves = actions(monster_pos, self.maze)
            if not valid_moves: return self.evaluate(player_pos, monster_pos, player_visited_count, monster_visited_count), None
            
            # Xếp nước đi ưu tiên theo heuristic (sắp xếp tăng dần vì Quái vật muốn tối thiểu hóa)
            valid_moves.sort(key=lambda act: self.evaluate(player_pos, result(monster_pos, act), player_visited_count, monster_visited_count))
            
            for act in valid_moves:
                next_m = result(monster_pos, act)
                eval_val, _ = self.minmax(player_pos, next_m, depth - 1, alpha, beta, True, player_visited_count, monster_visited_count)
                if eval_val < min_eval:
                    min_eval = eval_val
                    best_act = act
                beta = min(beta, eval_val)
                if beta <= alpha: break # Cắt tỉa Beta
            return min_eval, best_act

    def solve(self):
        player_pos = self.start
        monster_pos = self.monster_start
        path = [player_pos]
        visited = [player_pos]
        monster_path = [monster_pos]
        # Lưu số lần đã ghé thăm các ô trong ván đấu thực tế để phạt lặp
        player_visited_count = {player_pos: 1}
        monster_visited_count = {monster_pos: 1}
        # Chạy game turn-by-turn (Giới hạn 100 lượt để tránh lặp vô tận do né nhau)
        for turn in range(100):
            # Bạn
            _, p_act = self.minmax(player_pos, monster_pos, self.max_depth, -math.inf, math.inf, True, player_visited_count, monster_visited_count)
            if p_act:
                player_pos = result(player_pos, p_act)
            path.append(player_pos)
            visited.append(player_pos)
            monster_path.append(monster_pos)
            # Cập nhật số lần ghé thăm của Agent
            player_visited_count[player_pos] = player_visited_count.get(player_pos, 0) + 1
            if player_pos == self.goal:
                return {"path": path, "visited": visited, "monster_path": monster_path, "found": True, "msg": "Win"}
            if player_pos == monster_pos:
                return {"path": path, "visited": visited, "monster_path": monster_path, "found": False, "msg": "Lost"}
            # Quái vật
            _, m_act = self.minmax(player_pos, monster_pos, self.max_depth, -math.inf, math.inf, False, player_visited_count, monster_visited_count)
            if m_act:
                monster_pos = result(monster_pos, m_act)
            path.append(player_pos)
            visited.append(player_pos)
            monster_path.append(monster_pos)
            # Cập nhật số lần ghé thăm của Monster
            monster_visited_count[monster_pos] = monster_visited_count.get(monster_pos, 0) + 1
            if player_pos == monster_pos:
                return {"path": path, "visited": visited, "monster_path": monster_path, "found": False, "msg": "Lost"}
        return {"path": path, "visited": visited, "monster_path": monster_path, "found": False, "msg": "Draw (Turn limit)"}

class Minimax:
    label = "Minimax"

    def __init__(self, maze, start, goal, monster_start):
        self.maze = maze
        self.start = start
        self.goal = goal
        self.monster_start = monster_start
        self.max_depth = 4

    def evaluate(self, player_pos, monster_pos):
        if player_pos == self.goal:
            return 1000

        if player_pos == monster_pos:
            return -1000

        d_goal = abs(player_pos[0] - self.goal[0]) + abs(player_pos[1] - self.goal[1])
        d_monster = abs(player_pos[0] - monster_pos[0]) + abs(player_pos[1] - monster_pos[1])

        # Agent muốn gần đích và xa quái
        return -10 * d_goal + 5 * d_monster

    def minmax(self, player_pos, monster_pos, depth, is_max):
        if depth == 0 or player_pos == self.goal or player_pos == monster_pos:
            return self.evaluate(player_pos, monster_pos), None

        if is_max:
            best_value = -math.inf
            best_action = None

            for action in actions(player_pos, self.maze):
                next_player = result(player_pos, action)

                value, _ = self.minmax(
                    next_player,
                    monster_pos,
                    depth - 1,
                    False
                )

                if value > best_value:
                    best_value = value
                    best_action = action

            return best_value, best_action

        else:
            best_value = math.inf
            best_action = None

            for action in actions(monster_pos, self.maze):
                next_monster = result(monster_pos, action)

                value, _ = self.minmax(
                    player_pos,
                    next_monster,
                    depth - 1,
                    True
                )

                if value < best_value:
                    best_value = value
                    best_action = action

            return best_value, best_action

    def solve(self):
        player_pos = self.start
        monster_pos = self.monster_start

        path = [player_pos]
        monster_path = [monster_pos]
        visited = [player_pos]

        for _ in range(100):

            # Agent đi
            _, action = self.minmax(
                player_pos,
                monster_pos,
                self.max_depth,
                True
            )

            if action:
                player_pos = result(player_pos, action)

            path.append(player_pos)
            visited.append(player_pos)
            monster_path.append(monster_pos)

            if player_pos == self.goal:
                return {
                    "path": path,
                    "visited": visited,
                    "monster_path": monster_path,
                    "found": True,
                    "msg": "Win"
                }

            if player_pos == monster_pos:
                return {
                    "path": path,
                    "visited": visited,
                    "monster_path": monster_path,
                    "found": False,
                    "msg": "Lost"
                }

            # Monster đi
            _, action = self.minmax(
                player_pos,
                monster_pos,
                self.max_depth,
                False
            )

            if action:
                monster_pos = result(monster_pos, action)

            path.append(player_pos)
            visited.append(player_pos)
            monster_path.append(monster_pos)

            if player_pos == monster_pos:
                return {
                    "path": path,
                    "visited": visited,
                    "monster_path": monster_path,
                    "found": False,
                    "msg": "Lost"
                }

        return {
            "path": path,
            "visited": visited,
            "monster_path": monster_path,
            "found": False,
            "msg": "Draw"
        }

class ForwardChecking:
    label = "Forward Checking"

    def __init__(self, maze, start, goal):
        self.maze = maze
        self.start = start
        self.goal = goal

    def forward_check(self, state, visited):

        future_visited = visited | {state}

        # Nếu đã tới đích thì luôn hợp lệ
        if state == self.goal:
            return True

        # Domain của state
        state_domain = []

        for action in actions(state, self.maze):
            nxt = result(state, action)

            if nxt not in future_visited:
                state_domain.append(nxt)

        # Không còn nước đi nào mà chưa tới đích
        if len(state_domain) == 0:
            return False

        # Forward checking:
        # kiểm tra domain của các trạng thái tương lai
        for neighbor in state_domain:

            if neighbor == self.goal:
                continue

            neighbor_domain = 0

            for action in actions(neighbor, self.maze):
                nxt = result(neighbor, action)

                if nxt not in future_visited:
                    neighbor_domain += 1

            # Một trạng thái tương lai bị mất toàn bộ lựa chọn
            if neighbor_domain == 0:
                return False

        return True

    def solve(self):
        visited = {self.start}
        path = [self.start]
        Visited = []

        found = self._backtrack(
            self.start,
            visited,
            path,
            Visited
        )

        return { "path": path if found else [], "visited": Visited, "found": found }

    def _backtrack(self, current_state, visited, path, Visited):

        Visited.append(current_state)

        if current_state == self.goal:
            return True

        # Sinh các trạng thái kế tiếp hợp lệ
        valid_moves = []

        for action in actions(current_state, self.maze):
            child_state = result(current_state, action)

            if child_state not in visited:
                valid_moves.append(child_state)

        # Forward Checking trước khi gán giá trị
        for child_state in valid_moves:

            if not self.forward_check(child_state, visited):
                continue

            visited.add(child_state)
            path.append(child_state)

            if self._backtrack( child_state, visited, path, Visited ):
                return True

            # Backtracking
            visited.remove(child_state)
            path.pop()

        return False

# Bản đăng ký thuật toán công khai cho giao diện sử dụng
ALGORITHMS = {
    "BFS":      BFS,
    "DFS":      DFS,
    "A*":       AStar,
    "Greedy Best-First":   Greedy,
    "Steepest Ascent": SteepestAscent,
    "Belief State":      BeliefStateSearch,
    "Backtracking":      Backtracking,
    "Alpha-Beta":        AlphaBeta,
    "Minimax":           Minimax,
    "Forward Checking":  ForwardChecking,
}
