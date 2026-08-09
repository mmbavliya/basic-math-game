import random
import tkinter as tk
from tkinter import font

class MathKidsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌟 Kids Math Learning Adventure 🌟")
        self.root.geometry("660x820")
        self.root.resizable(True, True)
        self.root.minsize(620, 780)
        
        self.BG_COLOR = "#F0F8FF"
        self.CARD_BG = "#FFFFFF"
        self.PRIMARY_COLOR = "#6C5CE7"
        self.SECONDARY_COLOR = "#00CEC9"
        self.CORRECT_COLOR = "#00B894"
        self.ACCENT_YELLOW = "#FDCB6E"
        self.TEXT_COLOR = "#2D3436"
        
        self.root.configure(bg=self.BG_COLOR)
        
        self.score = 0
        self.streak = 0
        self.stars = 0
        self.current_num1 = 0
        self.current_num2 = 0
        self.current_operator = "+"
        self.correct_answer = 0
        self.mode = "+"
        self.difficulty = "easy"
        
        self.mode_var = tk.StringVar(value="+")
        self.diff_var = tk.StringVar(value="easy")
        
        self.title_font = font.Font(family="Comic Sans MS", size=20, weight="bold")
        self.header_font = font.Font(family="Comic Sans MS", size=13, weight="bold")
        self.problem_font = font.Font(family="Comic Sans MS", size=42, weight="bold")
        self.button_font = font.Font(family="Comic Sans MS", size=13, weight="bold")
        self.numpad_font = font.Font(family="Comic Sans MS", size=15, weight="bold")
        self.feedback_font = font.Font(family="Comic Sans MS", size=14, weight="bold")
        
        self._build_ui()
        self._generate_new_question()

    def _build_ui(self):
        header_frame = tk.Frame(self.root, bg=self.PRIMARY_COLOR, pady=8)
        header_frame.pack(fill="x")
        
        title_label = tk.Label(header_frame, text="★ Math Learning Adventure ★", font=self.title_font, bg=self.PRIMARY_COLOR, fg="#FFFFFF")
        title_label.pack()
        
        stats_frame = tk.Frame(self.root, bg=self.BG_COLOR, pady=6)
        stats_frame.pack(fill="x", padx=15)
        
        self.score_label = tk.Label(stats_frame, text="Score: 0", font=self.header_font, bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        self.score_label.pack(side="left", expand=True)
        
        self.streak_label = tk.Label(stats_frame, text="Streak: 0", font=self.header_font, bg=self.BG_COLOR, fg="#D63031")
        self.streak_label.pack(side="left", expand=True)
        
        self.stars_label = tk.Label(stats_frame, text="Stars: 0", font=self.header_font, bg=self.BG_COLOR, fg="#E17055")
        self.stars_label.pack(side="left", expand=True)
        
        controls_frame = tk.Frame(self.root, bg=self.BG_COLOR, pady=2)
        controls_frame.pack(fill="x", padx=15)
        
        mode_frame = tk.LabelFrame(controls_frame, text=" Select Mode ", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=("Comic Sans MS", 10, "bold"))
        mode_frame.pack(side="left", padx=8, fill="y")
        
        modes = [("+ Add", "+"), ("- Sub", "-"), ("× Multiply", "*"), ("🎲 Mixed", "mixed")]
        for text, m in modes:
            rb = tk.Radiobutton(mode_frame, text=text, value=m, variable=self.mode_var, command=lambda val=m: self._change_mode(val), bg=self.BG_COLOR, activebackground=self.BG_COLOR, font=("Comic Sans MS", 10, "bold"))
            rb.pack(anchor="w", padx=4, pady=1)
                
        diff_frame = tk.LabelFrame(controls_frame, text=" Difficulty ", bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=("Comic Sans MS", 10, "bold"))
        diff_frame.pack(side="right", padx=8, fill="y")
        
        diffs = [("Easy (1-10)", "easy"), ("Medium (1-20)", "medium"), ("Hard (1-50)", "hard")]
        for text, d in diffs:
            rb = tk.Radiobutton(diff_frame, text=text, value=d, variable=self.diff_var, command=lambda val=d: self._change_difficulty(val), bg=self.BG_COLOR, activebackground=self.BG_COLOR, font=("Comic Sans MS", 10, "bold"))
            rb.pack(anchor="w", padx=4, pady=1)

        self.card_frame = tk.Frame(self.root, bg=self.CARD_BG, relief="ridge", bd=3, pady=10, padx=15)
        self.card_frame.pack(padx=20, pady=10, fill="x")
        
        self.problem_label = tk.Label(self.card_frame, text="7 + 5 = ?", font=self.problem_font, bg=self.CARD_BG, fg=self.PRIMARY_COLOR)
        self.problem_label.pack(pady=5)
        
        entry_frame = tk.Frame(self.card_frame, bg=self.CARD_BG)
        entry_frame.pack(pady=4)
        
        self.answer_var = tk.StringVar()
        self.answer_entry = tk.Entry(entry_frame, textvariable=self.answer_var, font=font.Font(family="Comic Sans MS", size=22, weight="bold"), width=6, justify="center", bd=3, relief="solid")
        self.answer_entry.pack(side="left", padx=10)
        self.answer_entry.focus()
        
        self.root.bind("<Return>", lambda event: self._check_answer())
        
        numpad_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        numpad_frame.pack(pady=6)
        
        buttons = [('7', '8', '9'), ('4', '5', '6'), ('1', '2', '3'), ('C', '0', '⌫')]
        for row_idx, row in enumerate(buttons):
            for col_idx, char in enumerate(row):
                btn_color = self.ACCENT_YELLOW if char not in ('C', '⌫') else "#FAB1A0"
                btn = tk.Button(numpad_frame, text=char, font=self.numpad_font, width=4, height=1, bg=btn_color, activebackground=self.SECONDARY_COLOR, command=lambda c=char: self._numpad_click(c))
                btn.grid(row=row_idx, column=col_idx, padx=5, pady=3)
                
        action_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        action_frame.pack(pady=8)
        
        self.submit_btn = tk.Button(action_frame, text="🚀 Submit Answer!", font=self.button_font, bg=self.CORRECT_COLOR, fg="#FFFFFF", padx=12, pady=4, bd=0, relief="raised", command=self._check_answer)
        self.submit_btn.pack(side="left", padx=8)
        
        self.skip_btn = tk.Button(action_frame, text="⏩ Skip Question", font=font.Font(family="Comic Sans MS", size=11, weight="bold"), bg="#B2BEC3", fg="#FFFFFF", padx=10, pady=4, command=self._generate_new_question)
        self.skip_btn.pack(side="left", padx=8)
        
        self.feedback_label = tk.Label(self.root, text="Type your answer and press Submit!", font=self.feedback_font, bg=self.BG_COLOR, fg=self.TEXT_COLOR)
        self.feedback_label.pack(pady=6)

    def _change_mode(self, new_mode):
        self.mode = new_mode
        self._generate_new_question()

    def _change_difficulty(self, new_diff):
        self.difficulty = new_diff
        self._generate_new_question()

    def _numpad_click(self, char):
        if char == 'C':
            self.answer_var.set("")
        elif char == '⌫':
            current = self.answer_var.get()
            self.answer_var.set(current[:-1])
        else:
            if len(self.answer_var.get()) < 5:
                self.answer_var.set(self.answer_var.get() + char)

    def _generate_new_question(self):
        self.answer_var.set("")
        self.answer_entry.focus()
        
        if self.difficulty == "easy":
            max_num = 10
        elif self.difficulty == "medium":
            max_num = 20
        else:
            max_num = 50

        if self.mode == "mixed":
            op = random.choice(["+", "-", "*"])
        else:
            op = self.mode

        self.current_operator = op

        if op == "+":
            self.current_num1 = random.randint(1, max_num)
            self.current_num2 = random.randint(1, max_num)
            self.correct_answer = self.current_num1 + self.current_num2
            display_op = "+"
        elif op == "-":
            n1 = random.randint(1, max_num)
            n2 = random.randint(1, max_num)
            self.current_num1 = max(n1, n2)
            self.current_num2 = min(n1, n2)
            self.correct_answer = self.current_num1 - self.current_num2
            display_op = "−"
        elif op == "*":
            m_max = 10 if self.difficulty != "hard" else 12
            self.current_num1 = random.randint(1, m_max)
            self.current_num2 = random.randint(1, 10)
            self.correct_answer = self.current_num1 * self.current_num2
            display_op = "×"

        self.problem_label.config(text=f"{self.current_num1} {display_op} {self.current_num2} = ?")

    def _check_answer(self):
        user_input = self.answer_var.get().strip()
        if not user_input:
            self.feedback_label.config(text="Please enter an answer! ✏️", fg="#D63031")
            return
            
        try:
            val = int(user_input)
        except ValueError:
            self.feedback_label.config(text="Numbers only, please! 😊", fg="#D63031")
            return

        if val == self.correct_answer:
            self.streak += 1
            self.stars += 1
            added_score = 10 * (1 + (self.streak // 3))
            self.score += added_score
            
            encouragements = ["Super Star! Correct!", "Awesome Job!", "On Fire! Keep Going!", "Fantastic Math Skills!", "Bingo! You Got It!"]
            msg = random.choice(encouragements)
            if self.streak >= 3:
                msg += f" (Streak x{self.streak} Bonus!)"
                
            self.feedback_label.config(text=msg, fg=self.CORRECT_COLOR)
            self._update_scoreboard()
            self._generate_new_question()
        else:
            self.streak = 0
            self.feedback_label.config(text=f"Oops! {self.current_num1} {self.current_operator} {self.current_num2} is {self.correct_answer}. Try next one!", fg="#D63031")
            self._update_scoreboard()
            self._generate_new_question()

    def _update_scoreboard(self):
        self.score_label.config(text=f"Score: {self.score}")
        self.streak_label.config(text=f"Streak: 🔥 {self.streak}")
        self.stars_label.config(text=f"Stars: ⭐ {self.stars}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MathKidsApp(root)
    root.mainloop()
