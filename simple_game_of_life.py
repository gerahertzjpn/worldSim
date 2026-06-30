"""
Simple Conway's Game of Life
Запуск:
    python simple_game_of_life.py

Управление:
    Space  — старт / пауза
    ЛКМ    — поставить живую клетку
    ПКМ    — удалить клетку
    G      — поставить glider, который "ползёт" по полю
    R      — случайное поле
    C      — очистить поле
    + / -  — быстрее / медленнее
"""

import random
import tkinter as tk


CELL_SIZE = 12
COLS = 70
ROWS = 45
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

ALIVE = 1
DEAD = 0


class GameOfLife:
    def __init__(self, root):
        self.root = root
        self.root.title("Conway's Game of Life")

        self.grid = [[DEAD for _ in range(COLS)] for _ in range(ROWS)]
        self.running = True
        self.generation = 0
        self.speed_ms = 120

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()

        self.info = tk.Label(
            root,
            text="Space: pause/start | ЛКМ: draw | ПКМ: erase | G: glider | R: random | C: clear | +/-: speed",
            font=("Arial", 10)
        )
        self.info.pack()

        self.stats = tk.Label(root, text="", font=("Arial", 10))
        self.stats.pack()

        self.canvas.bind("<Button-1>", self.draw_cell)
        self.canvas.bind("<B1-Motion>", self.draw_cell)
        self.canvas.bind("<Button-3>", self.erase_cell)
        self.canvas.bind("<B3-Motion>", self.erase_cell)

        self.root.bind("<space>", self.toggle_running)
        self.root.bind("g", self.place_glider_key)
        self.root.bind("G", self.place_glider_key)
        self.root.bind("r", self.randomize_key)
        self.root.bind("R", self.randomize_key)
        self.root.bind("c", self.clear_key)
        self.root.bind("C", self.clear_key)
        self.root.bind("+", self.speed_up)
        self.root.bind("-", self.slow_down)

        # Стартовый glider, чтобы сразу было видно "движение"
        self.place_glider(5, 5)

        self.update()

    def draw_cell(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        if 0 <= row < ROWS and 0 <= col < COLS:
            self.grid[row][col] = ALIVE
            self.draw_grid()

    def erase_cell(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        if 0 <= row < ROWS and 0 <= col < COLS:
            self.grid[row][col] = DEAD
            self.draw_grid()

    def toggle_running(self, event=None):
        self.running = not self.running

    def place_glider_key(self, event=None):
        # Ставим glider примерно в левый верхний угол
        self.place_glider(5, 5)
        self.draw_grid()

    def randomize_key(self, event=None):
        self.grid = [
            [ALIVE if random.random() < 0.25 else DEAD for _ in range(COLS)]
            for _ in range(ROWS)
        ]
        self.generation = 0
        self.draw_grid()

    def clear_key(self, event=None):
        self.grid = [[DEAD for _ in range(COLS)] for _ in range(ROWS)]
        self.generation = 0
        self.draw_grid()

    def speed_up(self, event=None):
        self.speed_ms = max(20, self.speed_ms - 20)

    def slow_down(self, event=None):
        self.speed_ms = min(1000, self.speed_ms + 20)

    def place_glider(self, row, col):
        """
        Glider — маленькая фигура, которая из-за правил Game of Life
        визуально движется по диагонали.
        """
        pattern = [
            (0, 1),
            (1, 2),
            (2, 0),
            (2, 1),
            (2, 2),
        ]

        for dr, dc in pattern:
            r = row + dr
            c = col + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                self.grid[r][c] = ALIVE

    def count_neighbors(self, row, col):
        count = 0

        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue

                nr = row + dr
                nc = col + dc

                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    count += self.grid[nr][nc]

        return count

    def next_generation(self):
        new_grid = [[DEAD for _ in range(COLS)] for _ in range(ROWS)]

        for row in range(ROWS):
            for col in range(COLS):
                neighbors = self.count_neighbors(row, col)
                cell = self.grid[row][col]

                if cell == ALIVE:
                    # Живая клетка выживает, если у неё 2 или 3 соседа
                    if neighbors == 2 or neighbors == 3:
                        new_grid[row][col] = ALIVE
                    else:
                        new_grid[row][col] = DEAD
                else:
                    # Мёртвая клетка рождается, если у неё ровно 3 соседа
                    if neighbors == 3:
                        new_grid[row][col] = ALIVE

        self.grid = new_grid
        self.generation += 1

    def draw_grid(self):
        self.canvas.delete("all")

        for row in range(ROWS):
            for col in range(COLS):
                x1 = col * CELL_SIZE
                y1 = row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                if self.grid[row][col] == ALIVE:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="gray")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="#eeeeee")

        alive_cells = sum(sum(row) for row in self.grid)
        state = "идёт" if self.running else "пауза"
        self.stats.config(
            text=f"Поколение: {self.generation} | Живых клеток: {alive_cells} | Состояние: {state} | Скорость: {self.speed_ms} ms"
        )

    def update(self):
        if self.running:
            self.next_generation()

        self.draw_grid()
        self.root.after(self.speed_ms, self.update)


def main():
    root = tk.Tk()
    GameOfLife(root)
    root.mainloop()


if __name__ == "__main__":
    main()
