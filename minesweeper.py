import tkinter as tk
from tkinter import messagebox, simpledialog  
import random

class MinesweeperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.root.resizable(False, False)
        
        # default settings
        self.rows = 10
        self.cols = 10
        self.num_mines = 10
        
        # dark background theme
        self.root.configure(bg="#2b2b2b")
        
        self.menu_frame = tk.Frame(self.root, padx=50, pady=40, bg="#2b2b2b")
        self.game_frame = tk.Frame(self.root)
        
        self.show_menu()

    def show_menu(self):
        self.game_frame.pack_forget()
        for widget in self.game_frame.winfo_children():
            widget.destroy()
            
        self.menu_frame.pack()
        
        if not self.menu_frame.winfo_children():
            # main title
            title_label = tk.Label(
                self.menu_frame, 
                text="MINESWEEPER", 
                font=("Helvetica", 24, "bold"), 
                bg="#2b2b2b",   
                fg="#ffcc00"    
            )
            title_label.pack(pady=(0, 30))
            
            # reusable button style
            btn_style = {
                "width": 15,
                "font": ("Helvetica", 12, "bold"),
                "bg": "#4a4a4a",              
                "fg": "white",                
                "activebackground": "#ffcc00", 
                "activeforeground": "black",
                "cursor": "hand2",            
                "relief": tk.RAISED,
                "bd": 3
            }
            
            btn_start = tk.Button(self.menu_frame, text="Start Game", command=self.start_game, **btn_style)
            btn_start.pack(pady=8)
            
            btn_scores = tk.Button(self.menu_frame, text="Highscores", command=self.show_highscores, **btn_style)
            btn_scores.pack(pady=8)
            
            btn_settings = tk.Button(self.menu_frame, text="Settings", command=self.show_settings, **btn_style)
            btn_settings.pack(pady=8)
            
            btn_exit = tk.Button(self.menu_frame, text="Exit", command=self.root.destroy, **btn_style)
            btn_exit.pack(pady=8)

    def start_game(self):
        self.menu_frame.pack_forget()
        self.game_frame.pack()
        MinesweeperGame(self.game_frame, self.show_menu, self.rows, self.cols, self.num_mines)

    def show_highscores(self):
        messagebox.showinfo("Highscores", "Feature coming soon!\n\n1. 99 seconds\n2. 145 seconds\n3. 210 seconds")

    def show_settings(self):
        # ask user for custom grid size
        try:
            r_str = simpledialog.askstring("Settings", "Enter number of rows (e.g. 10):", parent=self.root)
            if r_str is None: return  
            r = int(r_str)  

            c_str = simpledialog.askstring("Settings", "Enter number of columns (e.g. 10):", parent=self.root)
            if c_str is None: return
            c = int(c_str)

            m_str = simpledialog.askstring("Settings", "Enter number of mines (e.g. 15):", parent=self.root)
            if m_str is None: return
            m = int(m_str)

            if m >= (r * c):
                raise ValueError("Too many mines!")
            if r < 5 or c < 5:
                raise ValueError("Grid is too small!")

            self.rows = r
            self.cols = c
            self.num_mines = m
            messagebox.showinfo("Success", f"Grid updated to {r}x{c} with {m} mines.")

        except ValueError as e:
            # handle invalid inputs safely
            error_msg = str(e)
            if "invalid literal" in error_msg:
                error_msg = "Please enter numbers only!"
            
            messagebox.showerror("Input Error", f"{error_msg}\n\nResetting to default.")
            self.rows = 10
            self.cols = 10
            self.num_mines = 10

class MinesweeperGame:
    def __init__(self, parent_frame, back_to_menu_callback, rows, cols, num_mines):
        self.parent = parent_frame
        self.back_to_menu = back_to_menu_callback
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        
        self.buttons = {}
        self.mines = set()
        self.flags = set()
        self.clicked = set()
        self.game_over = False

        self.create_widgets()
        self.place_mines()

    def create_widgets(self):
        control_frame = tk.Frame(self.parent)
        control_frame.pack(pady=5)
        
        back_btn = tk.Button(control_frame, text="< Menu", command=self.back_to_menu)
        back_btn.grid(row=0, column=0, padx=5)
        
        restart_btn = tk.Button(control_frame, text="Restart", command=self.restart)
        restart_btn.grid(row=0, column=1, padx=5)

        self.grid_frame = tk.Frame(self.parent)
        self.grid_frame.pack(padx=10, pady=(0, 10))

        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(
                    self.grid_frame, 
                    width=3, 
                    height=1, 
                    font=("Arial", 12, "bold"),
                    command=lambda r=r, c=c: self.on_left_click(r, c)
                )
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.on_right_click(r, c))
                btn.grid(row=r, column=c)
                self.buttons[(r, c)] = btn

    def place_mines(self):
        positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        self.mines = set(random.sample(positions, self.num_mines))

    def get_neighbors(self, r, c):
        neighbors = []
        for i in range(r-1, r+2):
            for j in range(c-1, c+2):
                if 0 <= i < self.rows and 0 <= j < self.cols and (i, j) != (r, c):
                    neighbors.append((i, j))
        return neighbors

    def count_adjacent_mines(self, r, c):
        return sum(1 for nr, nc in self.get_neighbors(r, c) if (nr, nc) in self.mines)

    def on_left_click(self, r, c):
        if self.game_over or (r, c) in self.flags or (r, c) in self.clicked:
            return

        if (r, c) in self.mines:
            self.game_over = True
            self.buttons[(r, c)].config(text="*", bg="red")
            self.reveal_all_mines()
            messagebox.showinfo("Game Over", "Boom! You hit a mine.")
        else:
            self.reveal_cell(r, c)
            self.check_win()

    def reveal_cell(self, r, c):
        if (r, c) in self.clicked or (r, c) in self.flags:
            return
        
        self.clicked.add((r, c))
        mines_around = self.count_adjacent_mines(r, c)
        
        self.buttons[(r, c)].config(state="disabled", relief=tk.SUNKEN, bg="lightgrey")
        
        if mines_around > 0:
            colors = {1: "blue", 2: "green", 3: "red", 4: "purple", 5: "maroon", 6: "turquoise", 7: "black", 8: "gray"}
            self.buttons[(r, c)].config(text=str(mines_around), disabledforeground=colors.get(mines_around, "black"))
        else:
            for nr, nc in self.get_neighbors(r, c):
                self.reveal_cell(nr, nc)

    def on_right_click(self, r, c):
        if self.game_over or (r, c) in self.clicked:
            return

        if (r, c) in self.flags:
            self.flags.remove((r, c))
            self.buttons[(r, c)].config(text="", bg="SystemButtonFace")
        else:
            self.flags.add((r, c))
            self.buttons[(r, c)].config(text="🚩", fg="red")

    def reveal_all_mines(self):
        for (r, c) in self.mines:
            if (r, c) not in self.flags:
                self.buttons[(r, c)].config(text="*", bg="red")
            elif (r, c) in self.flags and (r, c) not in self.mines:
                self.buttons[(r, c)].config(bg="orange")

    def check_win(self):
        if len(self.clicked) == (self.rows * self.cols) - self.num_mines:
            self.game_over = True
            self.reveal_all_mines()
            messagebox.showinfo("Congratulations", "You cleared the minefield!")

    def restart(self):
        self.grid_frame.destroy()
        self.clicked.clear()
        self.flags.clear()
        self.mines.clear()
        self.game_over = False
        self.create_widgets()
        self.place_mines()

if __name__ == "__main__":
    root = tk.Tk()
    app = MinesweeperApp(root)
    root.mainloop()