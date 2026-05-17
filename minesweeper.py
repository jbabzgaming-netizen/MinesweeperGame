import tkinter as tk
from tkinter import messagebox
import random

class MinesweeperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.menu_frame = tk.Frame(self.root, padx=20, pady=20)
        self.game_frame = tk.Frame(self.root)
        self.show_menu()

    def show_menu(self):
        # clear game and show menu
        self.game_frame.pack_forget()
        for widget in self.game_frame.winfo_children(): widget.destroy()
        self.menu_frame.pack()
        if not self.menu_frame.winfo_children():
            tk.Label(self.menu_frame, text="MINESWEEPER", font=("Arial", 20, "bold")).pack(pady=20)
            tk.Button(self.menu_frame, text="Start Game", width=15, command=self.start_game).pack(pady=5)
            tk.Button(self.menu_frame, text="Exit", width=15, command=self.root.destroy).pack(pady=5)

    def start_game(self):
        self.menu_frame.pack_forget()
        self.game_frame.pack()
        MinesweeperGame(self.game_frame, self.show_menu, 10, 10, 10)

class MinesweeperGame:
    def __init__(self, parent, back_cb, rows, cols, num_mines):
        self.parent = parent
        self.back_to_menu = back_cb
        self.rows, self.cols, self.num_mines = rows, cols, num_mines
        self.buttons, self.mines, self.flags, self.clicked = {}, set(), set(), set()
        self.game_over = False
        self.create_widgets()
        self.place_mines()

    def create_widgets(self):
        tk.Button(self.parent, text="< Menu", command=self.back_to_menu).pack(pady=5)
        self.grid_frame = tk.Frame(self.parent)
        self.grid_frame.pack()
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(self.grid_frame, width=3, height=1)
                btn.bind("<Button-1>", lambda e, r=r, c=c: self.left_click(r, c))
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.right_click(r, c))
                btn.grid(row=r, column=c)
                self.buttons[(r, c)] = btn

    def place_mines(self):
        positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        self.mines = set(random.sample(positions, self.num_mines))

    def get_neighbors(self, r, c):
        return [(i, j) for i in range(r-1, r+2) for j in range(c-1, c+2) if 0<=i<self.rows and 0<=j<self.cols and (i,j)!=(r,c)]

    def left_click(self, r, c):
        if self.game_over or (r, c) in self.clicked or (r, c) in self.flags: return
        if (r, c) in self.mines:
            self.game_over = True
            for mr, mc in self.mines: self.buttons[(mr, mc)].config(text="*", bg="red")
            messagebox.showinfo("Game Over", "Boom! You hit a mine.")
        else:
            self.reveal(r, c)
            self.check_win()

    def right_click(self, r, c):
        if self.game_over or (r, c) in self.clicked: return
        if (r, c) in self.flags:
            self.flags.remove((r, c)); self.buttons[(r, c)].config(text="")
        else:
            self.flags.add((r, c)); self.buttons[(r, c)].config(text="🚩", fg="red")

    def reveal(self, r, c):
        if (r, c) in self.clicked or (r, c) in self.flags: return
        self.clicked.add((r, c))
        self.buttons[(r, c)].config(state="disabled", relief=tk.SUNKEN, bg="lightgrey")
        mines_around = sum(1 for nr, nc in self.get_neighbors(r, c) if (nr, nc) in self.mines)
        if mines_around > 0: self.buttons[(r, c)].config(text=str(mines_around))
        else:
            for nr, nc in self.get_neighbors(r, c): self.reveal(nr, nc)

    def check_win(self):
        if len(self.clicked) == (self.rows * self.cols) - self.num_mines:
            self.game_over = True
            messagebox.showinfo("Win", "Congratulations, You cleared the field!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MinesweeperApp(root)
    root.mainloop()