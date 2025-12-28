from collections import defaultdict, deque
from src.utils import get_keys, levenshtein_distance
import random

class PoetryGraph:
    def __init__(self, sentences):
        self.sentences = sentences
        self.buckets = defaultdict(list)
        self.build_graph()

    def build_graph(self):
        """
        Build the implicit graph by bucketing sentences by their starting keys.
        """
        print("Building graph...")
        for s in self.sentences:
            if not s: continue
            first_char = s[0]
            keys = get_keys(first_char)
            for k in keys:
                self.buckets[k].append(s)
        print("Graph built.")

    def get_neighbors(self, sentence):
        """
        Get all sentences that can follow the given sentence.
        """
        if not sentence: return []
        last_char = sentence[-1]
        keys = get_keys(last_char)
        
        neighbors = []
        for k in keys:
            if k in self.buckets:
                neighbors.extend(self.buckets[k])
        return neighbors

    def bfs(self, start, end):
        """
        Find the shortest path from start to end using BFS.
        Returns a list of sentences [start, ..., end] or None if no path.
        """
        # Note: We do NOT check if start/end are in self.sentences here, 
        # because the caller might have handled fuzzy matching or user insistence.
        # However, if 'start' is not in the graph (buckets), we can't find neighbors.
        # But 'get_neighbors' works based on the last char of 'start', so it works even if 'start' is new.
        # The issue is 'end'. If 'end' is not in the graph, we can never reach it unless we add it?
        # Actually, if 'end' is not in the graph, we can still reach it if some node connects TO it.
        # But our graph is implicit. We only know nodes that are in 'buckets'.
        # If 'end' is not in 'sentences', it won't be in any bucket, so no node will point to it?
        # Wait, 'buckets' stores nodes by START char.
        # If A -> B, then B must be in a bucket corresponding to A's last char.
        # So if 'end' is not in 'sentences', it is not in any bucket.
        # Thus, no node A can have 'end' as a neighbor in our implicit graph.
        # So if 'end' is not in sentences, path is impossible unless we treat it specially.
        # But the prompt says "Do not question...".
        # If 'end' is not in DB, maybe we should check if any neighbor of current frontier IS 'end'?
        # But 'get_neighbors' returns nodes from 'buckets'. 'end' is not in 'buckets'.
        # So we can never reach 'end' if it's not in DB.
        # Unless we relax the condition: "reach a node that is fuzzy match to end"?
        # No, the prompt says "give all possible T" for fuzzy match.
        # So we assume the user picks a valid T from the fuzzy list.
        # If the user insists on a T that is NOT in DB, we probably can't solve it.
        # But let's stick to the fuzzy match logic in main.py.
        
        if start not in self.sentences:
             # If start is not in DB, we can still start BFS from it because we just need its last char.
             pass
        
        if end not in self.sentences:
            # If end is not in DB, we can't reach it in our graph structure.
            return None
            
        queue = deque([start])
        visited = {start: None} # Maps node -> parent
        
        while queue:
            current = queue.popleft()
            
            if current == end:
                return self.reconstruct_path(visited, end)
            
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited[neighbor] = current
                    queue.append(neighbor)
                    
        return None

    def reconstruct_path(self, visited, end):
        path = []
        curr = end
        while curr:
            path.append(curr)
            curr = visited[curr]
        return path[::-1]

    def get_random_sentence(self):
        return random.choice(self.sentences)

    def find_fuzzy_matches(self, query, max_distance=2):
        """
        Find sentences in the dataset that are within max_distance of query.
        """
        matches = []
        # Optimization: filter by length first
        q_len = len(query)
        candidates = [s for s in self.sentences if abs(len(s) - q_len) <= max_distance]
        
        for s in candidates:
            dist = levenshtein_distance(query, s)
            if dist <= max_distance and dist > 0: # dist > 0 because 0 is exact match
                matches.append(s)
        return matches
