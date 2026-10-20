from collections import deque

def dictionary(file_path, length=None):
    words = []
    with open(file_path, 'r') as file:
        for line in file:
            word = line.strip().lower()  # lowercase & with no spaces
            if word.isalpha():  # confirm it is alphabiatical without any char
                words.append(word)
    
    if length is not None:
        filtered = []
        for word in words:
            if len(word) == length:  
                filtered.append(word)
        words = filtered

    return set(words)

# This function generates all possible words that are one letter different from the given word
def get_neighbors(word, words):
    neighbors = []
    for i in range(len(word)):
        for c in 'abcdefghijklmnopqrstuvwxyz':
            # Check if the current letter is different from the letter at position i in the word
            if c != word[i]:
                # Create a new word by replacing the letter at position i with the current letter c
                new_word = word[:i] + c + word[i+1:]
                if new_word in words:
                    neighbors.append(new_word)
    return neighbors

def bfs_word_ladder(start, goal, words):
    if goal not in words:
        return []

    # Initialize the BFS queue with the start word
    queue = deque([[start]])
    # Keep track of visited words
    visited = set([start])

    while queue:
        # Get the current path from the queue
        path = queue.popleft()
        # The current word is the last word in the path
        current_word = path[-1]

        # If the current word is the goal, return the path
        if current_word == goal:
            return path

        # Get all neighbors (words one letter different) of the current word
        for neighbor in get_neighbors(current_word, words):
            if neighbor not in visited:
                # Mark the neighbor as visited
                visited.add(neighbor)
                # Create a new path with the neighbor added
                new_path = list(path)
                new_path.append(neighbor)
                # Add the new path to the queue
                queue.append(new_path)

    # If no path is found, return an empty list
    return []

# Example
file_path = "wordList.txt" 
word_list = dictionary(file_path, length = 4) 
start_word = "girl"
goal_word = "good"
ladder = bfs_word_ladder(start_word, goal_word, word_list)
print(ladder)