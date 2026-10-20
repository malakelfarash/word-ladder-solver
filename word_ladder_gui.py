from collections import deque

def dictionary(file_path, length=None):
    words = []

  #هنا حطينا  try عشان ن handle ال Errors
    try:
  #لو الملف موجود هيكمل عادي باقي الكود
     with open(file_path, 'r') as file:

      #دي لوب هتمر علي الملف كله لو في ايرور هتطلع الايرور ف انهو سطر بالظبط
         for line_num, line in enumerate(file, 1):

          # لو في سطر فاضي في الملف بتاع الكلمات
             if not line.strip():
                 print(f"Warning: Empty line at line {line_num}. Skipping...")
                 continue

          #هنا هيشوف لو اليوزر دخل حاجه مش String
             if line is None or not isinstance(line, str):
                 print(f"Warning: Invalid input at line {line_num}. Skipping...")
                 continue

             # هنحذف اي مسافات في الكلمه نفسها
             # هنحذف اي مسافات في السطر
            # هنحول الحروف كلها ل lower
             word = line.strip().replace("\t", "").replace(" ", "").lower()

             #بيتأكد إن الكلمة كلها حروف بس يعني مفيهاش أرقام أو رموز
             if word.isalpha():
                 words.append(word)
             else:
                 print(f"Warning: Skipped invalid word '{word}' at line {line_num}.")
                 continue

    # هنا ل الملف مش موجود اصلا هيطبع الرساله اللي موجوده دي بعد كده بيرجع set اللي هي مجموعه فاضيه ومش هيكمل الكود
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return set()

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
                new_word = word[:i] + c + word[i + 1:]
                if new_word in words:
                    neighbors.append(new_word)
    return neighbors


def bfs_word_ladder(start, goal, words):

    #هنشوف لو القاموس كان فاضي او فيه كلام قليل جدا
    if len(words) < 2:
        print("Error: The dictionary is too small or empty to perform the word ladder.")
        return []

    # هنا بنشوف لو الهدف موجود اصلا في القاموس ولا لا
    if goal not in words:
        print(f"Error: The goal word '{goal}' is not in the dictionary.")
        return []

        # هنا هنشوف لو طول الكلمتين متساوي ولا لا
    if len(start) != len(goal):
        print("Error: The start and goal words must have the same length.")
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

        # لو مفيش Path أو Ladder بين الكلمتين
    print(f"Error: No word ladder found between '{start}' and '{goal}'.")
    return []


# Example
file_path = "wordList.txt"
word_list = dictionary(file_path, length=4)

#هنا بيتاكد ان القاموس اتحمل فعلا ولو في مشكله في تحميله او هو مفيهوش حاجه هيوقف البرنامج ومش هيكمل
if not word_list:
    print("Error: Dictionary could not be loaded or is empty.")
    exit()

start_word = "girl"
goal_word = "good"
ladder = bfs_word_ladder(start_word, goal_word, word_list)
print(ladder)


import tkinter as tk
from tkinter import messagebox
from collections import deque

# ---------- Core Word Ladder Logic ----------
def dictionary(file_path, length=None):
    words = []
    try:
        with open(file_path, 'r') as file:
            for line_num, line in enumerate(file, 1):
                if not line.strip():
                    continue
                word = line.strip().replace("\t", "").replace(" ", "").lower()
                if word.isalpha():
                    words.append(word)
    except FileNotFoundError:
        return set()

    if length is not None:
        words = [word for word in words if len(word) == length]
    return set(words)

def get_neighbors(word, words):
    neighbors = []
    for i in range(len(word)):
        for c in 'abcdefghijklmnopqrstuvwxyz':
            if c != word[i]:
                new_word = word[:i] + c + word[i + 1:]
                if new_word in words:
                    neighbors.append(new_word)
    return neighbors

def bfs_word_ladder(start, goal, words):
    if len(words) < 2:
        return None, "The dictionary is too small or empty."
    if goal not in words:
        return None, f"The goal word '{goal}' is not in the dictionary."
    if len(start) != len(goal):
        return None, "Start and goal words must have the same length."

    queue = deque([[start]])
    visited = set([start])

    while queue:
        path = queue.popleft()
        current_word = path[-1]
        if current_word == goal:
            return path, None
        for neighbor in get_neighbors(current_word, words):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
    return None, f"No word ladder found between '{start}' and '{goal}'."

# ---------- GUI Functions ----------
def solve_word_ladder():
    # مسار ثابت للملف
    file_path = "wordList.txt"
    start = entry_start.get().strip().lower()
    goal = entry_goal.get().strip().lower()

    text_result.config(state="normal")
    text_result.delete(1.0, tk.END)

    if not start or not goal:
        messagebox.showerror("Input Error", "Please fill in the start and goal words.")
        return

    words = dictionary(file_path, length=len(start))
    if not words:
        messagebox.showerror("File Error", "Dictionary could not be loaded or is empty.")
        return

    path, error = bfs_word_ladder(start, goal, words)
    if error:
        messagebox.showerror("Ladder Error", error)
    else:
        text_result.insert(tk.END, " → ".join(path))

    text_result.config(state="disabled")

def clear_all():
    entry_start.delete(0, tk.END)
    entry_goal.delete(0, tk.END)
    text_result.config(state="normal")
    text_result.delete(1.0, tk.END)
    text_result.config(state="disabled")

# ---------- GUI Layout ----------
root = tk.Tk()
root.title("Word Ladder Solver")
root.geometry("400x300")

label_start = tk.Label(root, text="Start Word:")
label_start.pack(pady=(15, 0))
entry_start = tk.Entry(root)
entry_start.pack()

label_goal = tk.Label(root, text="Goal Word:")
label_goal.pack(pady=(10, 0))
entry_goal = tk.Entry(root)
entry_goal.pack()

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=15)
button_solve = tk.Button(frame_buttons, text="Find Word Ladder", bg="#4CAF50", fg="white", command=solve_word_ladder)
button_solve.pack(side=tk.LEFT, padx=5)
button_clear = tk.Button(frame_buttons, text="Clear", bg="gray", fg="white", command=clear_all)
button_clear.pack(side=tk.LEFT, padx=5)

label_result = tk.Label(root, text="Result:")
label_result.pack()
text_result = tk.Text(root, height=5, width=45, state="disabled")
text_result.pack()

root.mainloop()