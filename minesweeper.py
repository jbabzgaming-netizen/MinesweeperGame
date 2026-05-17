import tkinter as tk

class SimpleMinesweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.rows = 10
        self.cols = 10
        self.create_widgets()

    def create_widgets(self):
        # draw the board
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(self.root, width=3, height=1)
                btn.grid(row=r, column=c)

if __name__ == "__main__":
    root = tk.Tk()
    game = SimpleMinesweeper(root)
    root.mainloop()