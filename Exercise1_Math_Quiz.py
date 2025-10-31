from tkinter import *
from tkinter import messagebox
import random

root = Tk()
root.title("Arithmetic Quiz")         # Set window title
root.geometry("480x520")              # Set window size
root.resizable(0, 0)                  # Prevent window resizing

# Load the background image
bg_img = PhotoImage(file="Math.png")  

# Design colors
PINK = "#ffb6c1"      # light pink
HOT_PINK = "#ff69b4"  # hot pink
WHITE = "#fff"        # white
TEXT = "#b92a68"      # deep pink for text

# Global variables to manage quiz state
difficulty = None        # Stores selected difficulty level
score = 0                # Stores user's score
question_num = 0         # Tracks current question number
first_try = True         # True if it's the user's first attempt on a question
correct_answer = None    # Stores the correct answer for the current problem
problem_text = ""        # The current arithmetic problem as text
user_answer_entry = None # Entry widget for user's answer

def displayMenu():
    """Displays the difficulty selection menu with background image and pink/white theme."""
    clear_window()
    # Create background label and stretch it to fill window
    bg_label = Label(root, image=bg_img)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    # All other widgets are created after the background so they appear above it
    menu_label = Label(root, text="DIFFICULTY LEVEL", font=("Arial", 18, "bold"), bg=WHITE, fg=HOT_PINK)
    menu_label.pack(pady=18)
    # Difficulty selection buttons
    Button(root, text="1. Easy", width=18, font=("Arial", 15, "bold"), bg=PINK, fg=TEXT, command=lambda: start_quiz(1)).pack(pady=8)
    Button(root, text="2. Moderate", width=18, font=("Arial", 15, "bold"), bg=PINK, fg=TEXT, command=lambda: start_quiz(2)).pack(pady=8)
    Button(root, text="3. Advanced", width=18, font=("Arial", 15, "bold"), bg=PINK, fg=TEXT, command=lambda: start_quiz(3)).pack(pady=8)

def clear_window():
    """Removes all widgets from the root window."""
    for widget in root.winfo_children():
        widget.destroy()

def randomInt(min_val, max_val):
    """Returns a random integer between min_val and max_val (inclusive)."""
    return random.randint(min_val, max_val)

def decideOperation():
    """Randomly returns '+' or '-' to decide the operation for the problem."""
    return random.choice(['+', '-'])

def start_quiz(selected_difficulty):
    """Initializes quiz variables and starts the first question."""
    global difficulty, score, question_num
    difficulty = selected_difficulty
    score = 0
    question_num = 0
    next_question()

def next_question():
    """Moves to the next question or shows results if quiz is finished."""
    global question_num, first_try
    question_num += 1
    first_try = True
    if question_num > 10:
        displayResults()
    else:
        displayProblem()

def displayProblem():
    """Generates and displays a new arithmetic problem based on difficulty, with background image and pink/white theme."""
    global correct_answer, problem_text, user_answer_entry
    clear_window()
    # Create background label and stretch it
    bg_label = Label(root, image=bg_img)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    # Determine number range based on difficulty
    min_val, max_val = {1: (1, 9), 2: (10, 99), 3: (1000, 9999)}[difficulty]
    num1 = randomInt(min_val, max_val)
    num2 = randomInt(min_val, max_val)
    op = decideOperation()
    # Calculate correct answer
    if op == '+':
        correct_answer = num1 + num2
    else:
        correct_answer = num1 - num2
    problem_text = f"{num1} {op} {num2} = ?"
    # Display question number and problem
    Label(root, text=f"Question {question_num} of 10", font=("Arial", 14, "bold"), bg=WHITE, fg=HOT_PINK).pack(pady=13)
    Label(root, text=problem_text, font=("Arial", 22, "bold"), bg=PINK, fg=TEXT).pack(pady=13)
    # Entry for user's answer
    user_answer_entry = Entry(root, width=15, font=("Arial", 18), bg=WHITE, fg=TEXT, justify="center")
    user_answer_entry.pack(pady=10)
    user_answer_entry.focus_set()
    # Submit answer button
    Button(root, text="Submit", font=("Arial", 15, "bold"), bg=HOT_PINK, fg=WHITE, command=check_answer).pack(pady=10)

def check_answer():
    """Checks the user's answer, updates score, and gives feedback."""
    global first_try, score
    user_input = user_answer_entry.get()
    try:
        user_val = int(user_input)
    except ValueError:
        messagebox.showinfo("Invalid", "Please enter a valid integer.")
        return
    if isCorrect(user_val):
        score += 10 if first_try else 5
        messagebox.showinfo("Correct!", "That's correct! 🌸")
        next_question()
    else:
        if first_try:
            first_try = False
            messagebox.showinfo("Incorrect", "Wrong answer. Try again!")
            displayProblem()
        else:
            messagebox.showinfo("Incorrect", f"Sorry, the correct answer was {correct_answer}.")
            next_question()

def isCorrect(answer):
    """Returns True if the user's answer matches the correct answer."""
    return answer == correct_answer

def displayResults():
    """Displays the final score and rank, and prompts to play again or exit, with background image and pink/white theme."""
    clear_window()
    # Create background label and stretch it
    bg_label = Label(root, image=bg_img)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    grade = rank(score)
    # Display results, score, and grade
    Label(root, text="Quiz Complete!", font=("Arial", 18, "bold"), bg=PINK, fg=WHITE).pack(pady=16)
    Label(root, text=f"Your score: {score} / 100", font=("Arial", 15), bg=WHITE, fg=HOT_PINK).pack(pady=8)
    Label(root, text=f"Rank: {grade}", font=("Arial", 15), bg=WHITE, fg=TEXT).pack(pady=8)
    # Play again / exit buttons
    Button(root, text="Play Again", font=("Arial", 15, "bold"), bg=PINK, fg=TEXT, command=displayMenu).pack(pady=10)
    Button(root, text="Exit", font=("Arial", 15, "bold"), bg=HOT_PINK, fg=WHITE, command=root.quit).pack(pady=8)

def rank(score):
    """Returns a rank string based on the user's score."""
    if score >= 90: return "A+"
    elif score >= 80: return "A"
    elif score >= 70: return "B"
    elif score >= 60: return "C"
    elif score >= 50: return "D"
    else: return "F"

# Start the quiz by displaying the menu
displayMenu()
root.mainloop()