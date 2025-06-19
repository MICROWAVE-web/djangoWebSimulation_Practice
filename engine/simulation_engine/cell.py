import random

import torch
import torch.nn as nn
import torch.nn.functional as F

# константы

ROWS = 30
COLS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BACKGROUND = (240, 240, 240)

# Настройки симуляции
INITIAL_CELLS = 100
MAX_ENERGY = 100

REPRODUCTION_COST = 40 # Можно изменить через панель

PHOTOSYNTHESIS_ENERGY = 2  # Можно изменить через панель

MOVEMENT_COST = 1
PREDATION_ENERGY = 20


class Brain(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(6, 8)
        self.fc2 = nn.Linear(8, 4)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        return torch.sigmoid(self.fc2(x))


class Cell:
    def __init__(self, x, y, genome=None):
        self.x = x
        self.y = y
        self.energy = MAX_ENERGY // 2
        self.age = 0
        self.genome = genome if genome else self.random_genome()
        self.brain = genome['brain'] if genome and 'brain' in genome else Brain()

        self.direction = random.randint(0, 3)  # 0: up, 1: right, 2: down, 3: left

    def random_genome(self):
        return {
            'photosynthesis': random.random(),
            'speed': random.random(),
            'sense_distance': random.randint(1, 5),
            'reproduction_rate': random.random() * 0.1
        }

    def decide_action(self):
        # Примитивные входные данные
        input_data = torch.tensor([
            self.energy / MAX_ENERGY,
            self.age / 100,
            self.genome['photosynthesis'],
            self.genome['speed'],
            self.genome['sense_distance'] / 5,
            self.genome['reproduction_rate']
        ], dtype=torch.float32)

        output = self.brain(input_data)
        return output  # вернёт тензор с 4 числами от 0 до 1

    def mutate(self, new_genome, mutation_rate=0.1):
        new_brain = Brain()
        new_brain.load_state_dict(self.brain.state_dict())

        # Мутируем веса нейросети
        with torch.no_grad():
            for param in new_brain.parameters():
                if random.random() < mutation_rate:
                    param += 0.15 * torch.randn_like(param)

        new_genome['brain'] = new_brain

        # Мутируем другие гены
        for gene in new_genome:
            if gene == 'brain':
                continue

            if random.random() < mutation_rate:

                if gene in ['sense_distance']:
                    # Для дистанции чутья - мутация в пределах 1-5
                    if gene == 'sense_distance':
                        new_value = new_genome[gene] + random.randint(-1, 1)
                        new_genome[gene] = max(1, min(5, new_value))
                    else:
                        new_genome[gene] += random.randint(-1, 1)
                elif gene in ['photosynthesis', 'speed', 'reproduction_rate']:
                    # Для скорости - ограничение по типу организма
                    if gene == 'speed':
                        min_speed, max_speed = 0, 1
                        if isinstance(self, Plant):
                            max_speed = 0.3
                        elif isinstance(self, Fungus):
                            max_speed = 0.1
                        elif isinstance(self, Predator):
                            min_speed = 0.5

                        change = random.uniform(-0.2, 0.2)
                        new_value = new_genome[gene] + change
                        new_genome[gene] = max(min_speed, min(max_speed, new_value))
                    if gene == 'photosynthesis':
                        min_photosynthesis, max_photosynthesis = 0, 1
                        if type(self) in [Predator, Herbivore, Omnivore]:
                            max_photosynthesis = 0.1

                        change = random.uniform(-0.2, 0.2)
                        new_value = new_genome[gene] + change
                        new_genome[gene] = max(min_photosynthesis, min(max_photosynthesis, new_value))
                    else:
                        change = random.uniform(-0.2, 0.2)
                        new_genome[gene] = max(0, min(1, new_genome[gene] + change))
        return new_genome

    def move(self, grid):
        # Стоимость движения зависит от скорости
        movement_prob = self.genome['speed'] * 0.15
        if random.random() > movement_prob:
            return False

        self.energy -= MOVEMENT_COST

        # Попробовать двигаться в текущем направлении
        new_x, new_y = self.x, self.y
        if self.direction == 0 and self.y > 0:
            new_y -= 1
        elif self.direction == 1 and self.x < COLS - 1:
            new_x += 1
        elif self.direction == 2 and self.y < ROWS - 1:
            new_y += 1
        elif self.direction == 3 and self.x > 0:
            new_x -= 1

        # Если клетка пустая - двигаемся
        if grid[new_y][new_x] is None:
            grid[self.y][self.x] = None
            self.x, self.y = new_x, new_y
            grid[self.y][self.x] = self
            return True

        return False

    def get_light_level(self, _, y):
        # Освещение зависит от положения на экране (верх более освещен)
        return 1.0 - (y / ROWS) * 0.8

    def crossover_genome(self, other):
        new_genome = {}
        for gene in self.genome:
            if gene == 'brain':
                # Создаем гибридную нейросеть
                new_brain = Brain()
                child_state_dict = {}

                # Смешиваем веса от двух родителей
                for param_name, param in self.brain.named_parameters():
                    parent1_param = param.data
                    parent2_param = other.brain.state_dict()[param_name]

                    # Выбираем случайным образом от какого родителя взять вес
                    mask = torch.rand_like(parent1_param) < 0.5
                    child_param = torch.where(mask, parent1_param, parent2_param)
                    child_state_dict[param_name] = child_param

                new_brain.load_state_dict(child_state_dict)
                new_genome[gene] = new_brain
            elif gene in ['sense_distance']:
                # Для целых чисел - среднее значение с небольшим смещением
                base_value = (self.genome[gene] + other.genome[gene]) // 2
                new_genome[gene] = max(1, min(5, base_value + random.randint(-1, 1)))
            elif gene in ['photosynthesis', 'speed', 'reproduction_rate']:
                # Для вещественных чисел - среднее значение с небольшим смещением
                base_value = (self.genome[gene] + other.genome[gene]) / 2
                new_genome[gene] = max(0, min(1, base_value + random.uniform(-0.1, 0.1)))
                if type(self) in [Predator, Herbivore, Omnivore] and gene == 'photosynthesis':
                    new_genome[gene] = min(0.1, new_genome[gene])
        return new_genome

    def get_empty_neighbors(self, grid):
        neighbors = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < COLS and 0 <= ny < ROWS and (dx != 0 or dy != 0):
                    if grid[ny][nx] is None:
                        neighbors.append((nx, ny))
        return neighbors

    def reproduce(self, grid):
        # Определяем стоимость размножения для разных видов
        reproduction_costs = {
            Plant: REPRODUCTION_COST * 0.2,
            Fungus: REPRODUCTION_COST * 0.37,
            Herbivore: REPRODUCTION_COST * 0.2,
            Predator: REPRODUCTION_COST * 0.5,
            Omnivore: REPRODUCTION_COST * 0.5
        }

        cost = reproduction_costs.get(self.__class__, REPRODUCTION_COST)
        if self.energy < cost:
            return None

        # Вероятность размножения зависит от вида
        reproduction_rates = {
            Plant: 0.24,
            Fungus: 0.11,
            Herbivore: 0.35,
            Predator: 0.1,
            Omnivore: 0.14
        }

        base_prob = reproduction_rates.get(self.__class__, 0.1)
        age_factor = min(1.0, self.age / 40)
        energy_factor = self.energy / MAX_ENERGY
        reproduction_prob = base_prob * age_factor * energy_factor

        if random.random() > reproduction_prob:
            return None

        # Ищем пустую соседнюю клетку
        neighbors = self.get_empty_neighbors(grid)

        if not neighbors:
            return None

        spawn_nx, spawn_ny = random.choice(neighbors)
        self.energy -= cost // 2

        # Разные стратегии размножения для разных видов
        if isinstance(self, (Plant, Fungus)):
            # Бесполое размножение для растений и грибов
            child_genome = self.genome.copy()
            child_genome = self.mutate(child_genome, mutation_rate=0.08)
        else:
            # Половое размножение для животных
            partners = []
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    nx, ny = self.x + dx, self.y + dy
                    if 0 <= nx < COLS and 0 <= ny < ROWS and (dx != 0 or dy != 0):
                        neighbor = grid[ny][nx]
                        if neighbor and neighbor != self and isinstance(neighbor, self.__class__):
                            partners.append(neighbor)

            if partners:
                partner = random.choice(partners)
                child_genome = self.crossover_genome(partner)
                # Меньше мутаций при половом размножении
                child_genome = self.mutate(child_genome, mutation_rate=0.06)
            else:
                # Самооплодотворение, если партнер не найден
                child_genome = self.genome.copy()
                # Больше мутаций при самооплодотворении
                child_genome = self.mutate(child_genome, mutation_rate=0.12)

        # Создаем ребенка соответствующего типа
        if isinstance(self, Plant):
            child = Plant(spawn_nx, spawn_ny, child_genome)
        elif isinstance(self, Predator):
            child = Predator(spawn_nx, spawn_ny, child_genome)
        elif isinstance(self, Herbivore):
            child = Herbivore(spawn_nx, spawn_ny, child_genome)
        elif isinstance(self, Fungus):
            child = Fungus(spawn_nx, spawn_ny, child_genome)
        elif isinstance(self, Omnivore):
            child = Omnivore(spawn_nx, spawn_ny, child_genome)
        else:
            child = Cell(spawn_nx, spawn_ny, child_genome)

        child.energy = cost // 2
        grid[spawn_ny][spawn_nx] = child
        return child

    def update(self, grid):

        neighbors = self.get_empty_neighbors(grid)

        if neighbors:
            decision = self.decide_action()

            # Пример интерпретации: если первый выход > 0.5 — двигаться
            if decision[0] > 0.5 and self.sense_food(grid):
                self.move(grid)

            # Поворот в случайную сторону (или по второму выходу)
            if decision[1] > 0.66:
                self.direction = (self.direction + 1) % 4
            elif decision[1] < 0.33:
                self.direction = (self.direction - 1) % 4

        # Фотосинтез / охота
        self.eat(grid)

        # Попробовать размножиться, если третий выход достаточно высок
        child = None
        if neighbors and decision[2] > 0.40:
            child = self.reproduce(grid)
        self.age += 1

        if type(self) in [Herbivore]:
            self.energy -= 0.35  # Базальный метаболизм
        else:
            self.energy -= 0.5  # Базальный метаболизм

        # Умираем, если энергии нет
        if self.energy <= 0:
            grid[self.y][self.x] = None
            return False, child
        return True, child

    def eat(self, grid):
        pass

    def sense_food(self, grid):
        return False


class Plant(Cell):
    def __init__(self, x, y, genome=None):
        if genome is None:
            genome = self.random_genome()
        super().__init__(x, y, genome)

    def random_genome(self):
        return {
            'photosynthesis': random.random(),
            'speed': random.uniform(0, 0.3),
            'sense_distance': random.randint(1, 3),
            'reproduction_rate': random.uniform(0.05, 0.1)
        }

    def eat(self, grid):
        light_level = self.get_light_level(self.x, self.y)
        self.energy += light_level * self.genome['photosynthesis'] * PHOTOSYNTHESIS_ENERGY
        self.energy = min(self.energy, MAX_ENERGY)

    def sense_food(self, grid):
        sense_dist = self.genome['sense_distance']
        max_light = 0
        for dy in range(-sense_dist, sense_dist + 1):
            for dx in range(-sense_dist, sense_dist + 1):
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < COLS and 0 <= ny < ROWS:
                    light = self.get_light_level(nx, ny)
                    if light > max_light and (dx != 0 or dy != 0):
                        max_light = light
                        if abs(dx) > abs(dy):
                            self.direction = 1 if dx > 0 else 3
                        else:
                            self.direction = 2 if dy > 0 else 0
        return max_light > 0


class Predator(Cell):
    def __init__(self, x, y, genome=None):
        if genome is None:
            genome = self.random_genome()
        super().__init__(x, y, genome)

    def random_genome(self):
        return {
            'photosynthesis': random.uniform(0, 0.1),
            'speed': random.uniform(0.5, 1),
            'sense_distance': random.randint(2, 5),
            'reproduction_rate': random.uniform(0.01, 0.05)
        }

    def eat(self, grid):
        if not self.hunt(grid):
            light_level = self.get_light_level(self.x, self.y)
            self.energy += light_level * self.genome['photosynthesis'] * PHOTOSYNTHESIS_ENERGY
            self.energy = min(self.energy, MAX_ENERGY)

    def sense_food(self, grid):
        sense_dist = self.genome['sense_distance'] * 2
        closest_prey = None
        min_distance = float('inf')
        for dy in range(-sense_dist, sense_dist + 1):
            for dx in range(-sense_dist, sense_dist + 1):
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < COLS and 0 <= ny < ROWS and (dx != 0 or dy != 0):
                    cell = grid[ny][nx]
                    if cell and (type(cell) in [Herbivore, Omnivore] or random.random() < 0.1 and type(cell) == Plant):
                        distance = dx * dx + dy * dy
                        if distance < min_distance:
                            min_distance = distance
                            closest_prey = (dx, dy)
        if closest_prey:
            dx, dy = closest_prey
            if abs(dx) > abs(dy):
                self.direction = 1 if dx > 0 else 3
            else:
                self.direction = 2 if dy > 0 else 0
            return True
        return False

    def hunt(self, grid):
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < COLS and 0 <= ny < ROWS and (dx != 0 or dy != 0):
                    prey = grid[ny][nx]
                    if prey and (type(prey) in [Herbivore, Omnivore] or random.random() < 0.15 and type(prey) == Plant):
                        success_prob = self.genome['speed'] / (self.genome['speed'] + prey.genome['speed'] + 0.01)
                        if random.random() < success_prob:
                            self.energy += PREDATION_ENERGY
                            grid[ny][nx] = None
                            return True
        return False


class Herbivore(Cell):
    def __init__(self, x, y, genome=None):
        if genome is None:
            genome = self.random_genome()
        super().__init__(x, y, genome)

    def random_genome(self):
        return {
            'photosynthesis': random.uniform(0, 0.2),
            'speed': random.uniform(0.6, 0.9),
            'sense_distance': random.randint(4, 5),
            'reproduction_rate': random.uniform(0.03, 0.08)
        }

    def eat(self, grid):
        if not self.hunt(grid):
            light_level = self.get_light_level(self.x, self.y)
            self.energy += light_level * self.genome['photosynthesis'] * PHOTOSYNTHESIS_ENERGY
            self.energy = min(self.energy, MAX_ENERGY)

    def sense_food(self, grid):
        sense_dist = self.genome['sense_distance'] * 4  # Чуствительность еды для Травоядных
        closest_plant = None
        min_distance = float('inf')
        for dy in range(-sense_dist, sense_dist + 1):
            for dx in range(-sense_dist, sense_dist + 1):
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < COLS and 0 <= ny < ROWS and (dx != 0 or dy != 0):
                    cell = grid[ny][nx]
                    if cell and type(cell) is Plant:
                        distance = dx * dx + dy * dy
                        if distance < min_distance:
                            min_distance = distance
                            closest_plant = (dx, dy)
        if closest_plant:
            dx, dy = closest_plant
            if abs(dx) > abs(dy):
                self.direction = 1 if dx > 0 else 3
            else:
                self.direction = 2 if dy > 0 else 0
            return True
        return False

    def hunt(self, grid):
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < COLS and 0 <= ny < ROWS and (dx != 0 or dy != 0):
                    plant = grid[ny][nx]
                    if plant and type(plant) is Plant:
                        success_prob = self.genome['speed'] / (self.genome['speed'] + plant.genome['speed'] + 0.1)
                        if random.random() < success_prob:
                            self.energy += PREDATION_ENERGY // 2
                            grid[ny][nx] = None
                            return True
        return False


class Omnivore(Cell):
    def __init__(self, x, y, genome=None):
        if genome is None:
            genome = self.random_genome()
        super().__init__(x, y, genome)

    def random_genome(self):
        return {
            'photosynthesis': random.uniform(0.1, 0.4),
            'speed': random.uniform(0.4, 0.9),
            'sense_distance': random.randint(3, 5),
            'reproduction_rate': random.uniform(0.02, 0.06)
        }

    def eat(self, grid):
        if not self.hunt(grid):
            light_level = self.get_light_level(self.x, self.y)
            self.energy += light_level * self.genome['photosynthesis'] * PHOTOSYNTHESIS_ENERGY
            self.energy = min(self.energy, MAX_ENERGY)

    def sense_food(self, grid):
        sense_dist = self.genome['sense_distance'] * 2
        closest_food = None
        min_distance = float('inf')
        for dy in range(-sense_dist, sense_dist + 1):
            for dx in range(-sense_dist, sense_dist + 1):
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < COLS and 0 <= ny < ROWS and (dx != 0 or dy != 0):
                    cell = grid[ny][nx]
                    if cell and cell != self and not isinstance(cell, Fungus):
                        distance = dx * dx + dy * dy
                        if distance < min_distance:
                            min_distance = distance
                            closest_food = (dx, dy)
        if closest_food:
            dx, dy = closest_food
            if abs(dx) > abs(dy):
                self.direction = 1 if dx > 0 else 3
            else:
                self.direction = 2 if dy > 0 else 0
            return True
        return False

    def hunt(self, grid):
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < COLS and 0 <= ny < ROWS and (dx != 0 or dy != 0):
                    prey = grid[ny][nx]
                    if prey and prey != self and type(prey) != Omnivore:
                        success_prob = self.genome['speed'] / (self.genome['speed'] + prey.genome['speed'] + 0.1)
                        if random.random() < success_prob:
                            energy_gain = PREDATION_ENERGY if type(prey) == Predator else PREDATION_ENERGY // 2
                            self.energy += energy_gain
                            grid[ny][nx] = None
                            return True
        return False


class Fungus(Cell):
    def __init__(self, x, y, genome=None):
        if genome is None:
            genome = self.random_genome()
        super().__init__(x, y, genome)

    def random_genome(self):
        return {
            'photosynthesis': random.uniform(0, 0.2),
            'speed': 0,
            'sense_distance': 0,
            'reproduction_rate': random.uniform(0.1, 0.2)
        }

    def eat(self, grid):
        light_level = self.get_light_level(self.x, self.y)
        self.energy += light_level * self.genome['photosynthesis'] * PHOTOSYNTHESIS_ENERGY
        self.energy = min(self.energy, MAX_ENERGY)
