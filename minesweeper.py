import tkinter as tk
import random

class SimpleMinesweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.rows = 10
        self.cols = 10
        self.num_mines = 10
        self.buttons = {}
        self.mines = set()
        
        self.create_widgets()
        self.place_mines()

    def create_widgets(self):
        # build grid and bind left click
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(self.root, width=3, height=1)
                btn.bind("<Button-1>", lambda e, r=r, c=c: self.left_click(r, c))
                btn.grid(row=r, column=c)
                self.buttons[(r, c)] = btn

    def place_mines(self):
        # scatter mines
        positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        self.mines = set(random.sample(positions, self.num_mines))

    def get_neighbors(self, r, c):
        # find adjacent squares
        neighbors = []
        for i in range(r-1, r+2):
            for j in range(c-1, c+2):
                if 0 <= i < self.rows and 0 <= j < self.cols and (i, j) != (r, c):
                    neighbors.append((i, j))
        return neighbors

    def left_click(self, r, c):
        # check if clicked a mine
        if (r, c) in self.mines:
            self.buttons[(r, c)].config(text="*", bg="red")
        else:
            mines_around = sum(1 for nr, nc in self.get_neighbors(r, c) if (nr, nc) in self.mines)
            self.buttons[(r, c)].config(text=str(mines_around) if mines_around > 0 else "")

if __name__ == "__main__":
    root = tk.Tk()
    game = SimpleMinesweeper(root)
    root.mainloop()