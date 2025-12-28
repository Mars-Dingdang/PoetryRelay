import random
from collections import deque

class Game:
    def __init__(self, graph):
        self.graph = graph

    def generate_problem(self):
        """
        Generate a random start and end sentence such that a path exists.
        Returns (start, end).
        """
        attempts = 0
        while attempts < 100:
            start = self.graph.get_random_sentence()
            # Do a partial BFS to find a reachable node at some distance
            queue = deque([(start, 0)])
            visited = {start}
            candidates = []
            
            # Limit BFS depth/size to avoid taking too long
            max_steps = 1000
            steps = 0
            
            while queue and steps < max_steps:
                curr, dist = queue.popleft()
                steps += 1
                
                if dist >= 2: # At least 1 intermediate step preferred, but direct is ok too
                    candidates.append(curr)
                
                if dist < 5: # Don't go too deep for candidates
                    for neighbor in self.graph.get_neighbors(curr):
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append((neighbor, dist + 1))
            
            if candidates:
                end = random.choice(candidates)
                return start, end
            
            attempts += 1
            
        raise Exception("Could not generate a valid problem after multiple attempts.")

    def validate_solution(self, start, end, user_path):
        """
        Check if the user_path is a valid relay from start to end.
        """
        if not user_path:
            return False, "Empty path."
        
        if user_path[0] != start:
            return False, f"Path must start with '{start}'."
        
        if user_path[-1] != end:
            return False, f"Path must end with '{end}'."
            
        for i in range(len(user_path) - 1):
            curr = user_path[i]
            next_node = user_path[i+1]
            
            valid, msg = self.validate_next_step(curr, next_node)
            if not valid:
                return False, msg
                
        return True, "Correct"

    def validate_next_step(self, current, next_sentence):
        """
        Check if next_sentence is a valid successor to current.
        """
        if next_sentence not in self.graph.sentences:
            return False, f"Sentence '{next_sentence}' is not in the dataset."
            
        neighbors = self.graph.get_neighbors(current)
        if next_sentence not in neighbors:
            return False, f"'{current}' cannot be followed by '{next_sentence}'."
            
        return True, "Valid"
