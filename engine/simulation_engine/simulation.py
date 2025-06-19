import random
from .cell import Plant, Predator, Herbivore, Fungus, Omnivore

XSIZE = 60
YSIZE = 30


class Simulation:
    def __init__(self):
        self.grid = None
        self.cells = None
        self.reset()

    def reset(self):
        self.grid = [[None for _ in range(XSIZE)] for _ in range(YSIZE)]
        self.cells = []
        for _ in range(100):
            x, y = random.randint(0, XSIZE - 1), random.randint(0, YSIZE - 1)
            if self.grid[y][x] is None:
                rand = random.random()
                if rand < 0.59:
                    cell = Plant(x, y)
                elif rand < 0.74:
                    cell = Herbivore(x, y)
                elif rand < 0.83:
                    cell = Predator(x, y)
                elif rand < 0.90:
                    cell = Fungus(x, y)
                else:
                    cell = Omnivore(x, y)

                self.grid[y][x] = cell
                self.cells.append(cell)

    def add_plants(self):
        x, y = random.randint(0, XSIZE - 1), random.randint(0, YSIZE - 1)
        if self.grid[y][x] is None:
            cell = Plant(x, y)
            self.grid[y][x] = cell
            self.cells.append(cell)

    def update(self):
        new_cells = []
        dead_cells = []

        for cell in self.cells[:]:  # Делаем копию списка для итерации
            # Проверяем, что клетка все еще существует в сетке
            if self.grid[cell.y][cell.x] != cell:
                dead_cells.append(cell)
                continue

            alive, child = cell.update(self.grid)
            if not alive:
                dead_cells.append(cell)
            if child:
                # Проверяем, что ребенок действительно добавлен в сетку
                if self.grid[child.y][child.x] == child:
                    new_cells.append(child)

        # Удаляем мертвые клетки
        for cell in dead_cells:
            if cell in self.cells:  # Проверка на случай, если клетка уже удалена
                self.cells.remove(cell)
                # Убедимся, что клетка удалена из сетки
                if 0 <= cell.y < YSIZE and 0 <= cell.x < XSIZE and self.grid[cell.y][cell.x] == cell:
                    self.grid[cell.y][cell.x] = None

        # Добавляем новые клетки (уже проверено, что они в сетке)
        self.cells.extend(new_cells)

        if random.random() < 0.5:
            self.add_plants()

# Создаем глобальный экземпляр симуляции
simulation_instance = Simulation()
