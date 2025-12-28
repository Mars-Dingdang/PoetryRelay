import os
import sys
from src.data_loader import load_sentences
from src.graph import PoetryGraph
from src.game import Game
from src.utils import to_simplified

def main():
    print("Initializing Chinese Poetry Relay...")
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    sentences = load_sentences(data_dir)
    
    if not sentences:
        print("No data found. Please ensure data is in the 'data' directory.")
        return

    graph = PoetryGraph(sentences)
    game = Game(graph)
    
    while True:
        print("\n=== Chinese Poetry Relay ===")
        print("1. Solve (Find path between two sentences)")
        print("2. Play Game (Challenge mode)")
        print("3. Exit")
        
        choice = input("Select an option: ")
        
        if choice == '1':
            solve_mode(graph)
        elif choice == '2':
            game_mode(game)
        elif choice == '3':
            break
        else:
            print("Invalid option.")

def get_valid_sentence(graph, prompt_text):
    while True:
        user_input = input(prompt_text).strip()
        if not user_input:
            continue
            
        # Convert to simplified
        s_simp = to_simplified(user_input)
        
        if s_simp in graph.sentences:
            return s_simp
            
        # Fuzzy match
        matches = graph.find_fuzzy_matches(s_simp)
        if matches:
            print(f"Sentence '{user_input}' not found. Did you mean:")
            for i, m in enumerate(matches):
                print(f"{i+1}. {m}")
            print("0. No, use my input exactly (might not work if not in DB)")
            
            choice = input("Select an option (0-N): ").strip()
            if choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(matches):
                    return matches[idx-1]
                elif idx == 0:
                    return s_simp
        else:
            print(f"Warning: '{user_input}' not found in dataset and no close matches.")
            # Allow user to proceed anyway as per instructions "Do not question..."
            return s_simp

def solve_mode(graph):
    print("\n--- Solver Mode ---")
    start = get_valid_sentence(graph, "Enter start sentence: ")
    end = get_valid_sentence(graph, "Enter end sentence: ")
    
    print(f"Searching for path from '{start}' to '{end}'...")
    path = graph.bfs(start, end)
    
    if path:
        print("Path found:")
        print(" -> ".join(path))
        print(f"Length: {len(path)}")
    else:
        print("No solution found.")

def game_mode(game):
    print("\n--- Game Mode ---")
    try:
        start, end = game.generate_problem()
    except Exception as e:
        print(f"Error generating problem: {e}")
        return
        
    print(f"Start: {start}")
    print(f"End:   {end}")
    print("Enter the next sentence to continue the relay.")
    print("Type 'undo' to remove the last step, or 'quit' to give up.")
    
    path = [start]
    
    while path[-1] != end:
        print(f"\nCurrent chain: {' -> '.join(path)}")
        print(f"Target: {end}")
        
        user_input = input("Next sentence: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() == 'quit':
            print("Game over.")
            print("A possible solution was:")
            sol = game.graph.bfs(start, end)
            if sol:
                print(" -> ".join(sol))
            return
            
        if user_input.lower() == 'undo':
            if len(path) > 1:
                removed = path.pop()
                print(f"Undo: Removed '{removed}'")
            else:
                print("Cannot undo the start sentence.")
            continue
            
        # Simplify input
        next_s = to_simplified(user_input)
        
        # Validate
        valid, msg = game.validate_next_step(path[-1], next_s)
        if valid:
            path.append(next_s)
            print("Correct! Accepted.")
        else:
            # Try fuzzy match if not valid
            if next_s not in game.graph.sentences:
                matches = game.graph.find_fuzzy_matches(next_s)
                if matches:
                    print(f"Sentence '{user_input}' not found. Did you mean:")
                    for i, m in enumerate(matches):
                        print(f"{i+1}. {m}")
                    print("0. Cancel")
                    
                    choice = input("Select an option (0-N): ").strip()
                    if choice.isdigit():
                        idx = int(choice)
                        if 1 <= idx <= len(matches):
                            selected = matches[idx-1]
                            # Re-validate with selected
                            valid, msg = game.validate_next_step(path[-1], selected)
                            if valid:
                                path.append(selected)
                                print("Correct! Accepted.")
                            else:
                                print(f"Invalid: {msg}")
                        else:
                            print("Cancelled.")
                else:
                    print(f"Invalid: {msg}")
            else:
                print(f"Invalid: {msg}")
            
    print("\nCongratulations! You successfully completed the relay!")
    print(" -> ".join(path))

if __name__ == "__main__":
    main()
