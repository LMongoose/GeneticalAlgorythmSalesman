import time
import math
import random
import pygame


class GeneticAlgorithm():
    def __init__(self):
        self.number_cities = 0
        self.cities = []
        self.population_size = 0
        self.population = []
        self.scores = []
        self.best = None
        self.current_best = None
        self.best_record = float("inf")
        self.current_record = float("inf")

    def generate(self, window):
        # TODO: fix error window not update after moving
        if not window.txt_num_cities.get_text().isdigit():
            window.error("Erro", "O número de cidades precisa ser um número.")
            return
        if not window.txt_pop_size.get_text().isdigit():
            window.error("Erro", "O tamanho da população precisa ser um número.")
            return
        if int(window.txt_num_cities.get_text()) <= 0:
            window.error("Erro", "O número de cidades precisa ser maior que zero.")
            return
        if int(window.txt_pop_size.get_text()) <= 0:
            window.error("Erro", "O tamanho da população precisa ser maior que zero.")
            return

        self._start(int(window.txt_num_cities.get_text()), int(window.txt_pop_size.get_text()))
        self.draw(window)

    def calculate(self, window):
        if self.number_cities > 0 and self.population_size > 0:
            for i in range(0, self.population_size):
                self._calculate_scores()
                self._normalize_scores()
                self._next_generation()
                self.draw(window)
                time.sleep(0.1)

    def draw(self, window):
        # clear both canvas
        window.canvas_current_best = pygame.Surface((600, 480))
        window.canvas_current_best.fill((200, 200, 200))
        window.canvas_total_best = pygame.Surface((600, 480))
        window.canvas_total_best.fill((200, 200, 200))

        color_line = (140, 140, 140)
        # draw paths
        for i in range(0, len(self.current_best) - 1):
            # draw on canvas 1 (current best)
            pygame.draw.line(window.canvas_current_best, color_line, self.cities[self.current_best[i]], self.cities[self.current_best[i + 1]], 3)
            # draw on canvas 2 (best)
            pygame.draw.line(window.canvas_total_best, color_line, self.cities[self.best[i]], self.cities[self.best[i + 1]], 3)
        # draw on canvas 1 (current best)
        pygame.draw.line(window.canvas_current_best, color_line, self.cities[self.current_best[len(self.current_best) - 1]], self.cities[self.current_best[0]], 3)
        # draw on canvas 2 (best)
        pygame.draw.line(window.canvas_total_best, color_line, self.cities[self.best[len(self.current_best) - 1]], self.cities[self.best[0]], 3)

        # draw cities
        for city in self.cities:
            if city == self.cities[0]:
                color_city = (0, 240, 0)
            elif city == self.cities[-1]:
                color_city = (240, 0, 0)
            else:
                color_city = (0, 0, 0)

            # draw on canvas 1 (current best)
            pygame.draw.circle(window.canvas_current_best, color_city, (city[0], city[1]), 10)
            # draw on canvas 2 (best)
            pygame.draw.circle(window.canvas_total_best, color_city, (city[0], city[1]), 10)

        # update both canvas
        window.screen.blit(window.canvas_current_best, (30, 200))
        window.screen.blit(window.canvas_total_best, (650, 200))
        pygame.display.update()

    @staticmethod
    def get_distance(points, order: list):
        _sum = 0
        for i in range(0, len(order) - 1):
            cityAindex = order[i]
            cityA = points[cityAindex]
            cityBindex = order[i + 1]
            cityB = points[cityBindex]
            _sum += math.sqrt(((cityB[0] - cityA[0]) ** 2) + ((cityB[1] - cityA[1]) ** 2))
        return _sum

    def _start(self, number_cities: int, population_size: int):
        # reset data
        self.number_cities = number_cities
        self.cities = [None] * self.number_cities
        self.population_size = population_size
        self.population = [None] * self.population_size
        self.scores = [0] * self.population_size
        self.best = None
        self.current_best = None
        self.best_record = float("inf")

        # generate random points for all cities
        for i in range(0, self.number_cities):
            self.cities[i] = (random.randint(0, 580), random.randint(0, 460))

        # generate a start path between each city
        order = []
        for i in range(0, self.number_cities):
            order.append(i)
            self.current_best = order
            self.best = order

        # shuffle start path to create population
        temp_ = order.copy()
        for i in range(0, self.population_size):
            random.shuffle(temp_)
            self.population[i] = temp_.copy()

    def _calculate_scores(self):
        self.current_record = float("inf")
        for i in range(0, len(self.population) - 1):
            distance = GeneticAlgorithm.get_distance(self.cities, self.population[i])
            if distance < self.best_record:
                self.best_record = distance
                self.best = self.population[i]
            if distance < self.current_record:
                self.current_record = distance
                self.current_best = self.population[i]
            self.scores[i] = 1 / (math.pow(distance, 8) + 1)

    def _normalize_scores(self):
        _sum = 0
        for i in range(0, len(self.scores)):
            _sum += self.scores[i]
        for i in range(0, len(self.scores)):
            self.scores[i] = self.scores[i] / _sum

    def _next_generation(self):
        new_population = []
        for i in range(0, len(self.population)):
            pathA = self._select(self.population, self.scores)
            pathB = self._select(self.population, self.scores)
            pathC = self._crossover(pathA, pathB)
            pathC = self._mutate(pathC, 0.01)
            new_population.append(pathC)
        self.population = new_population

    def _select(self, population: list, scores: list):
        # pick a path from population based on its score
        index = 0
        r = random.uniform(0.0, 1.0)
        while r > 0:
            r = r - scores[index]
            index += 1
        index -= 1
        return population[index].copy()

    def _crossover(self, pathA: list, pathB: list):
        # get a half slice of data from pathA, complete with pathB not in slice and generate a new path
        start = math.floor(random.uniform(0.0, len(pathA) - 1))
        end = math.floor(random.uniform(start + 1, len(pathA) - 1))
        newpath = pathA[start:end]
        for i in range(0, len(pathB)):
            city = pathB[i]
            if(city not in newpath):
                newpath.append(city)
        return newpath

    def _mutate(self, path: list, mutation_rate: float):
        # randomly choose 2 elements from path and swap them
        newpath = path.copy()
        for i in range(0, self.number_cities):
            if random.uniform(0.0, 1.0) < mutation_rate:
                indexA = random.randint(0, len(newpath) - 1)
                indexB = (indexA + 1) % self.number_cities
                newpath[indexA], newpath[indexB] = newpath[indexB], newpath[indexA]
        return newpath